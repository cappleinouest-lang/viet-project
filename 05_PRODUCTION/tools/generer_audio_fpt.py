# -*- coding: utf-8 -*-
"""
Génère les audios du Module 0 avec FPT.TTS-pro (FPT AI Marketplace, marketplace.fptcloud.com) — DEC-0023.

Ce qui est généré (d'après 04_DONNEES, source unique) :
  - volet écoute : chaque terme des séries minimales, avec chaque voix active
    de voix.csv (provider = fpt-mkp), aux débits lent et normal ;
  - volet production : chaque mot support, avec la voix modèle (F1), lent et normal ;
  - étape E1 « Découverte » (DEC-0039) : chaque mot d'exemple de exemples_e1.csv, avec sa voix
    de femme et sa voix d'homme, lent et normal.

Où vont les fichiers : 04_DONNEES/audio/<référence>-<voix>-<débit>.mp3
Chaque fichier créé est ajouté à 04_DONNEES/audios.csv avec validated = false :
il devra être écouté et validé (R-AUD-01) avant d'être utilisé par le lecteur.

Modèle FPT par voix : colonne provider_model de voix.csv (FPT.TTS-pro pour Ban Mai,
FPT.AI-VITs pour les voix d'homme, choix du 2026-10-29 après écoute).

Chaque fichier est égalisé en volume (niveau de parole -20 dBFS, crête <= -1 dBFS, decoupe_audio.py) ;
le fichier reçu de FPT est gardé dans 04_DONNEES/audio/_bruts/. À lancer avec le Python de .venv-asr,
qui contient numpy et soundfile :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_fpt.py . ...

Option --doubler (désactivée par défaut) : envoie « mot, mot. » et ne garde que la 2e occurrence
(découpage par decoupe_audio.py, brut conservé dans 04_DONNEES/audio/_bruts/). Utile seulement
pour une voix qui avale la consonne de départ d'un mot isolé.

Clé d'accès : variable d'environnement FPT_MKP_API_KEY (clé créée dans la marketplace,
menu Serverless Inference > API Keys), jamais dans le projet (DOC-04).

Usage (depuis C:\\VIET_PROJECT ; remplacer python par .venv-asr\\Scripts\\python.exe) :
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py .                      -> plan seulement, rien n'est appelé
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --lecon M0-L01 --limite 4
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer          -> tout ce qui manque
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --refaire -> refait les audios déjà présents
        (les anciens fichiers sont déplacés dans 04_DONNEES/audio/_anciens/, rien n'est effacé ;
         leurs lignes de audios.csv sont remplacées, avec validated = false)

Le script peut être arrêté (Ctrl+C) et relancé : les fichiers déjà présents sont sautés.
Certificats https : si le module « truststore » est installé (python -m pip install truststore),
le script vérifie les certificats avec le magasin de Windows, comme le navigateur. La vérification
n'est jamais désactivée.
"""
import argparse
import csv
import json
import os
import shutil
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

API_URL = os.environ.get('FPT_MKP_URL', 'https://mkp-api.fptcloud.com/v1/audio/speech')
MODELE = 'FPT.TTS-pro'
FOURNISSEUR = 'fpt-mkp'                       # valeur de la colonne provider de voix.csv
VITESSE_FPT = {'slow': 0.8, 'normal': 1.0}    # valeurs par défaut ; « lent » propre à chaque voix : colonne provider_speed_slow de voix.csv
VITESSE_PAR_VOIX = {}                         # rempli par plan()
VOIX_MODELE = 'F1'                            # voix unique du volet production (R-AUD-03)
DELAI_ENTRE_APPELS = 1.5                      # secondes, pour ne pas surcharger le service
ATTENTES_SI_LIMITE = [10, 30]                 # secondes d'attente successives si le service répond 429
DOUBLER = False                               # --doubler : envoyer « mot, mot. » et garder la 2e occurrence
MODELE_PAR_VOIX = {}                          # rempli par plan() d'après la colonne provider_model de voix.csv
ATTENTE_MAX_FICHIER = 30                      # secondes d'attente si le service renvoie un lien au lieu du fichier

COLONNES_AUDIOS = ['audio_code', 'item_type', 'item_ref', 'voice', 'speed', 'source', 'file', 'validated']

