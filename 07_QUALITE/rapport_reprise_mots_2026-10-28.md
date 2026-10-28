---
id: QUAL-REPRISE-MOTS-20261028
titre: Rapport de reprise des mots et syllabes
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Résultat de la reprise automatique de mots.csv et syllabes.csv depuis les
  archives : sources utilisées, chiffres, anomalies et points à décider.
entrees: [DATA-MODELE, REG-DEC]
sorties: [04_DONNEES/mots.csv, 04_DONNEES/syllabes.csv]
sources:
  - _ARCHIVES/Projet de Formation_Vietnamien_A0_to_A2/PROD/00_GLOBAL/01_DB/01_DATA_SOURCES/EXPORTS/word.csv (mars 2026, la plus récente)
  - _ARCHIVES/Projet de Formation_Vietnamien_A0_to_A2/PROD/00_GLOBAL/01_DB/01_DATA_SOURCES/EXPORTS/word_frequency_vi_wordfreq_v1.csv
  - _ARCHIVES/Projet sous Anki/03_DATA_CSV/language/words.csv (étymologies)
  - _ARCHIVES/Projet de Formation_Vietnamien_A0_to_A2/PROD/00_GLOBAL/grammatical_categories.csv
---

# Rapport de reprise des mots et syllabes

## Résumé

**324 mots** et **372 syllabes** repris. La décomposition automatique de
chaque syllabe (initiale, noyau, finale, ton) a abouti pour **100 %** des
syllabes. Trois points demandent une décision : la **liste de fréquence**,
le **choix des mots supports du Module 0** (à refaire avec les 14 leçons) et
la **relecture des traductions**.

## 1. Chiffres

| Élément | Valeur |
|---|---|
| Mots repris | 324 (dont 84 marqués « support Module 0 » dans les archives) |
| Syllabes | 372 ; **un ton par syllabe** |
| Syllabes non décomposées | 0 |
| Codes de sons fusionnés appliqués (DEC-0018) | oui (k→c, gh→g, ngh→ng, y→i, gi/r→d, tr→ch, s→x) |
| Mots sans rang de fréquence | 123 |
| Mots sans étymologie | 13 |
| Mots sans traduction | 0 |

## 2. Leçon à partir de laquelle chaque mot est utilisable

Calculée à partir de `ouvertures.csv` (le mot devient utilisable quand tous
ses sons et tons sont ouverts) :

| Leçon | L01 | L02 | L03 | L04 | L05 | L06 | L07 | L08 | L09 | L10 | L11 | L12 | L13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mots | 24 | 25 | 4 | 22 | 13 | 11 | 10 | 20 | 36 | 88 | 11 | 43 | 17 |

## 3. Constat important : peu de mots pour les leçons de tons

Mots d'**une syllabe** utilisables dans chaque leçon de ton glottalisé
(\* = déjà marqué « support Module 0 ») :

| Leçon | Mots disponibles |
|---|---|
| L03 nặng | *bạn\*, hẹn, họ, mẹ* (4) |
| L07 hỏi | *giỏi, ở, phải, hỏi, rẻ, dở, mở, phở\** (8) |
| L11 ngã | *dễ, lẽ, cũng\*, mỗi, mũi, ngã, nghĩ, cũ, mũ* (9) |

> **Analyse** : les 84 mots « support Module 0 » des archives ont été choisis
> pour l'ancien ordre (12 leçons). Avec les 14 leçons, leur répartition est
> inégale (1 seul mot pour L03, L07 et L11). La liste des mots supports est
> à **refaire** à partir du corpus, leçon par leçon. Des mots fréquents et
> simples manquent au corpus pour L03 (par exemple *mạ*, *bạ*, *nạ*,
> *tạ*, *lạ* — à vérifier).

## 4. Fréquence

- La liste utilisée (wordfreq, 1 000 mots, sous-titres de films) ne contient
  **pas** les mots composés (*cà phê*, *bệnh viện*…) et laisse de côté des
  mots courants (*bốn*, *chín*, *mèo*…) : 123 mots sans rang.
- Les traductions de la liste « underthesea v4 » contiennent des erreurs
  (exemple : *và* traduit « Utiliser avec des baguettes ») : elle n'a pas été
  utilisée pour les traductions.

> **À décider** (R-LEX-07) : liste de fréquence de référence. Le critère
> « parmi les 500 plus fréquents » (R-LEX-03) n'est pas vérifiable pour un
> tiers des mots avec la liste actuelle.

## 5. Traductions à relire

Les traductions viennent de `word.csv` (mars 2026). Elles sont globalement
justes ; quelques-unes méritent une relecture :

| Mot | Traduction actuelle | Remarque |
|---|---|---|
| *chưng* | présenter | sens courant : « cuire à la vapeur » (*bánh chưng*) ; « exposer » se dit plutôt *trưng* — **à vérifier** |
| *à* | préposition (à, vers, pour) | à l'oral, surtout **particule** de question ou de surprise (« ah ? ») — **à vérifier** |
| *chi* | dépenses (argent de poche) | sens multiples (dépenser ; « quoi » au Centre) — **à vérifier** |
| *lẽ* | raison | souvent dans *có lẽ* (peut-être) |

## 6. Étymologie manquante (13 mots)

*cha, ho, lam, ma, pin, môn, nem, va li, dịu, tuy, lưu, ngửi, chuyên* —
à compléter (*pin* et *va li* sont des emprunts au français).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
