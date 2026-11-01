# -*- coding: utf-8 -*-
"""
Choisit les mots d'exemple de l'étape E1 « Découverte » (DEC-0039, DEC-0072) et écrit
04_DONNEES/exemples_e1.csv.

Pour chaque leçon et chaque son (ou ton) de ses séries minimales, au plus NB_MOTS mots du corpus
(word_code), d'une seule syllabe, contenant le son à sa place (début, voyelle, finale) ou portant
le ton. Dans tous les cas, le TON du mot doit être déjà ouvert à l'écoute (ouvertures.csv).

Règle de préférence (DEC-0072, point 4) : les mots sont rangés en trois niveaux et pris dans cet
ordre ; on ne passe au niveau suivant que s'il manque des mots.
  niveau 0 : tous les sons du mot sont DÉJÀ VUS : ouverts dans une leçon précédente, ou consonnes
             « d'abord » de la leçon (colonne e1_first de lecons.csv), ou, en partie B d'une leçon
             en deux parties, sons de la partie A ; plus le son étudié lui-même ;
  niveau 1 : les autres sons du mot appartiennent à la leçon elle-même ;
  niveau 2 : règle souple de DEC-0039 (autres sons libres).
Dans un niveau : d'abord le mot support de la série (s'il convient), puis des mots dont le début
varie (la voyelle, pour un son de début), du plus fréquent au moins fréquent.

Consonnes « d'abord » (DEC-0072, points 1 à 3 ; colonne e1_first de lecons.csv, « PH-CO-t PH-IN-m »
pour L01) : présentées en E1 avant les sons de la première partie. Leurs mots : la consonne + une
voyelle, sans finale, au ton déjà ouvert ; d'abord les voyelles de la première partie (les mêmes
syllabes que les mots d'exemple des voyelles). Et pour une leçon qui en a, les sons de la première
partie ne prennent que des mots du niveau 0 (DEC-0072, point 2 : t/m + voyelle seulement).

Syllabes sans sens (DEC-0073) : quand les mots du corpus donnent moins de MIN_EXEMPLES exemples, on
complète avec des syllabes de 04_DONNEES/syllabes_e1.csv faites seulement de sons déjà vus (niveau 0),
au ton déjà ouvert : d'abord les syllabes réelles (invented = false, au moins 2 dictionnaires sur 3,
DEC-0027), puis les syllabes inventées. Elles n'ont ni sens ni image et ne sont jamais écrites
(R-LEX-06) ; dans exemples_e1.csv : word_code vide, colonnes syllable et invented remplies.

Chaque mot reçoit une voix de femme et une voix d'homme, prises parmi les voix d'écoute du type de
leçon (voix.csv, colonnes listen_sounds / listen_tones, DEC-0055), en alternance.

Le fichier produit peut ensuite être corrigé à la main : relancer ce script le RÉÉCRIT
(utiliser --verifier pour seulement comparer, sans écrire ; le détail des changements est affiché).

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\choisir_exemples_e1.py . --verifier
    python 05_PRODUCTION\\tools\\choisir_exemples_e1.py .
"""
import csv
import os
import sys

