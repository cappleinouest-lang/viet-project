# -*- coding: utf-8 -*-
"""
Génère les audios du Module 0 avec FPT.TTS-pro (FPT AI Marketplace, marketplace.fptcloud.com) — DEC-0023.

Ce qui est généré (d'après 04_DONNEES, source unique) :
  - volet écoute : chaque terme des séries minimales, avec chaque voix d'écoute du type de leçon
    (voix.csv, colonnes listen_sounds / listen_tones, DEC-0055), aux débits lent et normal ;
  - volet production : chaque mot support, avec la voix modèle (F1), lent et normal ;
  - étape E1 « Découverte » (DEC-0039) : chaque mot d'exemple de exemples_e1.csv, avec sa voix
    de femme et sa voix d'homme, lent et normal ;
  - étape E1, voyelles simples (DEC-0070) : la voyelle SEULE (a, ă, â, e, ê, i, o, ô, ơ, u, ư),
    avec les voix d'écoute de la leçon, au débit normal seulement. Fichier : audio/V-<code du son>-<voix>-normal.mp3 ;
  - page « Les 6 tons » (DEC-0052) : la série de reference_tons.csv (ma, má, mà, mả, mã, mạ),
    avec les voix VOIX_REFERENCE_TONS, lent et normal ;
  - exercice « Combien de fois ? » (DEC-0054) : chaque suite ou phrase de comptage.csv, dite
    d'un seul tenant, avec les voix d'écoute du type de leçon, lent et normal (normal seulement dans les leçons
    de tons, DEC-0043). Fichier : audio/<item_code>-<voix>-<débit>.mp3.
    Classificateurs (DEC-0062, règle de regle_classificateurs.py) : « con mèo », référence K-<mot>,
    pour les mots d'exemple d'E1 (leurs deux voix) et les mots supports d'E4 (voix modèle), lent et normal.
    Pour les PHRASES, en plus, une version « mots espacés » (débit spaced, DEC-0058) : la phrase envoyée
    avec des points de suspension entre les mots (« Tôi… thích… cà phê. »), au débit normal.

Où vont les fichiers : 04_DONNEES/audio/<référence>-<voix>-<débit>.mp3
Chaque fichier créé est ajouté à 04_DONNEES/audios.csv avec validated = false :
il devra être écouté et validé (R-AUD-01) avant d'être utilisé par le lecteur.

Modèle FPT par voix : colonne provider_model de voix.csv. Depuis DEC-0067 (2026-10-31) : F4 Ban Mai
et H6 Quang Anh en FPT.TTS-ultra au débit normal ; FPT.TTS-ultra ignore la vitesse, donc le débit
LENT de ces voix est pris chez la voix indiquée dans la colonne slow_from (F1 Ban Mai FPT.TTS-pro,
H4 Huy Phong FPT.AI-VITs) : fichiers <référence>-F1-slow.mp3 et <référence>-H4-slow.mp3.
Fichiers FPT.TTS-ultra (DEC-0068) : début gardé tel que FPT le livre ; silence après le mot complété
jusqu'à 0,35 s, sans rien couper (decoupe_audio.completer_fin). Raccourcir aussi le début
(decoupe_audio.rogner_silences) reste possible avec ROGNER_ULTRA = True.

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
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --refaire --voix F3 --debit slow
        -> refait seulement les audios lents de F3 (filtres --voix et --debit : aussi sans --refaire)
    python 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --refaire --liste 07_QUALITE\\audios_a_refaire.csv
        -> refait les audios jugés « à refaire » à l'écoute (valider_audios.py, DEC-0065)
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
VOIX_MODELE = 'F4'                            # voix unique du volet production (R-AUD-03, DEC-0067)
VOIX_REFERENCE_TONS = ['F4', 'H6']            # page « Les 6 tons » : une voix de femme, une d'homme (DEC-0052, DEC-0067)
DELAI_ENTRE_APPELS = 1.5                      # secondes, pour ne pas surcharger le service
ATTENTES_SI_LIMITE = [10, 30]                 # secondes d'attente successives si le service répond 429
DOUBLER = False                               # --doubler : envoyer « mot, mot. » et garder la 2e occurrence
ROGNER_ULTRA = False                          # DEC-0068 : fichiers Ultra gardés bruts (silences non raccourcis)
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


def voyelle_simple(code):
    """Voyelle simple (DEC-0070) : sons PH-VS-… et PH-VO-… de sons.csv (a, i, u, e, o, ô, ơ, ư, ê, â, ă).
    Diphtongues et triphtongues exclues tant qu'elles n'ont pas été essayées seules."""
    return code.startswith('PH-VS-') or code.startswith('PH-VO-')


def plan(donnees, lecon=None):
    paires = lire(os.path.join(donnees, 'paires_minimales.csv'))
    mots = {m['word_code']: m for m in lire(os.path.join(donnees, 'mots.csv'))}
    supports = lire(os.path.join(donnees, 'mots_lecons.csv'))
    toutes = {v['voice_code']: v for v in lire(os.path.join(donnees, 'voix.csv'))}
    voix = [v for v in toutes.values() if v['status'] == 'active' and v['provider'] == FOURNISSEUR]
    # Débit lent emprunté (DEC-0067) : voix -> voix qui fournit son débit lent (colonne slow_from).
    lent_de = {v['voice_code']: v['slow_from'] for v in voix if v.get('slow_from')}
    items = {}   # (référence, voix, débit) -> description
    # Voix d'écoute selon le type de leçon (DEC-0055) : colonnes listen_sounds / listen_tones de voix.csv.
    lecons_tons = {l['lesson_code'] for l in lire(os.path.join(donnees, 'lecons.csv')) if l['is_tone_lesson'] == 'true'}
    def voix_ecoute(code_lecon):
        col = 'listen_tones' if code_lecon in lecons_tons else 'listen_sounds'
        return [v for v in voix if v.get(col, 'true') == 'true']

    def ajouter(ref, ecrit, type_item, code_voix, debit):
        if debit == 'slow':
            code_voix = lent_de.get(code_voix, code_voix)    # DEC-0067 : fichier lent de F1 / H4
        cle = (ref, code_voix, debit)
        if cle not in items:
            items[cle] = {'ref': ref, 'ecrit': ecrit, 'type': type_item, 'voix': code_voix, 'debit': debit}

    for p in paires:
        if lecon and p['lesson_code'] != lecon:
            continue
        ref = p['word_code'] or p['written']
        type_item = 'word' if p['word_code'] else ('invented' if p['invented'] == 'true' else 'syllable')
        for v in voix_ecoute(p['lesson_code']):
            for d in VITESSE_FPT:
                ajouter(ref, p['written'], type_item, v['voice_code'], d)
    for s in supports:
        if lecon and s['lesson_code'] != lecon:
            continue
        for d in VITESSE_FPT:
            ajouter(s['word_code'], mots[s['word_code']]['written'], 'word', VOIX_MODELE, d)
    actives = {v['voice_code'] for v in voix}
    # E1, voyelles simples (DEC-0070) : la voyelle seule, débit normal, voix d'écoute de la leçon.
    sons = {s['sound_code']: s for s in lire(os.path.join(donnees, 'sons.csv'))}
    vues = set()
    for p in paires:
        e = p['element']
        if (lecon and p['lesson_code'] != lecon) or e not in sons or not voyelle_simple(e) or (p['lesson_code'], e) in vues:
            continue
        vues.add((p['lesson_code'], e))
        for v in voix_ecoute(p['lesson_code']):
            ajouter('V-' + e, sons[e]['grapheme'], 'voyelle', v['voice_code'], 'normal')
    for x in lire(os.path.join(donnees, 'exemples_e1.csv')):      # DEC-0039
        if (lecon and x['lesson_code'] != lecon) or not x['word_code']:
            continue
        for code_voix in (x['voice_f'], x['voice_h']):
            if code_voix in actives:
                for d in VITESSE_FPT:
                    ajouter(x['word_code'], mots[x['word_code']]['written'], 'word', code_voix, d)
    if not lecon:                                                  # DEC-0052 : série des 6 tons
        for x in lire(os.path.join(donnees, 'reference_tons.csv')):
            ref = x['word_code'] or x['written']
            for code_voix in VOIX_REFERENCE_TONS:
                if code_voix in actives:
                    for d in VITESSE_FPT:
                        ajouter(ref, x['written'], 'word' if x['word_code'] else 'syllable', code_voix, d)
    for x in lire(os.path.join(donnees, 'comptage.csv')):           # DEC-0054
        if lecon and x['lesson_code'] != lecon:
            continue
        if x['kind'] == 'phrase':                                    # DEC-0058 : mots espacés
            for v in voix_ecoute(x['lesson_code']):
                ajouter(x['item_code'], phrase_espacee(x, mots), 'sequence', v['voice_code'], 'spaced')
        for v in voix_ecoute(x['lesson_code']):
            for d in VITESSE_FPT:
                if d == 'slow' and x['lesson_code'] in lecons_tons:
                    continue
                ajouter(x['item_code'], x['written'], 'sequence', v['voice_code'], d)
    # Classificateurs en E1 et E4 (DEC-0062) : même règle que generer_lecteur.py.
    import regle_classificateurs as rc
    ctx = rc.charger(donnees)
    for x in lire(os.path.join(donnees, 'exemples_e1.csv')):
        if (lecon and x['lesson_code'] != lecon) or not x['word_code']:
            continue
        a = rc.appui(ctx, x['word_code'], x['lesson_code'], x['element'])
        if a:
            for code_voix in (x['voice_f'], x['voice_h']):
                if code_voix in actives:
                    for d in VITESSE_FPT:
                        ajouter(a[1], a[0], 'sequence', code_voix, d)
    for s in supports:
        if lecon and s['lesson_code'] != lecon:
            continue
        a = rc.appui(ctx, s['word_code'], s['lesson_code'])
        if a:
            for d in VITESSE_FPT:
                ajouter(a[1], a[0], 'sequence', VOIX_MODELE, d)
    utiles = voix + [toutes[c] for c in sorted(set(lent_de.values())) if c in toutes]   # + voix du débit lent
    voix_fpt = {v['voice_code']: v['provider_voice'] for v in utiles}
    MODELE_PAR_VOIX.update({v['voice_code']: (v.get('provider_model') or MODELE) for v in utiles})
    VITESSE_PAR_VOIX.update({v['voice_code']: dict(VITESSE_FPT, spaced=1.0, **({'slow': float(v['provider_speed_slow'])}
                             if v.get('provider_speed_slow') else {})) for v in utiles})
    return list(items.values()), voix_fpt


def phrase_espacee(x, mots):
    """« Tôi thích cà phê. » -> « Tôi, thích, cà phê. » : virgules entre les MOTS (DEC-0067, à la place
    des points de suspension de DEC-0058 : plus d'espace, moins haché à l'écoute ; un mot de deux syllabes
    reste d'un seul tenant), majuscule et ponctuation finale gardées."""
    ecrits = [mots[w]['written'] if w in mots else w for w in x['word_codes'].split()]
    if not ecrits:
        return x['written']
    ecrits[0] = ecrits[0][:1].upper() + ecrits[0][1:]
    fin = x['written'].rstrip()[-1:] if x['written'].rstrip()[-1:] in '.?!' else '.'
    return ', '.join(ecrits) + fin


def nom_fichier(item):
    base = item['ref'] if item['type'] in ('word', 'sequence', 'voyelle') else 'S-' + telex(item['ecrit'])
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
    champs = {'model': modele or MODELE, 'input': texte, 'voice': voix_fpt, 'speed': vitesse, 'response_format': 'mp3'}
    if 'ultra' in (modele or MODELE).lower():
        champs['text'] = texte      # nom du champ dans l'exemple de la fiche FPT.TTS-ultra (essai du 2026-10-31)
    corps = json.dumps(champs, ensure_ascii=False).encode('utf-8')
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
    decoupe_audio.traiter_fichier(brut, temporaire, DOUBLER, rogner=ROGNER_ULTRA and 'ultra' in (modele or MODELE).lower(),
                                 fin='ultra' in (modele or MODELE).lower())
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
    a.add_argument('--voix', help='limiter à une ou plusieurs voix, par ex. F3 ou F3,H4')
    a.add_argument('--debit', help='limiter à un ou plusieurs débits : slow, normal, spaced (séparés par des virgules)')
    a.add_argument('--liste', help="limiter aux audios d'un fichier CSV (colonne file), par ex. 07_QUALITE/audios_a_refaire.csv")
    args = a.parse_args()
    global DOUBLER
    DOUBLER = args.doubler

    donnees = os.path.join(args.racine, '04_DONNEES')
    chemin_audios = os.path.join(donnees, 'audios.csv')
    items, voix_fpt = plan(donnees, args.lecon)
    if args.voix:
        items = [i for i in items if i['voix'] in args.voix.split(',')]
    if args.debit:
        items = [i for i in items if i['debit'] in args.debit.split(',')]
    if args.liste:   # DEC-0065 : seulement les audios d'une liste (colonne file), par ex. 07_QUALITE/audios_a_refaire.csv
        voulus = {r['file'] for r in lire(args.liste)}
        items = [i for i in items if nom_fichier(i) in voulus]
        print(f"Liste {args.liste} : {len(voulus)} audio(s) demandé(s), {len(items)} trouvé(s) dans le plan.")
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