MESSAGES_HTTP = {
    401: 'clé refusée : vérifiez la variable FPT_MKP_API_KEY (nouvelle fenêtre PowerShell après setx)',
    402: 'solde du portefeuille FPT à zéro : rechargez le compte sur la marketplace',
    404: 'modèle ou adresse inconnus',
    429: 'trop de demandes',
}

# Écriture « telex » : nom de fichier en ASCII, unique pour chaque syllabe (ma, má, mà… sont distincts).
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
    voix = [v for v in lire(os.path.join(donnees, 'voix.csv'))
            if v['status'] == 'active' and v['provider'] == FOURNISSEUR]
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
    actives = {v['voice_code'] for v in voix}
    for x in lire(os.path.join(donnees, 'exemples_e1.csv')):      # DEC-0039
        if (lecon and x['lesson_code'] != lecon) or not x['word_code']:
            continue
        for code_voix in (x['voice_f'], x['voice_h']):
            if code_voix in actives:
                for d in VITESSE_FPT:
                    ajouter(x['word_code'], mots[x['word_code']]['written'], 'word', code_voix, d)
    voix_fpt = {v['voice_code']: v['provider_voice'] for v in voix}
    MODELE_PAR_VOIX.update({v['voice_code']: (v.get('provider_model') or MODELE) for v in voix})
    VITESSE_PAR_VOIX.update({v['voice_code']: dict(VITESSE_FPT, **({'slow': float(v['provider_speed_slow'])}
                             if v.get('provider_speed_slow') else {})) for v in voix})
    return list(items.values()), voix_fpt


def nom_fichier(item):
    base = item['ref'] if item['type'] == 'word' else 'S-' + telex(item['ecrit'])
    return 'audio/' + base + '-' + item['voix'] + '-' + item['debit'] + '.mp3'


def avec_patience(action, etape=''):
    """Refait l'action quand le service répond 429 (trop de demandes), en attendant de plus en plus."""
    for attente in ATTENTES_SI_LIMITE + [None]:
        try:
            return action()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attente is None:
                try:
                    detail = e.read().decode('utf-8', 'replace')[:300]
                except Exception:
                    detail = ''
                explication = MESSAGES_HTTP.get(e.code, '')
                raise RuntimeError(f'HTTP {e.code} pendant {etape}'
                                   + (f' ({explication})' if explication else '')
                                   + f' ; message du service : {detail or "(vide)"}')
            print(f'(service occupé pendant {etape}, attente {attente} s) ', end='', flush=True)
            time.sleep(attente)


def ouvrir(req, delai):
    with urllib.request.urlopen(req, timeout=delai, context=CONTEXTE_SSL) as r:
        return r.headers.get('Content-Type', ''), r.read()


def telecharger_lien(url):
    """Si le service renvoie un lien au lieu du fichier : attend que le fichier soit prêt."""
    debut = time.time()
    while time.time() - debut < ATTENTE_MAX_FICHIER:
        try:
            _, contenu = avec_patience(lambda: ouvrir(url, 15), 'le téléchargement')
            if len(contenu) > 500:
                return contenu
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        except urllib.error.URLError:
            pass
        time.sleep(2)
    return None


def chercher_lien(reponse):
    if isinstance(reponse, dict):
        for k in ('url', 'link', 'audio_url', 'async'):
            if isinstance(reponse.get(k), str) and reponse[k].startswith('http'):
                return reponse[k]
        for v in reponse.values():
            lien = chercher_lien(v)
            if lien:
                return lien
    return None


