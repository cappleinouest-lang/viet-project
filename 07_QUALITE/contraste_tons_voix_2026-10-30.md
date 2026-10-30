---
id: QUAL-CONTRASTE-TONS-20261030
titre: Contraste des tons selon la voix de synthèse
statut: VALIDE
version: 1.1
date: 2026-10-30
resume: >
  Mesure, sur 36 mots (6 par ton) dits par les 4 voix FPT du projet, à quel
  point les 6 tons se distinguent par leur mélodie. Sert à choisir les voix
  avant de générer les audios de l'exercice « Combien de fois ? » (DEC-0054).
entrees: [REG-DEC, PROD-AUDIO]
sorties: []
sources:
  - 04_DONNEES/audio/*-normal.mp3 (F1, F3, H3, H4), mesure par l'algorithme de courbes_modele.py
---

# Contraste des tons selon la voix de synthèse

## Résumé

À la mesure, **Thu Minh (F3, écartée par DEC-0048)** sépare le mieux les tons
(94 % reconnus). Quang Anh (H1) et Minh Quan (H5) sont nettement en
dessous (61 % et 58 %). Parmi les voix actives, **Huy Phong (H4)** et **Ban Mai (F1)**
se valent ; **Le Minh (H3)** a le contraste le plus faible. Pour **toutes** les
voix, *huyền* et *hỏi* sont très proches par la mélodie, et *nặng* n'est pas
nettement bas. L'écart entre voix actives est faible sur un échantillon aussi
petit : l'écoute reste décisive.

## Méthode

- 36 mots d'une syllabe, sans finale -p, -t, -c, -ch, tirés au hasard parmi
  ceux que les 4 voix ont déjà prononcés (débit normal) : 6 par ton.
- Courbe mélodique par le calcul de `courbes_modele.py`, en demi-tons par
  rapport à la hauteur médiane de la voix (on garde le registre haut / bas).
- Chaque mot est décrit par 5 points de hauteur (10 % à 90 % de la durée),
  la durée et la part sans voix mesurable (coup de glotte).
- **Reconnus** : part des mots dont le ton est retrouvé par le ton moyen le
  plus proche (en laissant le mot de côté). **Contraste** : écart moyen entre
  les tons divisé par la dispersion à l'intérieur d'un ton (plus c'est grand,
  mieux les tons se séparent).

## Résultats

| Voix | Reconnus | Contraste | sắc / ngã | hỏi / nặng | huyền / nặng | huyền / hỏi |
|---|---|---|---|---|---|---|
| Ban Mai (F1) | 78 % | 4,00 | 3,23 | 2,55 | 1,99 | 1,08 |
| Thu Minh (F3, écartée) | **94 %** | **4,66** | **5,33** | 2,29 | 2,33 | 0,91 |
| Le Minh (H3) | 81 % | 3,24 | 2,42 | 1,87 | 2,15 | 1,07 |
| Huy Phong (H4) | 81 % | 4,07 | 2,11 | 2,06 | 1,70 | 0,95 |
| Quang Anh (H1, écartée) | 61 % | 2,83 | 1,84 | 1,31 | 0,78 | 1,05 |
| Minh Quan (H5, non retenue) | 58 % | 2,01 | 1,65 | 2,43 | 1,59 | 1,30 |

Confusions les plus fréquentes, toutes voix : *huyền* ↔ *hỏi*, *hỏi* ↔ *nặng*.

## Lecture

- **Fait mesuré** : *huyền* et *hỏi* ont presque la même mélodie (descendante,
  basse) chez les 4 voix. À Hanoï, *hỏi* se distingue surtout par une chute
  plus forte et une voix tendue ou grinçante, ce que la mélodie seule ne
  mesure pas.
- **Fait mesuré** : *nặng* est court mais reste à hauteur moyenne (≈ 0 demi-ton)
  chez les 4 voix, au lieu d'être bas et descendant.
- **Hypothèse** : ces deux faiblesses viendraient de la synthèse FPT elle-même ;
  à confirmer avec un enregistrement natif.
- **Ajout du 2026-10-30** (script `tester_voix_tons.py`, voix H1 et H5 générées
  dans `audio/_essais/tons/`) : **Quang Anh (H1)** et **Minh Quan (H5)** séparent
  nettement moins bien les tons. Leurs mots *hỏi* et *nặng* n'ont que 0,08 à
  0,11 s de voix mesurable : voix grinçante ou consonne avalée, que la mesure
  traite mal (hypothèse). Seul point fort : chez Quang Anh, *nặng* est bas et
  descendant (−0,8 → −2,6), comme attendu à Hanoï.
- **Limite** : 6 mots par ton ; une différence de 78 % à 81 % correspond à un
  seul mot. Seul l'écart de F3 (94 %) et la faiblesse de H3 (contraste 3,24)
  ressortent nettement.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-30 | Création. |
| 1.1 | 2026-10-30 | Ajout de Quang Anh (H1) et Minh Quan (H5). |
