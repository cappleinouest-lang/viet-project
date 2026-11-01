# -*- coding: utf-8 -*-
"""
Fabrique 04_DONNEES/syllabes_e1.csv : les syllabes SIMPLES candidates pour compléter les mots
d'exemple de l'étape E1 quand le corpus n'en a pas assez (DEC-0073). Le fichier produit est lu par
choisir_exemples_e1.py ; ce script-ci ne sert qu'à le refaire (par exemple si mots.csv change).

Ce qui est produit : toutes les combinaisons
    consonne initiale (aucune, b, m, n, d, đ, h, l, t, v, x, ph, th, ch, kh, nh)
  + voyelle simple (a, e, ê, i, o, ô, ơ, u, ư ; ă et â seulement suivies d'une finale)
  + finale (aucune, -m, -n, -p, -t ; -p et -t avec sắc ou nặng seulement)
  + ton (les 6),
sauf celles qui sont déjà des mots de mots.csv. Les consonnes à plusieurs écritures selon la voyelle
(c / k / q, g / gh, ng / ngh) et p- (emprunts) sont laissées de côté : leur écriture dépend du
contexte. Chaque syllabe est décomposée avec les codes de sons.csv (colonnes initial, nucleus,
final, tone) et classée :
    invented = false : présente, comme entrée isolée, dans au moins 2 des 3 dictionnaires
                       (Hồ Ngọc Đức, Từ điển tiếng Việt, Wiktionnaire), critère de DEC-0027 ;
    invented = true  : sinon (syllabe inventée, jamais écrite : R-LEX-06).
La colonne dictionaries dit dans lesquels elle a été trouvée.

Prérequis : la liste fusionnée des 3 dictionnaires du dépôt GitHub undertheseanlp/dictionary
(fichier dictionary/words.txt, licence GPL v3, non copié dans le projet), la même source que
QUAL-VERIF-HORS-CORPUS-20261028. Exemple, dans PowerShell, depuis un dossier hors du projet :
    git clone --depth 1 https://github.com/undertheseanlp/dictionary.git

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\fabriquer_syllabes_e1.py <chemin de words.txt> 04_DONNEES

Limite : les dictionnaires donnent l'existence d'une syllabe, pas son sens ni son usage à Hanoï.
"""
import csv
import json
import sys
import unicodedata

N = lambda x: unicodedata.normalize('NFC', x)

INITIALES = [('', ''), ('b', 'PH-IN-b'), ('m', 'PH-IN-m'), ('n', 'PH-IN-n'), ('d', 'PH-IN-d'), ('đ', 'PH-IN-dd'),
             ('h', 'PH-IN-h'), ('l', 'PH-IN-l'), ('t', 'PH-CO-t'), ('v', 'PH-IN-v'), ('x', 'PH-IN-x'),
             ('ph', 'PH-CO-ph'), ('th', 'PH-CO-th'), ('ch', 'PH-IN-ch'), ('kh', 'PH-IN-kh'), ('nh', 'PH-IN-nh')]
VOYELLES = [('a', 'PH-VS-a'), ('e', 'PH-VS-e'), ('ê', 'PH-VO-ee'), ('i', 'PH-VS-i'), ('o', 'PH-VS-o'),
            ('ô', 'PH-VS-oo'), ('ơ', 'PH-VO-ow'), ('u', 'PH-VS-u'), ('ư', 'PH-VO-uw'), ('ă', 'PH-VO-aw'),
            ('â', 'PH-VO-aa')]
FINALES = [('', ''), ('m', 'PH-FI-m'), ('n', 'PH-FI-n'), ('p', 'PH-FI-p'), ('t', 'PH-FI-t')]
TONS = [('ngang', ''), ('sac', '\u0301'), ('huyen', '\u0300'), ('hoi', '\u0309'), ('nga', '\u0303'), ('nang', '\u0323')]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    liste, donnees = sys.argv[1], sys.argv[2]
    dico = {}
    for ligne in open(liste, encoding='utf-8'):
        o = json.loads(ligne)
        s = o['source']
        dico[N(o['text'])] = s if isinstance(s, list) else [s]
    with open(donnees + '/mots.csv', encoding='utf-8-sig', newline='') as f:
        mots = {N(m['written']) for m in csv.DictReader(f, delimiter=';')}
    lignes = []
    for gi, ci in INITIALES:
        for gv, cv in VOYELLES:
            for gf, cf in FINALES:
                if gv in 'ăâ' and not gf:                       # ă et â ne terminent jamais une syllabe
                    continue
                for ton, marque in TONS:
                    if gf in ('p', 't') and ton not in ('sac', 'nang'):
                        continue
                    ecrit = N(gi + N(gv + marque) + gf)         # le ton se pose sur l'unique voyelle
                    if ecrit in mots:                           # déjà un mot du corpus
                        continue
                    sources = sorted(dico.get(ecrit, []))
                    lignes.append([ecrit, ci, cv, cf, ton, 'false' if len(sources) >= 2 else 'true', ' '.join(sources)])
    with open(donnees + '/syllabes_e1.csv', 'w', encoding='utf-8', newline='') as f:
        f.write('written;initial;nucleus;final;tone;invented;dictionaries\n')
        for x in lignes:
            f.write(';'.join(x) + '\n')
    print(len(lignes), 'syllabes ;', sum(x[5] == 'false' for x in lignes), 'réelles,',
          sum(x[5] == 'true' for x in lignes), 'inventées')


if __name__ == '__main__':
    main()
