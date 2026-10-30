# -*- coding: utf-8 -*-
"""
Choisit les mots d'exemple de l'étape E1 « Découverte » (DEC-0039) et écrit 04_DONNEES/exemples_e1.csv.

Pour chaque leçon et chaque son (ou ton) de ses séries minimales, au plus NB_MOTS mots :
  - mots du corpus (word_code), d'une seule syllabe, contenant le son à sa place
    (début, voyelle, finale) ou portant le ton ;
  - règle souple : le TON du mot doit être déjà ouvert à l'écoute (ouvertures.csv) ;
    les autres sons du mot sont libres ;
  - d'abord le mot support de la série (s'il convient), puis des mots dont le début varie
    (ou, pour un son de début, dont la voyelle varie), du plus fréquent au moins fréquent ;
  - chaque mot reçoit une voix de femme et une voix d'homme, prises parmi les voix d'écoute du
    type de leçon (voix.csv, colonnes listen_sounds / listen_tones, DEC-0055), en alternance.

Le fichier produit peut ensuite être corrigé à la main : relancer ce script le RÉÉCRIT
(utiliser --verifier pour seulement comparer, sans écrire).

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\choisir_exemples_e1.py .
    python 05_PRODUCTION\\tools\\choisir_exemples_e1.py . --verifier
"""
import csv
import os
import sys

NB_MOTS = 3
COLONNES = ['lesson_code', 'element', 'rank', 'word_code', 'voice_f', 'voice_h', 'note']
PLACES = ['initial', 'glide', 'nucleus', 'final']


def lire(dossier, nom):
    with open(os.path.join(dossier, nom), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def choisir(donnees):
    lecons = sorted(lire(donnees, 'lecons.csv'), key=lambda l: int(l['sort_order']))
    rang_lecon = {l['lesson_code']: int(l['sort_order']) for l in lecons}
    ouv = {o['element_code']: rang_lecon.get(o['listen_lesson'], 99) for o in lire(donnees, 'ouvertures.csv')}
    tons = {t['tone_code'] for t in lire(donnees, 'tons.csv')}
    mots = {m['word_code']: m for m in lire(donnees, 'mots.csv')}
    syl = {}
    for s in lire(donnees, 'syllabes.csv'):
        syl.setdefault(s['word_code'], []).append(s)
    monosyllabes = {w: s[0] for w, s in syl.items() if len(s) == 1 and w in mots}
    paires = lire(donnees, 'paires_minimales.csv')
    # Voix d'écoute par type de leçon (DEC-0055) : femmes et hommes, alternés d'un mot à l'autre.
    voix = [v for v in lire(donnees, 'voix.csv') if v['status'] == 'active']
    def voix_de(tons):
        col = 'listen_tones' if tons else 'listen_sounds'
        f = [v['voice_code'] for v in voix if v.get(col) == 'true' and v['gender'] == 'female']
        h = [v['voice_code'] for v in voix if v.get(col) == 'true' and v['gender'] == 'male']
        return f or ['F1'], h or ['H3']

    def frequence(w):
        r = mots[w].get('frequency_rank') or ''
        return int(r) if r.isdigit() else 99999

    lignes = []
    for l in lecons:
        code, rang = l['lesson_code'], int(l['sort_order'])
        femmes, hommes = voix_de(l['is_tone_lesson'] == 'true')
        series = [p for p in paires if p['lesson_code'] == code]
        elements = []
        for p in series:
            if p['element'] not in elements:
                elements.append(p['element'])
        for e in elements:
            est_ton = e in tons
            place = None
            if not est_ton:
                place = next((k for k in PLACES for s in monosyllabes.values() if s[k] == e), None)

            def convient(w):
                s = monosyllabes[w]
                if ouv.get(s['tone'], 99) > rang:          # règle souple : le ton doit être déjà vu
                    return False
                return s['tone'] == e if est_ton else s.get(place) == e

            candidats = sorted((w for w in monosyllabes if convient(w)), key=frequence)
            supports = [p['word_code'] for p in series if p['element'] == e and p['word_code']]
            supports += [p['word_code'] for p in series if p['position'] == '1' and p['word_code']]
            choisis = []
            for w in supports:
                if w in candidats and w not in choisis and len(choisis) < 1:
                    choisis.append(w)
            # variété : début différent (voyelle différente pour un son de début, voyelle + début pour un ton)
            cle = (lambda w: monosyllabes[w]['nucleus']) if place == 'initial' else \
                  (lambda w: (monosyllabes[w]['initial'], monosyllabes[w]['nucleus'])) if est_ton else \
                  (lambda w: monosyllabes[w]['initial'])
            for w in candidats:
                if len(choisis) >= NB_MOTS:
                    break
                if w not in choisis and cle(w) not in {cle(c) for c in choisis}:
                    choisis.append(w)
            for w in candidats:                              # complète si la variété ne suffit pas
                if len(choisis) >= NB_MOTS:
                    break
                if w not in choisis:
                    choisis.append(w)
            if not choisis:
                lignes.append({'lesson_code': code, 'element': e, 'rank': '', 'word_code': '',
                               'voice_f': '', 'voice_h': '', 'note': 'aucun mot du corpus ne convient'})
            for i, w in enumerate(choisis):
                f, h = femmes[i % len(femmes)], hommes[i % len(hommes)]
                lignes.append({'lesson_code': code, 'element': e, 'rank': str(i + 1), 'word_code': w,
                               'voice_f': f, 'voice_h': h, 'note': mots[w]['written']})
    return lignes


def main():
    racine = next((a for a in sys.argv[1:] if not a.startswith('--')), '.')
    donnees = os.path.join(racine, '04_DONNEES')
    lignes = choisir(donnees)
    chemin = os.path.join(donnees, 'exemples_e1.csv')
    vides = [l for l in lignes if not l['word_code']]
    print(f"{len(lignes) - len(vides)} mots d'exemple pour {len({(l['lesson_code'], l['element']) for l in lignes})} sons ; "
          f"{len(vides)} son(s) sans mot : " + ', '.join(f"{l['lesson_code']} {l['element']}" for l in vides))
    if '--verifier' in sys.argv:
        actuel = lire(donnees, 'exemples_e1.csv') if os.path.exists(chemin) else []
        cles = lambda ls: {(l['lesson_code'], l['element'], l['word_code']) for l in ls}
        print('Différences avec le fichier actuel :', len(cles(lignes) ^ cles(actuel)))
        return
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(lignes)
    print('Écrit :', chemin)


if __name__ == '__main__':
    main()
