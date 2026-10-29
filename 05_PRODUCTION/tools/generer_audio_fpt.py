# -*- coding: utf-8 -*-
"""
Génère les audios du Module 0 avec la synthèse vocale FPT.AI (DEC-0023).

Ce qui est généré (d'après 04_DONNEES, source unique) :
  - volet écoute : chaque terme des séries minimales, avec chaque voix active
    de voix.csv (F1, F2, H1), aux débits lent et normal ;
  - volet production : chaque mot support, avec la voix modèle (F1), lent et normal.

Où vont les fichiers : 04_DONNEES/audio/<référence>-<voix>-<débit>.mp3
Chaque fichier créé est ajouté à 04_DONNEES/audios.csv avec validated = false :
il devra être écouté et validé (R-AUD-01) avant d'être utilisé par le lecteur.

Clé d'accès : variable d'environnement FPT_AI_API_KEY, jamais dans le projet (DOC-04).

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py .                      -> plan seulement, rien n'est appelé
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --lecon M0-L01 --limite 6
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer          -> tout ce qui manque

Le script peut être arrêté (Ctrl+C) et relancé : les fichiers déjà présents sont sautés.
Certificats https : si le module « truststore » est installé (python -m pip install truststore),
le script vérifie les certificats avec le magasin de Windows, comme le navigateur. La vérification
n'est jamais désactivée.
"""
import argparse
import csv
import json
import os
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.request

try:
    import truststore            # vérification des certificats par le système (Windows), comme le navigateur
    truststore.inject_into_ssl()
    VERIFICATION = 'magasin de certificats du système (truststore)'
except ImportError:
    VERIFICATION = 'certificats intégrés à Python'
CONTEXTE_SSL = ssl.create_default_context()

API_URL = os.environ.get('FPT_AI_URL', 'https://api.fpt.ai/hmi/tts/v5')
VITESSE_FPT = {'slow': '-2', 'normal': '0'}   # échelle FPT.AI : -3 (lent) à +3 (rapide) ; à calibrer (DEC-0023)
VOIX_MODELE = 'F1'                            # voix unique du volet production (R-AUD-03)
DELAI_ENTRE_APPELS = 2.5                      # secondes, pour ne pas surcharger le service
ATTENTES_SI_LIMITE = [10, 20, 40, 60, 90]      # secondes d'attente successives si FPT.AI répond 429 (trop de demandes)
ATTENTE_MAX_FICHIER = 30                      # secondes d'attente du fichier préparé par FPT.AI

COLONNES_AUDIOS = ['audio_code', 'item_type', 'item_ref', 'voice', 'speed', 'source', 'file', 'validated']

# Écriture « telex » : nom de fichier en ASCII, unique pour chaque syllabe (ma, má, mà… sont distincts).
LETTRES = {'ă': 'aw', 'â': 'aa', 'ê': 'ee', 'ô': 'oo', 'ơ': 'ow', 'ư': 'uw', 'đ': 'dd'}
TONS = {'\u0301': 's', '\u0300': 'f', '\u0309': 'r', '\u0303': 'x', '\u0323': 'j'}


def telex(texte):
    morceaux = []
    for mot in texte.lower().split():
        ton = ''
        sortie = ''
        for c in unicodedata.normalize('NFD', mot):
            if c in TONS:
                ton = TONS[c]
            elif c == '\u0306':      # brève (ă)
                sortie = sortie[:-1] + 'aw'
            elif c == '\u0302':      # circonflexe (â, ê, ô)
                sortie = sortie + sortie[-1]
            elif c == '\u031b':      # crochet (ơ, ư)
                sortie = sortie + 'w'
            elif c == 'đ':
                sortie += 'dd'
            elif c.isascii() and c.isalnum():
                sortie += c
        morceaux.append(sortie + ton)
    return '_'.join(morceaux)


