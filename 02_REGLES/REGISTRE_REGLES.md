---
id: REG-REGLES
titre: Registre des règles
statut: BROUILLON
version: 0.9
date: 2026-10-28
resume: >
  Toutes les règles opposables de la formation, une par ligne, numérotées et
  vérifiables : parcours et étapes, volets et verrous, atomicité, sons et
  tons, mots, écrit, audio, progression. Chaque règle indique comment la
  vérifier et d'où elle vient. Les règles de code et de programmation sont
  hors périmètre pour l'instant.
entrees: [FOND-01, FOND-02, FOND-03, FOND-04, REG-DEC]
sorties: [PROG-M0, 04_DONNEES, 07_QUALITE, DATA-MODELE, PROD-ARCH, QUAL-PROP-MOTS-M0, PROG-ACT]
sources:
  - 01_FONDATIONS (FOND-01 à FOND-04, version 1.0)
  - 02_REGLES/DECISIONS.md (DEC-0004 à DEC-0013)
---

# Registre des règles

## Résumé

Une règle = un identifiant stable, un énoncé court, une méthode de
vérification, une source. Les règles sont regroupées en familles. Une règle
ne se modifie pas en silence : tout changement passe par une décision dans
`DECISIONS.md` et une nouvelle version de ce registre.

## Périmètre