NB_MOTS = 3
MIN_EXEMPLES = 2                         # DEC-0073 : en dessous, on complète avec des syllabes sans sens
COLONNES = ['lesson_code', 'element', 'rank', 'word_code', 'voice_f', 'voice_h', 'note', 'syllable', 'invented']
PLACES = ['initial', 'glide', 'nucleus', 'final']
GROUPE_A = ('nucleus', 'glide')          # partie A d'une leçon en deux parties : voyelles (DEC-0037)


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
    # Syllabes sans sens (DEC-0073), rangées sous une clé « S:<écrit> » à côté des mots.
    chemin_syl = os.path.join(donnees, 'syllabes_e1.csv')
    sans_sens = {'S:' + x['written']: x for x in (lire(donnees, 'syllabes_e1.csv') if os.path.exists(chemin_syl) else [])}
    decomp = dict(monosyllabes, **sans_sens)                        # mot ou syllabe -> décomposition
    paires = lire(donnees, 'paires_minimales.csv')
    # Voix d'écoute par type de leçon (DEC-0055) : femmes et hommes, alternés d'un mot à l'autre.
    voix = [v for v in lire(donnees, 'voix.csv') if v['status'] == 'active']

    def voix_de(lecon_de_tons):
        col = 'listen_tones' if lecon_de_tons else 'listen_sounds'
        f = [v['voice_code'] for v in voix if v.get(col) == 'true' and v['gender'] == 'female']
        h = [v['voice_code'] for v in voix if v.get(col) == 'true' and v['gender'] == 'male']
        return f or ['F4'], h or ['H6']

    def frequence(w):
        r = mots[w].get('frequency_rank') or ''
        return int(r) if r.isdigit() else 99999

    def place_de(e):
        """Place d'un son dans la syllabe (initial, glide, nucleus, final), d'après le corpus."""
        return next((k for k in PLACES for s in monosyllabes.values() if s[k] == e), None)

    def sons_du_mot(w):
        s = decomp[w]
        return {s.get(k) for k in PLACES if s.get(k)}

    def ton_ouvert(w, rang):
        return ouv.get(decomp[w]['tone'], 99) <= rang                # règle souple : le ton doit être déjà vu

    def ajouter(lignes, code, e, choisis, femmes, hommes):
        if not choisis:
            lignes.append({'lesson_code': code, 'element': e, 'rank': '', 'word_code': '',
                           'voice_f': '', 'voice_h': '', 'note': 'aucun mot du corpus ne convient'})
        for i, w in enumerate(choisis):
            syl_x = sans_sens.get(w)
            lignes.append({'lesson_code': code, 'element': e, 'rank': str(i + 1),
                           'word_code': '' if syl_x else w,
                           'voice_f': femmes[i % len(femmes)], 'voice_h': hommes[i % len(hommes)],
                           'note': (('syllabe inventée ' if syl_x['invented'] == 'true' else 'syllabe hors corpus ')
                                    + syl_x['written']) if syl_x else mots[w]['written'],
                           'syllable': syl_x['written'] if syl_x else '',
                           'invented': syl_x['invented'] if syl_x else ''})

    def prendre(candidats, cle, choisis, supports=()):
        """Complète « choisis » (au plus NB_MOTS) : support d'abord, puis variété selon « cle », puis le reste."""
        for w in supports:
            if w in candidats and w not in choisis and len(choisis) < NB_MOTS and not any(c in supports for c in choisis):
                choisis.append(w)
        for w in candidats:
            if len(choisis) >= NB_MOTS:
                break
            if w not in choisis and cle(w) not in {cle(c) for c in choisis}:
                choisis.append(w)
        for w in candidats:
            if len(choisis) >= NB_MOTS:
                break
            if w not in choisis:
                choisis.append(w)

    lignes = []
    for l in lecons:
        code, rang = l['lesson_code'], int(l['sort_order'])
        femmes, hommes = voix_de(l['is_tone_lesson'] == 'true')
        series = [p for p in paires if p['lesson_code'] == code]
        elements = []
        for p in series:
            if p['element'] not in elements:
                elements.append(p['element'])
        d_abord = (l.get('e1_first') or '').split()                 # DEC-0072 : consonnes vues d'abord
        en_deux = l.get('split_parts') == 'true'
        partie_a = [e for e in elements if e not in tons and place_de(e) in GROUPE_A] if en_deux else elements
        avant = {c for c, k in ouv.items() if k < rang}             # sons et tons des leçons précédentes
        de_la_lecon = {c for c, k in ouv.items() if k == rang}

        # 1. Consonnes « d'abord » : consonne + voyelle, sans finale ; voyelles de la 1re partie d'abord.
        for e in d_abord:
            candidats = [w for w, s in monosyllabes.items()
                         if s['initial'] == e and not s['final'] and not s['glide'] and ton_ouvert(w, rang)]
            candidats.sort(key=lambda w: (monosyllabes[w]['nucleus'] not in partie_a, frequence(w)))
            supports = [p['word_code'] for p in series if p['element'] == e and p['word_code']]   # m : « ma »
            choisis = []
            prendre(candidats, lambda w: monosyllabes[w]['nucleus'], choisis, supports)
            ajouter(lignes, code, e, choisis, femmes, hommes)

        # 2. Sons et tons des séries, avec la règle de préférence. Un son déjà présenté « d'abord »
        #    (m de L01, aussi dans la série ba / ma / va) garde les mêmes mots : pas de second jeu.
        for e in (x for x in elements if x not in d_abord):
            est_ton = e in tons
            place = None if est_ton else place_de(e)

            def convient(w):
                s = monosyllabes[w]
                return ton_ouvert(w, rang) and (s['tone'] == e if est_ton else s.get(place) == e)

            vus = avant | set(d_abord) | {e}
            if en_deux and e not in partie_a:                       # partie B : la partie A est vue
                vus |= set(partie_a)

            def niveau(w):
                autres = sons_du_mot(w)
                if autres <= vus:
                    return 0
                return 1 if autres <= vus | de_la_lecon else 2

            candidats = sorted((w for w in monosyllabes if convient(w)), key=lambda w: (niveau(w), frequence(w)))
            if d_abord and e in partie_a:                           # DEC-0072, point 2 : niveau 0 seulement
                candidats = [w for w in candidats if niveau(w) == 0]
            supports = [p['word_code'] for p in series if p['element'] == e and p['word_code']]
            supports += [p['word_code'] for p in series if p['position'] == '1' and p['word_code']]
            # variété : début différent (voyelle différente pour un son de début, voyelle + début pour un ton)
            cle = (lambda w: decomp[w]['nucleus']) if place == 'initial' else \
                  (lambda w: (decomp[w]['initial'], decomp[w]['nucleus'])) if est_ton else \
                  (lambda w: decomp[w]['initial'])
            choisis = []
            for n in (0, 1, 2):                                     # niveau par niveau (DEC-0072, point 4)
                prendre([w for w in candidats if niveau(w) == n], cle, choisis, supports)
            if len(choisis) < MIN_EXEMPLES:                         # DEC-0073 : syllabes sans sens, niveau 0
                def convient_syl(w):
                    s = decomp[w]
                    if place in GROUPE_A and not s['initial']:     # voyelle seule : déjà jouée (DEC-0070)
                        return False
                    return ton_ouvert(w, rang) and (s['tone'] == e if est_ton else s.get(place) == e)
                syl = [w for w in sans_sens if convient_syl(w) and niveau(w) == 0]
                syl.sort(key=lambda w: (sans_sens[w]['invented'] == 'true', w))   # réelles d'abord
                complement = []
                prendre(syl, lambda w: cle(w), complement)
                # variété avec les mots déjà choisis : début (ou voyelle) différent si possible
                deja = {cle(c) for c in choisis}
                complement.sort(key=lambda w: (sans_sens[w]['invented'] == 'true', cle(w) in deja))
                choisis += complement[:MIN_EXEMPLES - len(choisis)]
            ajouter(lignes, code, e, choisis, femmes, hommes)
    return lignes