def lire(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def plan(donnees, lecon=None):
    paires = lire(os.path.join(donnees, 'paires_minimales.csv'))
    mots = {m['word_code']: m for m in lire(os.path.join(donnees, 'mots.csv'))}
    supports = lire(os.path.join(donnees, 'mots_lecons.csv'))
    voix = [v for v in lire(os.path.join(donnees, 'voix.csv')) if v['status'] == 'active' and v['provider'] == 'fpt']
    items = {}   # (référence, voix, débit) -> description

    def ajouter(ref, ecrit, type_item, code_voix, debit):
        cle = (ref, code_voix, debit)
        if cle not in items:
            items[cle] = {'ref': ref, 'ecrit': ecrit, 'type': type_item, 'voix': code_voix, 'debit': debit}

    for p in paires:
        if lecon and p['lesson_code'] != lecon:
            continue
        ref = p['word_code'] or p['written']
        type_item = 'word' if p['word_code'] else ('invented' if p['invented'] == 'true' else 'syllable')
        for v in voix:
            for d in VITESSE_FPT:
                ajouter(ref, p['written'], type_item, v['voice_code'], d)
    for s in supports:
        if lecon and s['lesson_code'] != lecon:
            continue
        for d in VITESSE_FPT:
            ajouter(s['word_code'], mots[s['word_code']]['written'], 'word', VOIX_MODELE, d)
    voix_fpt = {v['voice_code']: v['provider_voice'] for v in voix}
    return list(items.values()), voix_fpt


def nom_fichier(item):
    base = item['ref'] if item['type'] == 'word' else 'S-' + telex(item['ecrit'])
    return 'audio/' + base + '-' + item['voix'] + '-' + item['debit'] + '.mp3'


def avec_patience(action):
    """Refait l'action quand FPT.AI répond 429 (trop de demandes), en attendant de plus en plus."""
    for attente in ATTENTES_SI_LIMITE + [None]:
        try:
            return action()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attente is None:
                raise
            print(f'(service occupé, attente {attente} s) ', end='', flush=True)
            time.sleep(attente)


def appeler(texte, cle, voix_fpt, vitesse):
    texte_api = texte if len(texte) >= 3 else texte + ' .'   # FPT.AI refuse les textes de moins de 3 caractères
    req = urllib.request.Request(API_URL, data=texte_api.encode('utf-8'), method='POST',
                                 headers={'api_key': cle, 'voice': voix_fpt, 'speed': vitesse, 'format': 'mp3'})
    def envoyer():
        with urllib.request.urlopen(req, timeout=30, context=CONTEXTE_SSL) as r:
            return json.loads(r.read().decode('utf-8'))
    rep = avec_patience(envoyer)
    if rep.get('error') not in (0, None) or not rep.get('async'):
        raise RuntimeError('réponse FPT.AI : ' + str(rep.get('message', rep)))
    return rep['async']


def telecharger(url, destination):
    debut = time.time()
    while time.time() - debut < ATTENTE_MAX_FICHIER:
        try:
            def lire_fichier():
                with urllib.request.urlopen(url, timeout=15, context=CONTEXTE_SSL) as r:
                    return r.read()
            contenu = avec_patience(lire_fichier)
            if len(contenu) > 500:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                with open(destination, 'wb') as f:
                    f.write(contenu)
                return True
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        except urllib.error.URLError:
            pass
        time.sleep(2)   # le fichier n'est pas encore prêt
    return False


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true', help='appeler FPT.AI (sinon : plan seulement)')
    a.add_argument('--lecon', help='limiter à une leçon, par ex. M0-L01')
    a.add_argument('--limite', type=int, default=0, help='nombre maximal de fichiers à créer')
    args = a.parse_args()

    donnees = os.path.join(args.racine, '04_DONNEES')
    chemin_audios = os.path.join(donnees, 'audios.csv')
    items, voix_fpt = plan(donnees, args.lecon)
    existants = {r['file'] for r in lire(chemin_audios)}
    a_faire = [i for i in items if nom_fichier(i) not in existants
               and not os.path.exists(os.path.join(donnees, nom_fichier(i)))]
    if args.limite:
        a_faire = a_faire[:args.limite]
    caracteres = sum(max(3, len(i['ecrit'])) for i in a_faire)
    print(f"Prévus : {len(items)} fichiers ; déjà présents : {len(items) - len([i for i in items if nom_fichier(i) not in existants])} ; "
          f"à créer maintenant : {len(a_faire)} (environ {caracteres} caractères envoyés à FPT.AI)")
    for i in a_faire[:8]:
        print('  ', i['ecrit'], i['voix'], i['debit'], '->', nom_fichier(i))
    if len(a_faire) > 8:
        print('   …')
    if not args.executer:
        print("Plan seulement. Ajoutez --executer pour lancer la génération.")
        return

    print('Vérification https :', VERIFICATION)
    cle = os.environ.get('FPT_AI_API_KEY')
    if not cle:
        sys.exit("La variable FPT_AI_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")

    nouveau_fichier = not os.path.exists(chemin_audios) or os.path.getsize(chemin_audios) == 0
    crees = erreurs = 0
    with open(chemin_audios, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';', lineterminator='\n')
        if nouveau_fichier:
            w.writerow(COLONNES_AUDIOS)
        for n, i in enumerate(a_faire, 1):
            fichier = nom_fichier(i)
            print(f"[{n}/{len(a_faire)}] {i['ecrit']} · {i['voix']} · {i['debit']} … ", end='', flush=True)
            try:
                url = appeler(i['ecrit'], cle, voix_fpt[i['voix']], VITESSE_FPT[i['debit']])
                if telecharger(url, os.path.join(donnees, fichier)):
                    base = os.path.basename(fichier)[:-4]
                    w.writerow(['A-' + base, i['type'], i['ref'], i['voix'], i['debit'], 'fpt', fichier, 'false'])
                    f.flush()
                    crees += 1
                    print('ok')
                else:
                    erreurs += 1
                    print('fichier non reçu à temps')
            except Exception as e:   # on continue : le fichier manquant sera repris au prochain lancement
                erreurs += 1
                print('erreur :', e)
                if 'CERTIFICATE_VERIFY_FAILED' in str(e) and VERIFICATION.startswith('certificats'):
                    sys.exit("Certificat https non vérifiable avec Python seul. Installez le module truststore :\n"
                             "    python -m pip install truststore\npuis relancez la même commande.")
                if erreurs >= 5 and crees == 0:
                    sys.exit('Cinq erreurs sans aucun succès : arrêt. Vérifiez la clé et le quota FPT.AI.')
            time.sleep(DELAI_ENTRE_APPELS)
    print(f"Terminé : {crees} fichier(s) créé(s), {erreurs} erreur(s)." + (" Relancez la même commande pour reprendre les manquants." if erreurs else ""))


if __name__ == '__main__':
    main()
