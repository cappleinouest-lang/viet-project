# -*- coding: utf-8 -*-
"""
GÉNÉRATEUR DU LECTEUR D'ACTIVITÉS (DEC-0017, DEC-0030)
=======================================================

À QUOI IL SERT
    Le lecteur (05_PRODUCTION/lecteur/) ne contient aucun contenu pédagogique.
    Ce script lit les données de référence (04_DONNEES, source unique) et
    fabrique, dans 06_LIVRABLES/lecteur/, un lecteur prêt à ouvrir :
      - donnees.js : TOUT le contenu (leçons, séries, termes, symboles, sons
        d'E1, voix, paramètres), sous la forme window.DONNEES_LECTEUR = {...} ;
      - index.html, lecteur.css, lecteur.js : copiés tels quels ;
      - audio/ : les fichiers mp3 utilisés (validés, ou tous avec --non-valides) ;
      - lecteur_autonome.html : la même chose en UN seul fichier.
    06_LIVRABLES est jetable : on peut l'effacer et le regénérer (DOC-03).
    Ce script ne modifie aucun fichier source et n'utilise que Python standard.

USAGE (depuis C:\\VIET_PROJECT)
    python 05_PRODUCTION\\tools\\generer_lecteur.py .
    python 05_PRODUCTION\\tools\\generer_lecteur.py . --non-valides
        (essai : utilise aussi les audios pas encore validés, R-AUD-01)
    Résultat : ouvrir 06_LIVRABLES\\lecteur\\index.html.

ENTRÉES (04_DONNEES, sauf mention)
    lecons.csv            leçons : numéro, titre, seuil, tons ?, deux parties ? ;
                          e1_first : sons d'abord (DEC-0072) ; e1_rappel : sons en rappel court (DEC-0075)
    paires_minimales.csv  séries minimales : termes, position, élément contrasté
    mots.csv, sons.csv, tons.csv, reperes_sons.csv
                          sens des mots, symboles, place, repères (DEC-0038, DEC-0042)
    exemples_e1.csv       mots d'exemple de l'étape E1 (DEC-0039) ; syllabes sans sens (DEC-0073) ;
                          colonnes voice_f / voice_h ignorées depuis DEC-0077 (voix d'E1 : VOIX_PAR_USAGE)
    voix.csv              voix actives ; voix d'écoute E2/E3 par type de leçon (listen_sounds / listen_tones, DEC-0055) ;
                          slow_from : voix qui fournit le débit lent (DEC-0067 : F4 <- F1)
    audio/e1_sequences/sequences_e1.csv
                          séquences d'écoute de l'E1 (MOD-D25), fabriquées par concatener_e1.py
    mots_lecons.csv       mots supports de chaque leçon : les mots d'E4 (DEC-0050)
    courbes_modele.csv    courbes mélodiques du modèle (F4, lent F1), calculées par courbes_modele.py (DEC-0050)
    reference_tons.csv    série ma, má, mà, mả, mã, mạ de la page « Les 6 tons » (DEC-0052)
    comptage.csv          suites de l'exercice « Combien de fois ? » (DEC-0054) ; syllabes.csv pour repérer les cibles
    audios.csv            fichiers audio déclarés et leur validation
    05_PRODUCTION/lecteur/images_provisoires.csv   emoji en attendant images.csv

MODIFICATIONS COURANTES : OÙ REGARDER
    seuils de verrou, 20 réponses, 2 voix…  → PARAMETRES (ci-dessous)
    voix selon l'activité (DEC-0077)         → VOIX_PAR_USAGE
    hauteur des voix de synthèse provisoires → VOIX_PROVISOIRES
    ordre des séries (voyelles d'abord…)     → ORDRE_POSITIONS
    noms des parties A / B                   → parties()
    ce que reçoit le lecteur pour un terme   → main(), bloc « sortie_termes »
    Si on ajoute une information ici, il faut aussi l'utiliser dans lecteur.js.
"""
# Bibliothèques standard de Python (rien à installer).
import csv
import datetime
import json
import os
import shutil
import sys

# ---------------------------------------------------------------------------
# 1. Arguments et dossiers
# ---------------------------------------------------------------------------
# ARGS : arguments sans « -- » ; le premier est la racine du projet (« . »).
# NON_VALIDES : vrai si --non-valides est donné (mode d'essai).
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
RACINE = ARGS[0] if ARGS else '.'
NON_VALIDES = '--non-valides' in sys.argv
DONNEES = os.path.join(RACINE, '04_DONNEES')
LECTEUR = os.path.join(RACINE, '05_PRODUCTION', 'lecteur')
SORTIE = os.path.join(RACINE, '06_LIVRABLES', 'lecteur')

