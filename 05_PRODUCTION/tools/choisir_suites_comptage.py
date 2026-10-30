# -*- coding: utf-8 -*-
"""
Compose les items de l'exercice « Combien de fois ? » (fin d'E3, DEC-0054) et écrit
04_DONNEES/comptage.csv.

Un item = une SUITE de mots connus, dite d'affilée (« ba, mẹ, ma, bé »), et un son ou un ton
CIBLE de la leçon ; l'apprenant dit combien de fois il entend la cible. Plus tard, de vraies
petites phrases s'ajouteront (colonne kind = phrase), saisies à la main dans le même fichier.

Règles appliquées :
  - atomicité stricte : seuls des mots du corpus d'UNE syllabe dont TOUS les éléments (début,
    voyelle, finale, ton) sont ouverts à l'écoute au plus tard dans la leçon (ouvertures.csv) ;
  - le NOMBRE ATTENDU est CALCULÉ à partir de syllabes.csv (jamais compté à la main) ;
  - les autres mots de la suite sont pris d'abord parmi ceux qui portent un élément PROCHE
    (les autres termes des séries de la cible), pour que l'écoute soit réellement exigeante ;
  - pas deux fois le même mot à la suite ; tirage reproductible (graine fixe).

Le fichier produit peut être corrigé à la main ; relancer ce script le RÉÉCRIT, sauf les lignes
kind = phrase (gardées telles quelles). --verifier : compare sans écrire.

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\choisir_suites_comptage.py .
    python 05_PRODUCTION\\tools\\choisir_suites_comptage.py . --verifier
"""
import csv
import os
import random
import sys

NB_SUITES = 4                     # suites par élément cible
COMPTES = [1, 2, 3, 2]            # nombre de cibles voulu pour chaque suite (dans l'ordre)
LONGUEURS = [3, 4, 4, 5]          # nombre de mots de chaque suite
GRAINE = 20261030
COLONNES = ['item_code', 'lesson_code', 'element', 'kind', 'word_codes', 'written', 'count',
            'validated', 'note']
PLACES = ['initial', 'glide', 'nucleus', 'final', 'tone']


def lire(dossier, nom):
    chemin = os.path.join(dossier, nom)
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def elements_du_mot(s):
    return [s[p] for p in PLACES if s.get(p)]


def compter(element, mots, syllabe):
    """Nombre de mots de la suite qui contiennent l'élément (calcul, jamais à la main)."""
    return sum(1 for w in mots if element in elements_du_mot(syllabe[w]))


def composer(donnees):
    lecons = sorted(lire(donnees, 'lecons.csv'), key=lambda l: int(l['sort_order']))
    rang = {l['lesson_code']: int(l['sort_order']) for l in lecons}
    ouv = {o['element_code']: rang.get(o['listen_lesson'], 99) for o in lire(donnees, 'ouvertures.csv')}
    mots = {m['word_code']: m for m in lire(donnees, 'mots.csv')}
    par_mot = {}
    for s in lire(donnees, 'syllabes.csv'):
        par_mot.setdefault(s['word_code'], []).append(s)
    syllabe = {w: s[0] for w, s in par_mot.items() if len(s) == 1 and w in mots}
    paires = lire(donnees, 'paires_minimales.csv')
    series = {}
    for p in paires:
        series.setdefault(p['series_code'], []).append(p)

    def ouvert_avant(w, r):
        return all(ouv.get(e, 99) <= r for e in elements_du_mot(syllabe[w]))

    lignes, absents = [], []
    for l in lecons:
        code, r = l['lesson_code'], int(l['sort_order'])
        reserve = sorted(w for w in syllabe if ouvert_avant(w, r))
        cibles = []
        for p in paires:
            if p['lesson_code'] == code and p['element'] not in cibles:
                cibles.append(p['element'])
        for e in cibles:
            alea = random.Random(f'{GRAINE}-{code}-{e}')
            avec = [w for w in reserve if e in elements_du_mot(syllabe[w])]
            if not avec:
                absents.append(f'{code} {e}')
                continue
            proches_el = {t['element'] for s in series.values() if s[0]['lesson_code'] == code
                          and any(t['element'] == e for t in s) for t in s} - {e}
            sans = [w for w in reserve if e not in elements_du_mot(syllabe[w])]
            proches = [w for w in sans if proches_el & set(elements_du_mot(syllabe[w]))]
            for k in range(NB_SUITES):
                n, longueur = COMPTES[k % len(COMPTES)], LONGUEURS[k % len(LONGUEURS)]
                n = min(n, longueur - 1) if sans else longueur
                choix = [alea.choice(avec) for _ in range(n)]
                for _ in range(longueur - n):
                    source = proches if proches and alea.random() < 0.6 else sans
                    choix.append(alea.choice(source) if source else alea.choice(avec))
                # ordre au hasard, sans deux fois le même mot de suite
                for _ in range(50):
                    alea.shuffle(choix)
                    if all(choix[i] != choix[i + 1] for i in range(len(choix) - 1)):
                        break
                lignes.append({
                    'item_code': f'C-{code[-3:]}-{e}-{k + 1}',
                    'lesson_code': code, 'element': e, 'kind': 'suite',
                    'word_codes': ' '.join(choix),
                    'written': ', '.join(mots[w]['written'] for w in choix),
                    'count': str(compter(e, choix, syllabe)),
                    'validated': 'false', 'note': '',
                })
    return lignes, absents


def main():
    racine = next((a for a in sys.argv[1:] if not a.startswith('--')), '.')
    donnees = os.path.join(racine, '04_DONNEES')
    chemin = os.path.join(donnees, 'comptage.csv')
    lignes, absents = composer(donnees)
    phrases = [x for x in lire(donnees, 'comptage.csv') if x.get('kind') == 'phrase']
    print(f'{len(lignes)} suites ; {len(phrases)} phrase(s) gardée(s) ; '
          f'{len(absents)} cible(s) sans mot utilisable : ' + (', '.join(absents) or 'aucune'))
    if '--verifier' in sys.argv:
        return
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(lignes + phrases)
    print('Écrit :', chemin)


if __name__ == '__main__':
    main()