def main():
    racine = next((a for a in sys.argv[1:] if not a.startswith('--')), '.')
    donnees = os.path.join(racine, '04_DONNEES')
    lignes = choisir(donnees)
    chemin = os.path.join(donnees, 'exemples_e1.csv')
    vides = [l for l in lignes if not l['word_code'] and not l['syllable']]
    nb_syl = sum(1 for l in lignes if l['syllable'])
    print(f"{len(lignes) - len(vides)} mots d'exemple pour {len({(l['lesson_code'], l['element']) for l in lignes})} sons ; "
          f"dont {nb_syl} syllabes sans sens (DEC-0073) ; "
          f"{len(vides)} son(s) sans exemple : " + ', '.join(f"{l['lesson_code']} {l['element']}" for l in vides))
    if '--verifier' in sys.argv:
        actuel = lire(donnees, 'exemples_e1.csv') if os.path.exists(chemin) else []
        cles = lambda ls: {(l['lesson_code'], l['element'], l['word_code']) for l in ls}
        print('Différences avec le fichier actuel :', len(cles(lignes) ^ cles(actuel)))
        # Détail, son par son : mots actuels → mots proposés.
        def par_son(ls):
            d = {}
            for x in ls:
                d.setdefault((x['lesson_code'], x['element']), []).append(
                    x['note'] if x['word_code'] else ('(' + x['syllable'] + ('*' if x.get('invented') == 'true' else '') + ')'
                                                      if x.get('syllable') else '—'))
            return d
        a, n = par_son(actuel), par_son(lignes)
        for k in sorted(set(a) | set(n)):
            if a.get(k) != n.get(k):
                print(f"  {k[0]} {k[1]:14} {', '.join(a.get(k, ['(absent)'])):28} → {', '.join(n.get(k, ['(retiré)']))}")
        return
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(lignes)
    print('Écrit :', chemin)


if __name__ == '__main__':
    main()