# ---------------------------------------------------------------------------
# 2. Réglages transmis au lecteur
# ---------------------------------------------------------------------------
# PARAMETRES est recopié tel quel dans donnees.js et lu par lecteur.js (variable P).
# Le seuil de réussite, lui, est propre à chaque leçon : lecons.csv, colonne listen_threshold.
# Paramètres du verrou d'écoute (R-VOL-05, DEC-0032) et du lecteur (PROG-ACT).
PARAMETRES = {
    'fenetre_score': 20,          # nombre de dernières réponses prises en compte
    'min_reussites_par_serie': 2, # au débit normal (DEC-0032)
    'min_voix': 2,                # R-VOL-05
    'max_meme_position': 3,       # PROG-ACT § 4 : pas plus de 3 fois de suite la même bonne réponse
    'ecart_max_lecons': 3,        # R-VOL-04 (non contrôlé tant que le volet production n'existe pas)
    'essais_max_e4': 3,           # PROG-ACT : 3 essais au plus par mot en E4, puis mot suivant
}

# Quand un fichier audio manque, le lecteur fait lire le mot par la voix de synthèse de
# l'appareil (une seule voix) : on imite plusieurs voix en changeant la hauteur
# (> 1 : plus aigu, voix de femme ; < 1 : plus grave, voix d'homme) et la vitesse.
# Ajouter ici toute nouvelle voix de voix.csv.
# Réglages provisoires de la synthèse vocale du navigateur, en attendant les audios
# FPT.AI (DEC-0023). Les « voix » F1, F2, H1 sont simulées par la hauteur de voix.
VOIX_PROVISOIRES = {
    'F1': {'hauteur': 1.15, 'vitesse': 1.0},
    'F2': {'hauteur': 1.4, 'vitesse': 0.95},
    'F3': {'hauteur': 1.35, 'vitesse': 0.95},
    'H1': {'hauteur': 0.7, 'vitesse': 1.0},
    'H3': {'hauteur': 0.7, 'vitesse': 1.0},
    'H4': {'hauteur': 0.85, 'vitesse': 0.95},
    'F4': {'hauteur': 1.15, 'vitesse': 1.0},
    'H6': {'hauteur': 0.8, 'vitesse': 1.0},
}
# Vitesse de la voix de synthèse pour chaque débit (n'agit pas sur les fichiers audio).
# Les clés 'slow' et 'normal' sont aussi celles de audios.csv (colonne speed).
DEBITS = {'slow': 0.55, 'normal': 0.9, 'spaced': 0.9}   # spaced : mots espacés (DEC-0058)
# Voix selon l'activité (DEC-0077, stratégie multi-voix par usage) : [femme, homme].
# E2 / E3 et échauffement ne sont pas ici : colonnes listen_sounds / listen_tones de voix.csv
# (leçons de sons : F4 + H4 ; leçons de tons : F1 + H3).
VOIX_PAR_USAGE = {
    'e1_voyelle': ['F1', 'H4'],   # E1, voyelle seule (DEC-0070)
    'e1_syllabe': ['F1', 'H4'],   # E1, syllabes sans sens (DEC-0073)
    'e1_mots':    ['F4', 'H4'],   # E1, mots d'exemple des leçons de sons (DEC-0039)
    'tons':       ['F1', 'H3'],   # leçons de tons (E1) et page « Les 6 tons » (DEC-0052)
    'combien':    ['F1', 'H3'],   # « Combien de fois ? » (DEC-0054) et phrases espacées (DEC-0058)
}
# Voix modèle des étapes de production E4–E5 (R-AUD-03) : Ban Mai F4 seule (DEC-0067, DEC-0077).
VOIX_MODELE = 'F4'
# Page « Les 6 tons » (DEC-0052) : F1 + H3 (DEC-0077).
VOIX_REFERENCE_TONS = VOIX_PAR_USAGE['tons']

# Ordre d'affichage des séries d'une leçon selon la place de l'élément contrasté :
# 0 voyelles (et tons), 1 consonnes de début, 2 finales. Sert aussi au découpage en parties
# (partie A = groupe 0, partie B = le reste).
ORDRE_POSITIONS = {'nucleus': 0, 'glide': 0, 'initial': 1, 'final': 2}


# ---------------------------------------------------------------------------
# 3. Fonctions utilitaires
# ---------------------------------------------------------------------------
# lire('mots.csv') : renvoie la liste des lignes d'un CSV (séparateur « ; », UTF-8),
# chaque ligne étant un dictionnaire {nom de colonne: valeur}. Fichier absent : liste vide.
def lire(nom, dossier=DONNEES):
    chemin = os.path.join(dossier, nom)
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


