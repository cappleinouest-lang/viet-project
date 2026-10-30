# -*- coding: utf-8 -*-
"""
ABANDONNÉ (DEC-0061, 2026-10-30) : le mot d'appui gêne la comparaison en E2–E3. Script gardé pour
l'historique ; appuis_series.csv n'est plus lu. Les classificateurs servent en E1, E4, E5 (mots.csv).

Choisit les séries minimales dont les termes sont dits avec un MOT D'APPUI « chiffre + classificateur »
(« hai con mèo / hai con mè ») et écrit 04_DONNEES/appuis_series.csv (DEC-0060).

Pourquoi : le mot étudié ne commence plus l'énoncé ; sa consonne de début est mieux prononcée par
la synthèse (essai du 2026-10-30, tester_appui.py : Thu Minh 48 -> 94 ms, Huy Phong 46 -> 59 ms).

Une série est retenue seulement si :
  - tous ses mots RÉELS sont des noms (mots.csv, category = NOUN) ;
  - ils ont tous le MÊME classificateur (mots.csv, colonne classifier) ; les syllabes inventées de
    la série reçoivent le même appui (seule la cible doit changer d'un terme à l'autre) ;
  - le ton du classificateur est déjà ouvert à l'écoute dans la leçon (règle souple, DEC-0056) ;
  - leçon de tons : seulement si le classificateur est au ton ngang (un autre ton placé juste
    avant gênerait l'écoute du ton étudié).
Le chiffre est « hai » (ton ngang).

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\choisir_appuis.py . --lecons M0-L04,M0-L05     (essai)
    python 05_PRODUCTION\\tools\\choisir_appuis.py .                            (toutes les leçons)
"""
import csv
import os
import sys

CHIFFRE = 'hai'
COLONNES = ['series_code', 'lesson_code', 'carrier', 'classifier', 'note']
TONS_MARQUES = {'\u0301': 'sac', '\u0300': 'huyen', '\u0309': 'hoi', '\u0303': 'nga', '\u0323': 'nang'}


def lire(dossier, nom):
    with open(os.path.join(dossier, nom), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def ton_de(ecrit):
    import unicodedata
    for c in unicodedata.normalize('NFD', ecrit):
        if c in TONS_MARQUES:
            return TONS_MARQUES[c]
    return 'ngang'


def main():
    racine = next((a for a in sys.argv[1:] if not a.startswith('--')), '.')
    donnees = os.path.join(racine, '04_DONNEES')
    limite = sys.argv[sys.argv.index('--lecons') + 1].split(',') if '--lecons' in sys.argv else None
    lecons = {l['lesson_code']: l for l in lire(donnees, 'lecons.csv')}
    rang = {c: int(l['sort_order']) for c, l in lecons.items()}
    ouv = {o['element_code']: rang.get(o['listen_lesson'], 99) for o in lire(donnees, 'ouvertures.csv')}
    mots = {m['word_code']: m for m in lire(donnees, 'mots.csv')}
    clfs = {c['classifier_code']: c for c in lire(donnees, 'classificateurs.csv')}
    series = {}
    for p in lire(donnees, 'paires_minimales.csv'):
        series.setdefault(p['series_code'], []).append(p)

    lignes, ecartees = [], []
    for sc, termes in sorted(series.items()):
        code = termes[0]['lesson_code']
        if limite and code not in limite:
            continue
        reels = [t for t in termes if t['word_code'] and t['invented'] != 'true']
        if not reels or any(mots[t['word_code']]['category'] != 'NOUN' for t in reels):
            continue
        c = {mots[t['word_code']].get('classifier', '') for t in reels}
        if len(c) != 1 or '' in c:
            continue
        c = c.pop()
        ecrit = clfs[c]['written']
        ton = ton_de(ecrit)
        if ouv.get(ton, 99) > rang[code]:
            ecartees.append(f'{sc} ({code}) : ton {ton} de « {ecrit} » pas encore ouvert')
            continue
        if lecons[code]['is_tone_lesson'] == 'true' and ton != 'ngang':
            ecartees.append(f'{sc} ({code}) : leçon de tons et « {ecrit} » n’est pas au ton ngang')
            continue
        lignes.append({'series_code': sc, 'lesson_code': code, 'carrier': f'{CHIFFRE} {ecrit}', 'classifier': c,
                       'note': ' / '.join(t['written'] for t in sorted(termes, key=lambda t: int(t['position'])))})
    chemin = os.path.join(donnees, 'appuis_series.csv')
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(lignes)
    for x in lignes:
        print(f"  {x['series_code']} {x['lesson_code']} : {x['carrier']} + ({x['note']})")
    for e in ecartees:
        print('  écartée :', e)
    print(f'{len(lignes)} série(s) avec appui. Écrit : {chemin}')


if __name__ == '__main__':
    main()