def synthetiser(texte, cle, voix_fpt, vitesse, modele=None):
    """Renvoie le contenu mp3, ou lève une erreur."""
    corps = json.dumps({'model': modele or MODELE, 'input': texte, 'voice': voix_fpt,
                        'speed': vitesse, 'response_format': 'mp3'}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(API_URL, data=corps, method='POST',
                                 headers={'Authorization': 'Bearer ' + cle,
                                          'Content-Type': 'application/json'})
    type_contenu, contenu = avec_patience(lambda: ouvrir(req, 60), 'la demande')
    if 'json' in type_contenu or contenu[:1] in (b'{', b'['):
        reponse = json.loads(contenu.decode('utf-8'))
        lien = chercher_lien(reponse)
        if not lien:
            raise RuntimeError('réponse inattendue du service : ' + json.dumps(reponse, ensure_ascii=False)[:300])
        contenu = telecharger_lien(lien)
        if not contenu:
            raise RuntimeError('fichier non reçu à temps')
    if len(contenu) < 500:
        raise RuntimeError(f'fichier trop petit ({len(contenu)} octets) : probablement pas un mp3')
    return contenu


def refaire(a_faire, donnees, chemin_audios, cle, voix_fpt):
    """Régénère des audios existants : l'ancien fichier part dans audio/_anciens/, la ligne de audios.csv est remplacée."""
    lignes = lire(chemin_audios)
    nouvelles = {}
    anciens = os.path.join(donnees, 'audio', '_anciens')
    horodatage = time.strftime('%Y%m%d-%H%M%S')
    crees = erreurs = 0
    try:
        for n, i in enumerate(a_faire, 1):
            fichier = nom_fichier(i)
            destination = os.path.join(donnees, fichier)
            print(f"[{n}/{len(a_faire)}] {i['ecrit']} · {i['voix']} · {i['debit']} … ", end='', flush=True)
            try:
                nouveau = destination[:-4] + '.nouveau.mp3'
                produire(i['ecrit'], cle, voix_fpt[i['voix']], VITESSE_PAR_VOIX[i['voix']][i['debit']], nouveau, MODELE_PAR_VOIX[i['voix']])
                if os.path.exists(destination):
                    os.makedirs(anciens, exist_ok=True)
                    nom = os.path.basename(fichier)[:-4] + '-' + horodatage + '.mp3'
                    shutil.move(destination, os.path.join(anciens, nom))
                os.replace(nouveau, destination)
                base = os.path.basename(fichier)[:-4]
                nouvelles[fichier] = {'audio_code': 'A-' + base, 'item_type': i['type'], 'item_ref': i['ref'],
                                      'voice': i['voix'], 'speed': i['debit'], 'source': FOURNISSEUR,
                                      'file': fichier, 'validated': 'false'}
                crees += 1
                print('ok')
            except Exception as e:   # l'ancien fichier reste en place si la régénération échoue
                erreurs += 1
                print('erreur :', e)
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    print('Arrêt : problème de clé ou de solde.')
                    break
            time.sleep(DELAI_ENTRE_APPELS)
    finally:   # même après Ctrl+C : audios.csv est réécrit avec les fichiers déjà refaits
        if nouvelles:
            resultat = [nouvelles.pop(l['file'], l) for l in lignes] + list(nouvelles.values())
            with open(chemin_audios, 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=COLONNES_AUDIOS, delimiter=';', lineterminator='\n')
                w.writeheader()
                w.writerows(resultat)
    print(f"Terminé : {crees} fichier(s) refait(s), {erreurs} erreur(s). Anciens fichiers : 04_DONNEES/audio/_anciens/")


def produire(texte, cle, voix_fpt, vitesse, destination, modele=None):
    """Crée le mp3 final : appel FPT (texte doublé si DOUBLER), puis découpage éventuel
    et égalisation du volume (decoupe_audio.py). Le fichier reçu de FPT est gardé dans audio/_bruts/."""
    import decoupe_audio
    contenu = synthetiser(f'{texte}, {texte}.' if DOUBLER else texte, cle, voix_fpt, vitesse, modele)
    bruts = os.path.join(os.path.dirname(os.path.dirname(destination)), 'audio', '_bruts')
    os.makedirs(bruts, exist_ok=True)
    brut = os.path.join(bruts, os.path.basename(destination).replace('.nouveau', ''))
    with open(brut, 'wb') as f:
        f.write(contenu)
    temporaire = destination + '.tmp.mp3'
    decoupe_audio.traiter_fichier(brut, temporaire, DOUBLER)
    os.replace(temporaire, destination)


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true', help='appeler FPT.TTS-pro (sinon : plan seulement)')
    a.add_argument('--lecon', help='limiter à une leçon, par ex. M0-L01')
    a.add_argument('--limite', type=int, default=0, help='nombre maximal de fichiers à créer')
    a.add_argument('--refaire', action='store_true',
                   help='refaire les audios déjà présents (anciens fichiers mis de côté dans audio/_anciens/)')
    a.add_argument('--doubler', action='store_true', help='envoyer « mot, mot. » et garder la 2e occurrence')
    args = a.parse_args()
    global DOUBLER
    DOUBLER = args.doubler

    donnees = os.path.join(args.racine, '04_DONNEES')
    chemin_audios = os.path.join(donnees, 'audios.csv')
    items, voix_fpt = plan(donnees, args.lecon)
    if not voix_fpt:
        sys.exit(f"Aucune voix active avec provider = {FOURNISSEUR} dans voix.csv.")
    existants = {r['file'] for r in lire(chemin_audios)}
    manquants = [i for i in items if nom_fichier(i) not in existants
                 and not os.path.exists(os.path.join(donnees, nom_fichier(i)))]
    if args.refaire:
        presents = {r['file'] for r in lire(chemin_audios)} | {
            nom_fichier(i) for i in items if os.path.exists(os.path.join(donnees, nom_fichier(i)))}
        cibles = [i for i in items if nom_fichier(i) in presents]
        print(f"Mode --refaire : {len(cibles)} audio(s) déjà présent(s) seront refaits ; rien d'autre.")
    else:
        cibles = manquants
    a_faire = cibles[:args.limite] if args.limite else cibles
    caracteres = sum((2 * len(i['ecrit']) + 3) if DOUBLER else len(i['ecrit']) for i in a_faire)
    print(f"Voix utilisées : " + ', '.join(f'{c} = {v} ({MODELE_PAR_VOIX[c]}, lent {VITESSE_PAR_VOIX[c]["slow"]})' for c, v in voix_fpt.items()))
    print("Mots doublés puis découpés : " + ("oui" if DOUBLER else "non (mot seul)"))
    print(f"Prévus : {len(items)} fichiers ; déjà présents : {len(items) - len(manquants)} ; "
          f"à créer maintenant : {len(a_faire)} (environ {caracteres} caractères envoyés)")
    for i in a_faire[:8]:
        print('  ', i['ecrit'], i['voix'], i['debit'], '->', nom_fichier(i))
    if len(a_faire) > 8:
        print('   …')
    if not args.executer:
        print("Plan seulement. Ajoutez --executer pour lancer la génération.")
        return

    print('Vérification https :', VERIFICATION)
    try:
        import numpy, soundfile   # noqa: F401
    except ImportError:
        sys.exit("numpy et soundfile sont nécessaires (égalisation du volume, découpage).\n"
                 "Lancez le script avec le Python du projet : .venv-asr\\Scripts\\python.exe ...")
    cle = os.environ.get('FPT_MKP_API_KEY')
    if not cle:
        sys.exit("La variable FPT_MKP_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")

    if args.refaire:
        refaire(a_faire, donnees, chemin_audios, cle, voix_fpt)
        return

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
                destination = os.path.join(donnees, fichier)
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                produire(i['ecrit'], cle, voix_fpt[i['voix']], VITESSE_PAR_VOIX[i['voix']][i['debit']], destination, MODELE_PAR_VOIX[i['voix']])
                base = os.path.basename(fichier)[:-4]
                w.writerow(['A-' + base, i['type'], i['ref'], i['voix'], i['debit'], FOURNISSEUR, fichier, 'false'])
                f.flush()
                crees += 1
                print('ok')
            except Exception as e:   # on continue : le fichier manquant sera repris au prochain lancement
                erreurs += 1
                print('erreur :', e)
                if 'CERTIFICATE_VERIFY_FAILED' in str(e) and VERIFICATION.startswith('certificats'):
                    sys.exit("Certificat https non vérifiable avec Python seul. Installez le module truststore :\n"
                             "    python -m pip install truststore\npuis relancez la même commande.")
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    sys.exit('Arrêt : problème de clé ou de solde, inutile de continuer.')
                if erreurs >= 5 and crees == 0:
                    sys.exit('Cinq erreurs sans aucun succès : arrêt. Vérifiez la clé et le solde FPT.')
            time.sleep(DELAI_ENTRE_APPELS)
    print(f"Terminé : {crees} fichier(s) créé(s), {erreurs} erreur(s)."
          + (" Relancez la même commande pour reprendre les manquants." if erreurs else ""))


if __name__ == '__main__':
    main()