# Exemple : séries [xem/xêm, xem/xen] → ['PH-VS-e', 'PH-VO-ee', 'PH-FI-m', 'PH-FI-n'].
def elements_de(series):
    """Sons (ou tons) des séries, dans l'ordre d'apparition : un écran E1 par élément (DEC-0039)."""
    res = []
    for s in series:
        for t in s['termes']:
            if t['element'] not in res:
                res.append(t['element'])
    return res


# Renvoie la liste des parties d'une leçon. Sans découpage : une seule partie « U ».
# Avec découpage (colonne split_parts de lecons.csv) : A = séries de voyelles, B = les autres.
# Nom du personnage d'une voix, pour l'affichage de test (DEC-0047) : début de la colonne
# note de voix.csv (« Ban Mai (marketplace…) ; … » → « Ban Mai »), sinon l'identifiant FPT.
def nom_personnage(v):
    note = v.get('note', '')
    for sep in (' (', ' :', ' ;'):
        note = note.split(sep)[0]
    return note.strip() or v.get('provider_voice', '') or v['voice_code']


def parties(liste, couper):
    """Une leçon « en deux parties » (DEC-0037) : voyelles, puis consonnes et finales."""
    if not couper:
        return [{'code': 'U', 'titre': '', 'series': [s['code'] for s in liste], 'elements': elements_de(liste)}]
    a = [s for s in liste if s['groupe'] == 0]
    b = [s for s in liste if s['groupe'] != 0]
    return [{'code': 'A', 'titre': 'Voyelles', 'series': [s['code'] for s in a], 'elements': elements_de(a)},
            {'code': 'B', 'titre': 'Consonnes et finales', 'series': [s['code'] for s in b], 'elements': elements_de(b)}]