| Inclus | Hors périmètre (pour l'instant) |
|---|---|
| Pédagogie, phonétique, choix des mots, écrit, audio, progression | Règles de **code et de programmation** (SQL, Python, PowerShell, encodage des scripts). Elles seront traitées plus tard, à partir de `IA_RULES_STRICT_READ_FIRST_v4_0` (archives). |
| | Règles **documentaires** : voir `REGLES_DOCUMENTAIRES.md` (DOC-01 à DOC-35) |

## Familles

| Préfixe | Famille |
|---|---|
| **R-PARC** | Parcours d'une leçon et étapes |
| **R-VOL** | Volets écoute / production et verrous |
| **R-ATOM** | Une seule nouveauté, atomicité |
| **R-PHON** | Sons, tons, notation, accent |
| **R-LEX** | Choix des mots et des syllabes |
| **R-ECR** | Place de l'écrit |
| **R-AUD** | Audio |
| **R-PROG** | Progression du Module 0 |
| **R-REV** | Recyclage et révision |
| **R-SUP** | Neutralité vis-à-vis du support |

Légende de la colonne « Vérification » : **auto** = contrôlable par un
script sur les données ; **revue** = contrôle humain ; **mesure** = statistique
de l'élève.

## R-PARC — Parcours d'une leçon

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-PARC-01** | Chaque leçon se parcourt en **5 étapes**, dans cet ordre : E1 Écouter, E2 Distinguer, E3 Opposer, E4 Répéter, E5 Stabiliser. | auto : chaque activité porte une étape E1–E5 | DEC-0010 |
| **R-PARC-02** | Une activité appartient à **une seule** étape et **une seule** leçon. | auto | DEC-0010 |
| **R-PARC-03** | **E1** : l'élève écoute sans répondre ni répéter. | revue | FOND-04 § 3 |
| **R-PARC-04** | **E2** : l'élève choisit entre **deux** possibilités (A ou B) qui forment une **paire minimale** tirée de la série de la leçon (mot support + un autre terme) ; le contraste porte sur un **ton** ou un **son** proche (voyelle, consonne). Choix présentés au débit lent par l'**image et le symbole**, au débit normal par le **symbole seul** (DEC-0028) ; sans image : symbole ou bouton sonore. Symbole d'un ton : pictogramme et couleur ; symbole d'un son : `ipa_main` du son contrasté, présenté en E1 avec son audio (DEC-0029). | auto : 2 termes d'une même `series_code` | FOND-04 § 3 ; DEC-0024 ; DEC-0026 ; DEC-0028 ; DEC-0029 |
| **R-PARC-05** | **E3** : les termes forment une **série minimale** de **2 à 4** mots ou pseudo-mots, qui ne diffèrent que par l'élément cible (ton ou son). E3 reprend la série **complète** dont E2 a utilisé une paire. | auto : comparaison des termes | FOND-04 § 3 ; DEC-0025 ; DEC-0026 |
| **R-PARC-06** | **E4** : l'élève reproduit après un modèle, d'abord **lent** puis **normal** ; le modèle lent précède toujours le modèle normal. | auto : ordre des audios | FOND-04 § 3 |
| **R-PARC-07** | **E5** : séries d'enchaînement, débit progressif (lent → normal → un peu plus rapide). | auto | FOND-04 § 3 |

## R-VOL — Volets et verrous

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-VOL-01** | E1–E3 forment le **volet écoute** ; E4–E5 le **volet production**. | auto | DEC-0010 |
| **R-VOL-02** | Valider l'écoute de la leçon N **ouvre** l'écoute de la leçon N+1, sans attendre la production de N. | mesure | DEC-0007 |
| **R-VOL-03** | La production d'un élément ne commence qu'**après** validation de son écoute. | mesure | DEC-0007 |
| **R-VOL-04** | L'écoute a **au plus 3 leçons d'avance** sur la production (paramètre). Au-delà, l'écoute est mise en pause jusqu'à rattrapage. | mesure | DEC-0007 |
| **R-VOL-05** | **Verrou d'écoute** : E2 et E3 réussis à **≥ 85 %** (paramètre), mesurés sur **au moins 2 voix**. | mesure | DEC-0012 |
| **R-VOL-06** | **Verrou d'écoute des leçons de tons** : **≥ 90 %** (paramètre). | mesure | DEC-0012 |
| **R-VOL-07** | Le verrou d'écoute exige aussi la reconnaissance à **débit normal** et l'absence de confusion majeure avec la leçon précédente. | mesure | FOND-04 § 5 |
| **R-VOL-08** | **Verrou de production** : production **intelligible**, pas parfaite. *Méthode de mesure à définir avec l'outil.* | à définir | FOND-04 § 5 |
| **R-VOL-09** | **Sortie du Module 0** : toutes les leçons validées dans les deux volets ; tons ≥ 90 % ; ư, ơ, â intelligibles ; -p, -t, -c, -ch non relâchées ; rythme syllabique. | mesure + revue | FOND-04 § 5 |
| **R-VOL-10** | On passe à la suite sur **verrou**, jamais sur **calendrier**. | revue | DEC-0004 |

## R-ATOM — Une seule nouveauté

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-ATOM-01** | Chaque leçon n'introduit qu'**une famille** de nouveautés (sons ou tons). | revue | FOND-04 § 6 |
| **R-ATOM-02** | Chaque activité n'a qu'**une cible** : un son **ou** un ton. | auto | FOND-04 § 6 |
| **R-ATOM-03** | Dans le **volet écoute** de la leçon N, un item ne contient que des sons et tons dont l'**écoute** est ouverte en N ou avant. | auto | FOND-04 § 6 ; règle d'atomicité v1.1 (archives), étendue |
| **R-ATOM-04** | Dans le **volet production** de la leçon N, un item ne contient que des sons et tons dont la **production** est ouverte en N ou avant. | auto | FOND-04 § 6 |
| **R-ATOM-05** | De E1 à E4, chaque item de la leçon N contient **l'élément cible de la leçon N**. Seule E5 (et la leçon de recyclage L14) peut contenir des items sans élément nouveau, au titre du recyclage. | auto | Règle d'atomicité v1.1 (archives), § 4.2 |
| **R-ATOM-06** | Chaque son et chaque ton possède **deux leçons d'ouverture** : une pour l'écoute, une pour la production. | auto : deux champs renseignés dans les données | DEC-0007 |

## R-PHON — Sons, tons, notation, accent

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-PHON-01** | La formation enseigne le **vietnamien du Nord**, **accent courant de Hanoï**. | revue | DEC-0009 |
| **R-PHON-02** | **tr/ch**, **s/x** et **d/gi/r** ne font l'objet d'**aucune** activité d'écoute (E1–E3) : leur distinction est un point d'orthographe (E4–E5). | auto : aucune paire E2/E3 sur ces contrastes | DEC-0009 |
| **R-PHON-03** | Seuls les sons de l'**inventaire du projet** (`04_DONNEES/phonemes.csv`) et les **6 tons** (`tons.csv`) sont utilisés. | auto | FOND-02 ; R02.1 (archives) |
| **R-PHON-04** | Notation phonétique de référence : celle de la base, notamment **ư = /ɨ/**, **ơ = /ə/**. | auto | DEC-0008 |
| **R-PHON-05** | **ngã** est noté **3ˀ5** (glottalisation au milieu) ; **nặng** **21ʔ** (en fin). | auto | FOND-02 § 1 |
| **R-PHON-06** | ă et â sont des voyelles **brèves** ; ê et ô ne sont **pas** des voyelles longues ; ê n'est **pas** une voyelle centrale. | revue | DEC-0005 ; FOND-02 § 3 ; FOND-03 § 5 |

## R-LEX — Mots et syllabes

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-LEX-01** | En Module 0, le mot est un **support sonore**, pas un vocabulaire à apprendre. | revue | FOND-04 § 9 |
| **R-LEX-02** | **Micro-lexique** du Module 0 : **50 à 100 mots** au plus. | auto : comptage | FOND-01 § 4 |
| **R-LEX-03** | Un mot utilisé satisfait les **5 critères** : sons de l'inventaire ; sons et tons déjà ouverts dans le volet ; parmi les **500 plus fréquents** ; **syllabe réelle** ; **une seule** cible nouvelle. | auto (fréquence : sur la liste de référence) | Règle de choix des mots v1.1 (archives) |
| **R-LEX-04** | Préférence pour les mots d'**une syllabe** ; **pas** de mot de 3 syllabes ou plus aux étapes d'écoute. | auto | Règle de choix des mots v1.1, R-MOT-01/02 |
| **R-LEX-05** | **Exception** : une **syllabe inventée**, conforme à la structure du vietnamien, est autorisée **uniquement en E2 et E3**, comme terme d'une série minimale, quand aucun mot réel ne convient (moins de 2 dictionnaires sur 3). En E2, elle est présentée par un **bouton sonore**. | auto : `invented` + étape E2 ou E3 | DEC-0013 ; DEC-0025 ; DEC-0027 |
| **R-LEX-06** | Une syllabe inventée n'est **jamais affichée**. | auto | DEC-0013 |
| **R-LEX-07** | La liste de fréquence de référence est à **fixer et documenter** dans `04_DONNEES` ; ses traductions doivent être revues (erreurs constatées). | revue | FOND-03 ; constat du 2026-10-28 |

## R-ECR — Écrit

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-ECR-01** | **E1, E2** : aucun écrit visible. | auto | DEC-0011 |
| **R-ECR-02** | **E3** : écrit absent au début, visible **en fin d'étape** (sauf syllabe inventée : R-LEX-06). | auto | DEC-0011 ; DEC-0013 |
| **R-ECR-03** | **E4, E5** : écrit visible, **à l'appui** de l'audio. | auto | DEC-0011 |
| **R-ECR-04** | Aucune transcription phonétique des **mots**. La notation phonétique des **sons** (`sons.csv`) peut accompagner l'écrit en production ; elle n'est jamais exigée de l'élève. Exception : le symbole court (`ipa_main`) du son contrasté sert d'étiquette de réponse dès E1 (DEC-0029). | revue | FOND-04 § 7 ; DEC-0021 ; DEC-0029 |

## R-AUD — Audio

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-AUD-01** | Audio **natif** ou **de synthèse validé**, accent courant de Hanoï. | revue (écoute de contrôle) | DEC-0009 ; FOND-04 § 8 |
| **R-AUD-02** | Étapes d'écoute (E1–E3) : **au moins 2 voix** distinctes, et autant de **variété** que possible (homme, femme, enfant ; débits différents) pour habituer l'oreille à plusieurs prononciations. | auto | FOND-04 § 8 ; DEC-0023 |
| **R-AUD-03** | Étapes de production (E4–E5) : **une voix modèle** unique par item. | auto | FOND-04 § 8 |
| **R-AUD-04** | Toute nouveauté est introduite à **débit lent** ; le débit normal vient après verrou ; le débit **rapide** sert à la stabilisation (E5). | auto | FOND-04 § 8 ; R-CU-06 (archives) ; DEC-0023 |
| **R-AUD-05** | Aucun audio **décoratif** ; tout audio est un item pédagogique. | revue | R02 (archives) |
| **R-AUD-06** | Tout audio est **regénérable** à partir des données seules (texte, voix, débit). | auto | FOND-01 § 5 ; R-CU-03 (archives) |

## R-PROG — Progression du Module 0

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-PROG-01** | Ordre de référence : les **14 leçons** de `04_DONNEES/lecons.csv` (ordre C complété par les leçons de tons). | auto | DEC-0005 ; DEC-0019 |
| **R-PROG-02** | Tons glottalisés **un par un**, chacun dans une **leçon dédiée** et opposé à un ton proche déjà connu : **nặng** en L03 (face à huyền) → **hỏi** en L07 (face à huyền puis nặng) → **ngã** en L11 (face à sắc), avec le contraste **hỏi / ngã**. | auto : `ouvertures.csv` | DEC-0006 ; DEC-0019 |
| **R-PROG-03** | **ngã** est acquis avant le début de A1. | mesure | DEC-0006 |
| **R-PROG-04** | Durées **indicatives** : rythme 20–30 min/jour ; Module 0 ≈ 4–6 mois ; total A0→A2 à préciser. | revue | DEC-0004 |
| **R-PROG-05** | Aucun apprentissage lexical ou grammatical substantiel avant validation du Module 0. | revue | FOND-01 § 5 |

## R-REV — Recyclage et révision

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-REV-01** | Toute nouveauté est **réutilisée** dans les leçons suivantes. | auto | FOND-04 § 10 ; R-CU-07 (archives) |
| **R-REV-02** | Chaque **E5** contient **au moins un** item d'une leçon précédente. | auto | FOND-04 § 10 |
| **R-REV-03** | La leçon **L14** est consacrée au recyclage de L01–L13, sans nouveauté. | auto | DEC-0005 ; DEC-0019 |
| **R-REV-04** | Les révisions sont **espacées** ; une erreur rapproche la révision suivante. | revue (paramétrage de l'outil) | FOND-04 § 10 |

## R-SUP — Neutralité vis-à-vis du support

| ID | Règle | Vérification | Source |
|---|---|---|---|
| **R-SUP-01** | Les fondations, règles, programme et données décrivent des **activités** et des **items**, jamais des « cartes », « decks » ou « notes ». | auto : recherche de ces mots | DEC-0010 |
| **R-IMG-01** | Chaque mot support facile à imager (`imageable`) reçoit une **image** (pictogramme ou dessin, style homogène) ; l'image peut apparaître dès E1 ; elle n'est pas de l'écrit. | auto : `images.csv` | DEC-0024 |
| **R-IMG-02** | Les images ont une **licence** compatible avec le partage, citée dans `images.csv`. | auto | DEC-0024 |
| **R-SUP-02** | Le choix de l'outil de formation (Anki ou autre) ne doit exiger **aucune** modification des fondations ni de ce registre ; seule une couche d'adaptation dans `05_PRODUCTION` est créée. | revue | DEC-0010 |

## Questions ouvertes

> **À décider** : méthode de mesure du verrou de production (R-VOL-08), à
> traiter avec le choix de l'outil.

> **À décider** : liste de fréquence de référence (R-LEX-07).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création : 57 règles en 10 familles, issues des fondations v1.0 et de DEC-0004 à DEC-0013. Règles de code hors périmètre. |
| 0.2 | 2026-10-28 | R-PROG-01, R-PROG-02, R-ATOM-05, R-REV-03 : 14 leçons (DEC-0019). |
| 0.3 | 2026-10-28 | R-ECR-04 : pas de transcription des mots (DEC-0021). |
| 0.4 | 2026-10-28 | R-AUD-02 et R-AUD-04 : variété des voix, débit rapide (DEC-0023). |
| 0.5 | 2026-10-28 | R-PARC-04, R-PARC-05, R-LEX-05 ; ajout de R-IMG-01 et R-IMG-02 (DEC-0024, DEC-0025). |
| 0.6 | 2026-10-28 | R-PARC-04 et R-PARC-05 : même série en E2 (paire) et E3 (série complète) ; contraste de ton ou de son (DEC-0026). |
| 0.7 | 2026-10-28 | R-LEX-05 : syllabe inventée permise en E2 et E3 (DEC-0027). |
| 0.8 | 2026-10-28 | R-PARC-04 : images, puis symboles (DEC-0028). |
| 0.9 | 2026-10-28 | R-PARC-04 et R-ECR-04 : symbole des sons = `ipa_main` du son contrasté (DEC-0029). |

## Liens

- **Entrées** :
  [Fondations](../01_FONDATIONS/README.md) ·
  [Journal des décisions](DECISIONS.md)
- **Sorties** :
  [Progression du Module 0](../03_PROGRAMME/progression_M0.md) ·
  `04_DONNEES` · `07_QUALITE` (contrôles automatiques)
