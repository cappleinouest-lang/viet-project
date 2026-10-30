# -*- coding: utf-8 -*-
"""
Règle commune : quand un nom est-il dit avec son classificateur (« con mèo ») ? (DEC-0061, DEC-0062)

Utilisée par generer_audio_fpt.py (quels audios produire) et generer_lecteur.py (quels audios jouer),
pour qu'ils appliquent exactement la même règle. Bibliothèque standard seulement.

Un nom W, dans la leçon L, est dit « classificateur + nom » si :
  1. mots.csv donne un classificateur à W (colonne classifier) ;
  2. le TON du classificateur est déjà ouvert à l'écoute dans L (règle souple, DEC-0056) ;
  3. si L est une leçon de tons : le classificateur est au ton ngang (un autre ton placé juste
     avant le nom gênerait l'écoute du ton étudié) ;
  4. si une CIBLE est donnée (écran d'E1 d'un son ou d'un ton) : le classificateur ne contient pas
     lui-même cette cible (sinon on l'entendrait deux fois sans le savoir : pas de « con » pour o, -n).
Audio correspondant : référence K-<code du mot> (« con mèo »), dans audios.csv.
"""
import csv
import os
import unicodedata

TONS = {'́': 'sac', '̀': 'huyen', '̉': 'hoi', '̃': 'nga', '̣': 'nang'}
PLACES = ('initial', 'glide', 'nucleus', 'final', 'tone')


def _lire(donnees, nom):
    chemin = os.path.join(donnees, nom)
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def _ton(ecrit):
    for c in unicodedata.normalize('NFD', ecrit):
        if c in TONS:
            return TONS[c]
    return 'ngang'


def charger(donnees):
    """Prépare ce dont la règle a besoin (à appeler une fois)."""
    lecons = {l['lesson_code']: l for l in _lire(donnees, 'lecons.csv')}
    rang = {c: int(l['sort_order']) for c, l in lecons.items()}
    mots = {m['word_code']: m for m in _lire(donnees, 'mots.csv')}
    par_ecrit = {}
    for s in _lire(donnees, 'syllabes.csv'):
        w = s['word_code']
        if w in mots and len([x for x in mots[w]['written'].split()]) == 1:
            par_ecrit.setdefault(mots[w]['written'].lower(), s)
    return {
        'rang': rang,
        'tons_lecon': {c for c, l in lecons.items() if l['is_tone_lesson'] == 'true'},
        'ouv': {o['element_code']: rang.get(o['listen_lesson'], 99) for o in _lire(donnees, 'ouvertures.csv')},
        'mots': mots,
        'clf': {c['classifier_code']: c['written'] for c in _lire(donnees, 'classificateurs.csv')},
        'syllabe': par_ecrit,     # décomposition des classificateurs présents dans le corpus (con, cái…)
    }


def appui(ctx, mot, lecon, cible=None):
    """Renvoie (texte « con mèo », référence audio « K-W0139 ») ou None si le nom reste seul."""
    m = ctx['mots'].get(mot)
    if not m or not m.get('classifier'):
        return None
    clf = ctx['clf'].get(m['classifier'])
    if not clf:
        return None
    s = ctx['syllabe'].get(clf.lower())
    ton = s['tone'] if s and s.get('tone') else _ton(clf)
    if ctx['ouv'].get(ton, 99) > ctx['rang'].get(lecon, 0):
        return None
    if lecon in ctx['tons_lecon'] and ton != 'ngang':
        return None
    if cible:
        elements = [s[p] for p in PLACES if s and s.get(p)] if s else [ton]
        if cible in elements:
            return None
    return f"{clf} {m['written']}", f"K-{mot}"
