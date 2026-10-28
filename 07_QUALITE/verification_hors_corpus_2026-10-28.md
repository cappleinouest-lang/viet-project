---
id: QUAL-VERIF-HORS-CORPUS-20261028
titre: Vérification des termes hors corpus des séries minimales
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Les 107 termes des séries minimales absents de mots.csv ont été cherchés
  dans trois dictionnaires : 74 sont de vrais mots, 33 restent des syllabes
  inventées. Il ne reste que 9 séries sans paire de deux mots réels pour E2.
entrees: [DATA-MODELE, REG-DEC]
sorties: [04_DONNEES/paires_minimales.csv]
sources:
  - https://github.com/undertheseanlp/dictionary (fusion de 3 listes, licence GPL v3)
  - Hồ Ngọc Đức, liste de mots (hongocduc) ; Từ điển tiếng Việt (tudientv) ; Wiktionnaire vietnamien (wiktionary)
---

# Vérification des termes hors corpus des séries minimales

## 1. Méthode

- **Fait** : chaque terme marqué `invented = true` dans `paires_minimales.csv`
  a été cherché comme **entrée isolée, en minuscules** (pour écarter les noms
  propres) dans les trois listes fusionnées par *underthesea*.
- **Critère retenu (DEC-0027)** : présent dans **au moins 2 dictionnaires**
  → mot réel (`invented = false`) ; dans 1 seul ou aucun → syllabe inventée.
- **Limite** : ces listes donnent l'**existence** d'un mot, pas son sens, sa
  fréquence ni son usage au Nord. Certains mots peuvent être rares,
  familiers ou du Sud. Le sens reste à vérifier avant toute image ; la
  colonne `validated` reste à `false`.

## 2. Résultats

| Résultat | Termes | Liste |
|---|---|---|
| Mot réel (≥ 2 dictionnaires) | 74 | *ang*, *be*, *bi*, *bè*, *bì*, *cán*, *cúng*, *dơ*, *dị*, *gioi*, *giòi*, *giọi*, *ha*, *ham*, *hen*, *hoi*, *há*, *hèn*, *hén*, *héo*, *hò*, *hô*, *khẻ*, *liu*, *me*, *mu*, *mun*, *muồi*, *mè*, *mé*, *môm*, *múi*, *mộc*, *mờ*, *mợ*, *mủ*, *mủi*, *ngả*, *nhe*, *nà*, *néo*, *nêm*, *nò*, *phai*, *phơ*, *phờ*, *sạ*, *sọ*, *ti*, *tiu*, *toi*, *tót*, *va*, *vu*, *vít*, *vói*, *vạ*, *vọ*, *vối*, *xen*, *xo*, *ó*, *ôn*, *úng*, *đao*, *đát*, *đê*, *đẹt*, *đọt*, *đố*, *đớt*, *ơ*, *ờ*, *ợ* |
| Un seul dictionnaire → inventé, à confirmer | 5 | *côm*, *mú*, *nen*, *nuốc*, *pa* |
| Absent des 3 dictionnaires → inventé | 28 | *com*, *dợ*, *giay*, *hon*, *hòi*, *hó*, *họi*, *họt*, *lám*, *mon*, *mói*, *mổi*, *mộn*, *nguồi*, *ngá*, *nin*, *phài*, *phại*, *phợ*, *pim*, *pên*, *sộ*, *thịc*, *thịn*, *vộ*, *xêm*, *đàu*, *đẹm* |

Détail des termes présents dans un seul dictionnaire :

| Terme | Dictionnaire |
|---|---|
| *côm* | hongocduc |
| *mú* | hongocduc |
| *nen* | hongocduc |
| *nuốc* | hongocduc |
| *pa* | hongocduc |

## 3. Effet sur E2

Séries sans paire de deux mots réels : **52 → 9**. Pour ces 9 séries, la
paire d'E2 contient une syllabe inventée, présentée par des **boutons
sonores** (DEC-0027, R-LEX-05) :

*xem / xêm*, *nên / nen / nin*, *pin / pên*, *pin / pim*, *con / hon*,
*học / họt*, *thịt / thịn / thịc*, *nước / nuốc*, *người / nguồi*.

Toutes portent sur un **son** (voyelle ou consonne finale) ; aucune série de
ton n'est concernée.

## 4. À faire

- Vérifier le sens et l'usage au Nord des 74 mots réels (dictionnaire ou
  locuteur natif), puis décider s'ils deviennent des mots de `mots.csv`.
- Confirmer les 5 termes d'un seul dictionnaire.

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