# ---------------------------------------------------------------------------
# 4. Programme principal
# ---------------------------------------------------------------------------
def main():
    # --- 4.1 Lecture des données. Les dictionnaires { code: ligne } permettent de retrouver
    #         vite un mot, un son, un ton par son code.
    lecons = lire('lecons.csv')
    mots = {m['word_code']: m for m in lire('mots.csv')}
    sons = {s['sound_code']: s for s in lire('sons.csv')}
    tons = {t['tone_code']: t for t in lire('tons.csv')}
    paires = lire('paires_minimales.csv')
    toutes_voix = {v['voice_code']: v for v in lire('voix.csv')}
    voix = [v for v in toutes_voix.values() if v['status'] == 'active']
    # DEC-0077 : avertir si une voix prévue pour un usage n'est pas active dans voix.csv (elle serait ignorée).
    actives = {v['voice_code'] for v in voix}
    for usage, liste_v in list(VOIX_PAR_USAGE.items()) + [('modele', [VOIX_MODELE])]:
        for c in liste_v:
            if c not in actives:
                print(f"ATTENTION : voix {c} prévue pour « {usage} » (DEC-0077) mais inactive dans voix.csv")
    audios = lire('audios.csv')
    # images.csv est lu mais pas encore utilisé (fichier vide) : les images viennent
    # provisoirement de images_provisoires.csv (emoji).
    images = {i['word_code']: i for i in lire('images.csv')}
    images_prov = {i['word_code']: i['emoji'] for i in lire('images_provisoires.csv', LECTEUR)}
    reperes = {r['symbol']: r for r in lire('reperes_sons.csv')}   # DEC-0038
    exemples = lire('exemples_e1.csv')                              # DEC-0039
    mots_lecons = lire('mots_lecons.csv')                           # E4 : mots supports
    comptage = lire('comptage.csv')                                 # DEC-0054
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import regle_classificateurs as rc                              # DEC-0062 : même règle que l'audio
    from generer_audio_fpt import voyelle_simple                    # DEC-0070 : même règle que l'audio
    import concatener_e1 as seq_e1                                  # MOD-D25 : séquences d'écoute de l'E1
    index_seq = seq_e1.lire_index(DONNEES)
    fichiers_seq = set()
    ctx_clf = rc.charger(DONNEES)
    syllabe = {}
    for s_ in lire('syllabes.csv'):
        syllabe.setdefault(s_['word_code'], []).append(s_)
    # Courbes du modèle (DEC-0050) : fichier audio -> { 'm': médiane Hz, 'p': [demi-tons ou None] }.
    courbes = {}
    for c in lire('courbes_modele.csv'):
        courbes[c['file']] = {'m': float(c['median_hz']) if c['median_hz'] else None,
                              'p': [None if x == '_' else float(x) for x in c['points'].split()]}

    # --- 4.2 Audios utilisables : clé (référence du terme, voix, débit) -> chemin du fichier.
    # Référence = code du mot (W0057) ou, pour une syllabe sans code, son écriture (xêm).
    # Audios validés : (référence, voix, débit) -> fichier
    fichiers_audio = {}
    for a in audios:
        if a.get('validated') == 'true' or (NON_VALIDES and os.path.exists(os.path.join(DONNEES, a['file']))):
            fichiers_audio[(a['item_ref'], a['voice'], a['speed'])] = a['file']

    # --- 4.3 symbole(élément) : tout ce que le lecteur affiche pour un son ou un ton :
    #   texte      : pictogramme du ton, ou symbole phonétique entre barres (/ɛ/)
    #   categorie  : identique / proche / nouveau (marque = ≈ ★, DEC-0038)
    #   place      : debut / fin / voyelle / ton (ce qu'il faut écouter, DEC-0042)
    #   repere     : mot repère (français écrit, ou vietnamien en image) ; indication : indice d'écoute
    # S'arrête avec un message clair si un son ou un repère manque dans les données.
    def symbole(element):
        if element in tons:
            t = tons[element]
            return {'texte': t['pictogram'], 'couleur': t['color_hex'], 'nom': t['name_vi'],
                    'indication': 'ton ' + t['name_vi'] + ' : ' + t['contour_fr'], 'place': 'ton',
                    # Lettres (DEC-0063) : pour un ton, la marque d'accent (◌́), ou « sans accent ».
                    'lettres': [t['mark']] if t.get('mark') else []}
        s = sons.get(element)
        if not s:
            raise SystemExit('Élément inconnu : ' + element)
        principal = s['ipa_main']
        # Consonne finale : repère propre à la fin de mot s'il existe (« -m » : pomme), DEC-0046.
        r = reperes.get('-' + principal) if s['position'] == 'final' else None
        r = r or reperes.get(principal)
        if not r:
            raise SystemExit('Pas de repère pour le symbole /' + principal + '/ dans reperes_sons.csv')
        # Catégorie (DEC-0038) : son identique au français, proche, ou nouveau.
        categorie = {'exact': 'identique', 'proche': 'proche'}.get(r['match'], 'nouveau')
        # Place dans la syllabe (DEC-0042) : une consonne se dit en début ou en fin de mot.
        place = {'initial': 'debut', 'final': 'fin'}.get(s['position'], 'voyelle')
        # Lettres vietnamiennes du son (DEC-0063) : toutes ses graphies (spellings « d|gi|r »), sinon
        # grapheme ; une finale garde son tiret (« -m »).
        lettres = [x.strip() for x in (s.get('spellings') or s['grapheme']).split('|') if x.strip()]
        if s['position'] == 'final':
            lettres = [x if x.startswith('-') else '-' + x for x in lettres]
        return {'texte': '/' + principal + '/', 'couleur': '', 'nom': s['grapheme'], 'lettres': lettres,
                'indication': r['listening_cue'], 'categorie': categorie, 'place': place,
                'repere': {'langue': r['language'], 'mot': r['keyword'] if r['language'] == 'fr' else '',
                           'image': r['picture']},
                # Chemin de prononciation (DEC-0038), affiché en E4 : départ, un seul changement, vérification.
                'chemin': {'depart': r['start'], 'partie': r['body_part'], 'changement': r['change'],
                           'verification': r['check'], 'certitude': r['certainty']} if r.get('change') else None}

    # --- 4.4 audio(référence) : fichiers disponibles pour un terme, rangés par voix puis débit :
    #   { 'F1': { 'slow': 'audio/W0057-F1-slow.mp3', 'normal': ... }, 'H3': {...} }
    # Seules les voix actives de voix.csv sont prises. Débit lent emprunté (DEC-0067) : pour une voix
    # dont la colonne slow_from est remplie (F4 <- F1, H6 <- H4), le fichier lent est celui de cette voix.
    def audio(ref):
        res = {}
        for v in voix:
            for d in DEBITS:
                source = (v.get('slow_from') or v['voice_code']) if d == 'slow' else v['voice_code']
                f = fichiers_audio.get((ref, source, d))
                if f:
                    res.setdefault(v['voice_code'], {})[d] = f
        return res

    # --- 4.5 Regroupement des lignes de paires_minimales.csv par série (S0001, S0002…).
    series = {}
    for p in paires:
        series.setdefault(p['series_code'], []).append(p)

    # --- 4.6 Construction de chaque leçon, dans l'ordre de sort_order.
    sortie_lecons = []
    for l in sorted(lecons, key=lambda x: int(x['sort_order'])):
        code = l['lesson_code']
        liste = []
        for sc, termes in series.items():
            if termes[0]['lesson_code'] != code:
                continue
            # Termes de la série dans l'ordre des positions (1 = mot support, 2 = contraste principal).
            # groupe : 0 voyelles ou tons, 1 début, 2 finale (voir ORDRE_POSITIONS).
            termes = sorted(termes, key=lambda t: int(t['position']))
            premier = termes[0]['element']
            groupe = 0 if premier in tons else ORDRE_POSITIONS.get(sons[premier]['position'], 3)
            sortie_termes = []
            for t in termes:
                # m : le mot du corpus (None pour une syllabe sans code). Une syllabe inventée
                # n'a jamais d'image ni d'écrit affiché (R-LEX-06).
                m = mots.get(t['word_code']) if t['word_code'] else None
                invente = t['invented'] == 'true'
                image = ''
                if m and m['imageable'] == 'true' and not invente:
                    image = images_prov.get(m['word_code'], '')  # images.csv vide : emoji provisoire
                ref = t['word_code'] or t['written']
                # Pas de mot d'appui dans les séries (E2, E3, échauffement) : DEC-0061 (essai de DEC-0060
                # abandonné : « on ne sait pas trop quoi comparer »). Le mot est toujours dit seul.
                aud = audio(ref)
                appui = ''
                sortie_termes.append({
                    'position': int(t['position']),
                    'ecrit': t['written'],          # jamais affiché si invente (R-LEX-06)
                    'sens': m['meaning_fr'].split(' / ')[0] if m else '',
                    'invente': invente,
                    'element': t['element'],
                    'symbole': symbole(t['element']),
                    'image': image,
                    'audio': aud,
                    'appui': appui,                 # « hai con » : affiché avec l'écrit, lu par la synthèse
                })
            liste.append({'code': sc, 'type': termes[0]['contrast_type'], 'groupe': groupe,
                          'place': sortie_termes[0]['symbole']['place'],   # ce qu'il faut écouter (DEC-0042)
                          'termes': sortie_termes})
        # Séries triées : voyelles (ou tons), puis débuts, puis finales ; puis par code.
        liste.sort(key=lambda s: (s['groupe'], s['code']))
        # E1 « Découverte » (DEC-0039) : chaque son seul, dans 3 mots au plus, voix de femme puis d'homme.
        decouverte = {}
        # DEC-0072 : sons présentés en E1 AVANT ceux de la première partie (L01 : t puis m),
        # colonne e1_first de lecons.csv. Un son déjà dans les séries (m) garde une seule fiche.
        d_abord = (l.get('e1_first') or '').split()
        # DEC-0075 : sons déjà vus en L01, présentés en « rappel court » dans cette leçon
        # (1 mot, 1 voix de femme, pas d'écoute lente) : colonne e1_rappel de lecons.csv.
        rappel = set((l.get('e1_rappel') or '').split())
        lecon_tons = l['is_tone_lesson'] == 'true'
        for e in d_abord + [x for x in elements_de(liste) if x not in d_abord]:
            mots_e = []
            exemples_e = sorted((x for x in exemples if x['lesson_code'] == code and x['element'] == e
                                 and (x['word_code'] or x.get('syllable'))), key=lambda x: int(x['rank']))
            # DEC-0075 : rappel court : un seul mot (le rang 1), une seule voix (la femme).
            if e in rappel:
                exemples_e = exemples_e[:1]
            for x in exemples_e:
                # Voix d'E1 (DEC-0077) : leçon de tons F1 + H3 ; syllabe sans sens F1 + H4 ; mot F4 + H4.
                usage = 'tons' if lecon_tons else ('e1_mots' if x['word_code'] else 'e1_syllabe')
                voix_mot = VOIX_PAR_USAGE[usage][:1] if e in rappel else list(VOIX_PAR_USAGE[usage])
                if not x['word_code']:
                    # Syllabe sans sens (DEC-0073) : ni sens ni image, jamais écrite (R-LEX-06) ;
                    # « ecrit » ne sert qu'à la voix de synthèse et à l'audio (référence = l'écriture).
                    invente = x.get('invented') == 'true'
                    mots_e.append({'ecrit': x['syllable'], 'sens': 'syllabe inventée' if invente else 'syllabe',
                                   'image': '', 'voix': voix_mot,
                                   'audio': audio(x['syllable']), 'appui': '', 'invente': invente,
                                   'syllabe': True})   # MOD-D25 : syllabes avant les mots
                    continue
                m = mots[x['word_code']]
                # Classificateur (DEC-0062) : « con mèo » si la règle l'autorise et que l'audio existe.
                a = rc.appui(ctx_clf, x['word_code'], code, e)
                aud_clf = audio(a[1]) if a else {}
                mots_e.append({
                    'ecrit': m['written'],          # pour la voix de synthèse seulement : jamais affiché en E1 (R-ECR-01)
                    'sens': m['meaning_fr'].split(' / ')[0],
                    'image': images_prov.get(m['word_code'], '') if m['imageable'] == 'true' else '',
                    'voix': voix_mot,
                    'audio': aud_clf or audio(m['word_code']),
                    'appui': a[0].split(' ')[0] if aud_clf else '',
                })
            # Voyelle simple (DEC-0070) : la voyelle seule, jouée avant les mots (débit normal seulement).
            # Seulement si le fichier existe : la voix de synthèse de l'appareil épellerait la lettre.
            seul = None
            if e in sons and voyelle_simple(e) and not lecon_tons:
                aud_seul = {v: fd for v, fd in audio('V-' + e).items() if fd.get('normal')}
                if aud_seul:
                    voix_seul = VOIX_PAR_USAGE['e1_voyelle']   # DEC-0077 : F1 + H4
                    seul = {'ecrit': sons[e]['grapheme'], 'audio': aud_seul,
                            'voix': [x for x in voix_seul if x in aud_seul] or list(aud_seul)}
            # MOD-D25 : ordre d'écoute voyelle seule -> syllabes sans sens -> mots (tuiles dans le même ordre).
            mots_e.sort(key=lambda m: not m.get('syllabe'))
            decouverte[e] = {'element': e, 'symbole': symbole(e), 'mots': mots_e, 'seul': seul,
                             'rappel': e in rappel}  # DEC-0075
            # MOD-D25 : séquence d'écoute (un MP3 par voix), si concatener_e1.py l'a fabriquée à jour.
            sq = seq_e1.sequence_lecteur(DONNEES, code, e, decouverte[e], index_seq)
            if sq:
                decouverte[e]['sequence'] = sq
                fichiers_seq.update(p['fichier'] for c in sq.values() for p in c)
        # E4 « Écoute et répète » (DEC-0049, DEC-0050) : les mots supports de la leçon, dans
        # l'ordre de mots_lecons.csv, avec la voix modèle seule (R-AUD-03), ses deux débits et
        # la courbe mélodique de chaque fichier. Cibles = sons (ou tons) des séries dont le mot
        # est le terme 1 ; mot support hors séries : pas de cible affichée.
        production = []
        for ml in (x for x in mots_lecons if x['lesson_code'] == code):
            m = mots.get(ml['word_code'])
            if not m:
                continue
            cibles = []
            for termes in series.values():
                if termes[0]['lesson_code'] == code:
                    for t in termes:
                        if t['position'] == '1' and t['word_code'] == m['word_code'] and t['element'] not in cibles:
                            cibles.append(t['element'])
            aud = {d: f for d, f in audio(m['word_code']).get(VOIX_MODELE, {}).items()}
            # Classificateur en E4 (DEC-0062) : « con mèo » répété APRÈS le mot seul, comme un item de plus.
            a = rc.appui(ctx_clf, m['word_code'], code)
            aud_clf = {d: f for d, f in audio(a[1]).get(VOIX_MODELE, {}).items()} if a else {}
            suite = None
            if aud_clf:
                suite = {
                    'code': m['word_code'] + '+clf', 'ecrit': a[0], 'sens': m['meaning_fr'].split(' / ')[0],
                    'image': images_prov.get(m['word_code'], '') if m['imageable'] == 'true' else '',
                    'cibles': [symbole(e) for e in cibles], 'audio': {VOIX_MODELE: aud_clf},
                    'courbes': {d: courbes[f] for d, f in aud_clf.items() if f in courbes},
                    'avec_classificateur': True,
                }
            production.append({
                'code': m['word_code'],
                'ecrit': m['written'],
                'sens': m['meaning_fr'].split(' / ')[0],
                'image': images_prov.get(m['word_code'], '') if m['imageable'] == 'true' else '',
                'cibles': [symbole(e) for e in cibles],
                'audio': {VOIX_MODELE: aud} if aud else {},
                'courbes': {d: courbes[f] for d, f in aud.items() if f in courbes},
            })
            if suite:
                production.append(suite)
        # « Combien de fois ? » (DEC-0054) : chaque suite, rattachée à la partie qui contient sa
        # cible ; pour chaque mot, « cible » dit s'il contient le son ou le ton à compter.
        sections = parties(liste, l.get('split_parts') == 'true')
        # Liste des sons d'E1 de chaque partie (DEC-0072) : les sons « d'abord » en tête de la
        # première partie. « elements » (séries, « Combien de fois ? », verrous) ne change pas.
        for k, pa in enumerate(sections):
            pa['e1'] = (d_abord + [e for e in pa['elements'] if e not in d_abord]) if k == 0 else list(pa['elements'])
        combien = []
        for x in (c for c in comptage if c['lesson_code'] == code):
            e = x['element']
            pc = next((pa['code'] for pa in sections if e in pa['elements']), None)
            if not pc:
                continue
            mots_x = []    # une case par SYLLABE (un mot de 2 syllabes peut contenir 2 cibles)
            for w in x['word_codes'].split():
                for sy in sorted(syllabe.get(w, []), key=lambda s: int(s['position'])):
                    els = [sy[k] for k in ('initial', 'glide', 'nucleus', 'final', 'tone') if sy.get(k)]
                    mots_x.append({'ecrit': sy['written'], 'cible': e in els})
            combien.append({'code': x['item_code'], 'element': e, 'partie': pc, 'symbole': symbole(e),
                            'ecrit': x['written'], 'mots': mots_x, 'nombre': int(x['count']),
                            'nature': x['kind'], 'sens': x['note'] if x['kind'] == 'phrase' else '',
                            'audio': audio(x['item_code'])})
        # Ce que reçoit le lecteur pour une leçon (voir le « vocabulaire » en tête de lecteur.js).
        sortie_lecons.append({
            'code': code,
            'numero': int(l['sort_order']),
            'titre': l['family_fr'],
            'seuil': float(l['listen_threshold']),
            'tons': l['is_tone_lesson'] == 'true',
            'recyclage': l['is_recycling'] == 'true',
            'series': liste,
            'parties': sections,
            'combien': combien,
            'decouverte': decouverte,
            'e1_first': d_abord,            # DEC-0072 : sons présentés avant la première partie
            'production': production,
            # Voix d'écoute de la leçon (DEC-0055) : E2, E3, échauffement, « Combien de fois ? ».
            'voix': [v['voice_code'] for v in voix
                     if v.get('listen_tones' if l['is_tone_lesson'] == 'true' else 'listen_sounds', 'true') == 'true'],
            # Voix de « Combien de fois ? » et des phrases espacées (DEC-0077) : F1 + H3, voix actives seulement.
            'voix_combien': [c for c in VOIX_PAR_USAGE['combien'] if c in actives],
        })

    # --- 4.6 bis Page « Les 6 tons » (DEC-0052) : pour chaque ton, la syllabe de la série, son
    # ton (pictogramme, couleur, contour), ses audios et ses courbes par voix et par débit.
    reference_tons = []
    for x in lire('reference_tons.csv'):
        t = tons.get(x['tone_code'])
        if not t:
            continue
        aud = audio(x['word_code'] or x['written'])
        reference_tons.append({
            # Série (DEC-0064) : ma, bi, hai… ; libellé (a, ai, -t), nature (voyelle, diphtongue…).
            'serie': x.get('series') or 'ma', 'libelle': x.get('label') or 'a', 'nature': x.get('kind') or 'voyelle',
            'invente': x.get('invented') == 'true',
            'ton': x['tone_code'], 'nom': t['name_vi'], 'pictogramme': t['pictogram'], 'couleur': t['color_hex'],
            'contour': t['contour_fr'], 'chao': t['chao'], 'glottal': t['glottalization'],
            'ecrit': x['written'], 'sens': x['meaning_fr'],
            'audio': aud,
            'courbes': {v: {d: courbes[f] for d, f in fd.items() if f in courbes} for v, fd in aud.items()},
        })

    # --- 4.7 Le contenu complet de donnees.js.
    def lent(v):     # voix qui fournit le débit lent de v (elle-même, ou slow_from, DEC-0067)
        return toutes_voix.get(v.get('slow_from') or '', v)

    donnees = {
        'genere_le': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'parametres': PARAMETRES,
        # Pour chaque voix : code, genre, réglages de la synthèse provisoire, et (mode test,
        # DEC-0047) le nom du personnage, l'identifiant et le modèle FPT, la valeur speed par débit.
        'voix': [{'code': v['voice_code'], 'genre': v['gender'], **VOIX_PROVISOIRES.get(v['voice_code'], {}),
                  'nom': nom_personnage(v), 'voix_fpt': v.get('provider_voice', ''),
                  'modele': v.get('provider_model', ''),
                  'vitesse_fpt': {'slow': float(lent(v).get('provider_speed_slow') or 0.8), 'normal': 1.0, 'spaced': 1.0},
                  # Mode test (DEC-0047) : d'où vient le débit lent (DEC-0067).
                  'lent': {'code': lent(v)['voice_code'], 'voix_fpt': lent(v).get('provider_voice', ''),
                           'modele': lent(v).get('provider_model', '')}}
                 for v in voix],
        'voix_modele': VOIX_MODELE,
        'voix_reference_tons': [c for c in VOIX_REFERENCE_TONS if any(v['voice_code'] == c for v in voix)],
        'debits': DEBITS,
        # « ⚑ Signaler un son » (DEC-0069) : version de chaque fichier = sa date (même calcul que
        # valider_audios.py), pour qu'un signalement ne touche pas un audio refait depuis.
        'versions': {f: str(int(os.path.getmtime(os.path.join(DONNEES, f))))
                     for f in set(fichiers_audio.values()) if os.path.exists(os.path.join(DONNEES, f))},
        'lecons': sortie_lecons,
        'reference_tons': reference_tons,
    }

    # --- 4.8 Écriture des fichiers dans 06_LIVRABLES/lecteur/.
    os.makedirs(SORTIE, exist_ok=True)
    js = 'window.DONNEES_LECTEUR = ' + json.dumps(donnees, ensure_ascii=False, indent=1) + ';\n'
    with open(os.path.join(SORTIE, 'donnees.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
    for nom in ['index.html', 'lecteur.css', 'prononciation.js', 'lecteur.js']:
        shutil.copyfile(os.path.join(LECTEUR, nom), os.path.join(SORTIE, nom))
    # Audios validés copiés à côté du lecteur (et séquences d'E1, MOD-D25)
    for f in set(fichiers_audio.values()) | fichiers_seq:
        src = os.path.join(DONNEES, f)
        dst = os.path.join(SORTIE, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)

    # --- 4.9 lecteur_autonome.html : la page dans laquelle on REMPLACE mot pour mot les trois
    # lignes qui chargent lecteur.css, donnees.js et lecteur.js par leur contenu.
    # Si ces lignes changent dans index.html, il faut changer les trois replace() ci-dessous.
    # Version en un seul fichier
    with open(os.path.join(LECTEUR, 'index.html'), encoding='utf-8') as f:
        page = f.read()
    with open(os.path.join(LECTEUR, 'lecteur.css'), encoding='utf-8') as f:
        css = f.read()
    with open(os.path.join(LECTEUR, 'lecteur.js'), encoding='utf-8') as f:
        code = f.read()
    page = page.replace('<link rel="stylesheet" href="lecteur.css">', '<style>\n' + css + '\n</style>')
    page = page.replace('<script src="donnees.js"></script>', '<script>\n' + js + '</script>')
    with open(os.path.join(LECTEUR, 'prononciation.js'), encoding='utf-8') as f:
        prono = f.read()
    page = page.replace('<script src="prononciation.js"></script>', '<script>\n' + prono + '\n</script>')
    page = page.replace('<script src="lecteur.js"></script>', '<script>\n' + code + '\n</script>')
    with open(os.path.join(SORTIE, 'lecteur_autonome.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)

    # --- 4.10 Bilan affiché dans PowerShell.
    nb_series = sum(len(l['series']) for l in sortie_lecons)
    print(f"{len(sortie_lecons)} leçons, {nb_series} séries, {len(fichiers_audio)} audios "
          f"{'(validés ou non : ESSAI)' if NON_VALIDES else 'validés'} -> {SORTIE}")
    nb_seq = sum(1 for l in sortie_lecons for d in l['decouverte'].values() if d.get('sequence'))
    nb_e1 = sum(len(l['decouverte']) for l in sortie_lecons)
    print(f"E1 : {nb_seq} / {nb_e1} sons avec séquence d'écoute ({len(fichiers_seq)} fichiers, MOD-D25)")
    nb_c = sum(len(l['combien']) for l in sortie_lecons)
    nb_c_audio = sum(1 for l in sortie_lecons for x in l['combien'] if x['audio'])
    print(f"« Combien de fois ? » : {nb_c} suites, dont {nb_c_audio} avec audio")
    nb_e4 = sum(len(l['production']) for l in sortie_lecons)
    nb_courbes = sum(len(p['courbes']) for l in sortie_lecons for p in l['production'])
    for v_ref in VOIX_REFERENCE_TONS:   # DEC-0077 : F1 et H3
        nb_ref = sum(1 for x in reference_tons if x['courbes'].get(v_ref, {}).get('normal'))
        print(f"Page « Les 6 tons » : {nb_ref} / {len(reference_tons)} tons avec audio et courbe ({v_ref})")
    print(f"E4 : {nb_e4} mots supports, {nb_courbes} courbes du modèle"
          f"{'' if courbes else ' (courbes_modele.csv absent : lancer courbes_modele.py)'}")


# Lancement quand le fichier est exécuté directement (et non importé par un autre script).
if __name__ == '__main__':
    main()
