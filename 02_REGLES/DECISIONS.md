---
id: REG-DEC
titre: Journal des décisions
statut: VALIDE
version: 1.1
date: 2026-10-28
resume: >
  Trace chaque arbitrage du projet : la question posée, les options, la
  décision et sa raison. Une décision ne se modifie pas : on en prend une
  nouvelle qui la remplace.
entrees: []
sorties: [REG-DOC]
sources: []
---

# Journal des décisions

## Résumé

Une ligne de décision = un identifiant `DEC-NNNN` qui ne change jamais
(DOC-22, DOC-26). Pour revenir sur une décision, on en ajoute une nouvelle
qui indique « remplace DEC-NNNN ».

## Décisions

### DEC-0001 — Refonte de la structure et archivage

- **Date** : 2026-10-28
- **Question** : comment repartir sur une base saine ?
- **Options** : réorganiser les dossiers existants sur place / archiver et
  reconstruire à côté.
- **Décision** : les dossiers `OLD`, `Projet de Formation_Vietnamien_A0_to_A2`
  et `Projet sous Anki` sont déplacés, intacts, dans `_ARCHIVES`. Une nouvelle
  structure en 7 dossiers est créée. Le contenu est repris depuis OLD
  **et** depuis le dossier récent `Projet de Formation_Vietnamien_A0_to_A2`.
- **Raison** : doublons, contradictions et versions multiples rendaient
  impossible de savoir quel document faisait foi ; l'archivage garde tout
  sans risque de perte.

### DEC-0002 — Langue des noms de fichiers

- **Date** : 2026-10-28
- **Question** : noms des documents en français ou en anglais ?
- **Décision** : documents en **français** ; scripts et colonnes de données
  en **anglais**.
- **Raison** : les documents sont lus par Christophe ; l'anglais côté
  technique reste compatible avec la base PostgreSQL existante.

### DEC-0003 — Gestion de l'historique

- **Date** : 2026-10-28
- **Question** : Git ou historique manuel ?
- **Décision** : **Git**, en plus du tableau d'historique en bas de chaque
  document.
- **Raison** : supprime les copies `_v1`, `_v2`, permet de revenir en arrière
  et de voir exactement ce qui a changé.

### DEC-0004 — Durée du Module 0

- **Date** : 2026-10-28
- **Question** : quelle durée retenir pour le Module 0 ? Les archives se
  contredisent : 40 à 60 h (*Objectifs généraux v2*) contre 240 à 400 h sur
  6 à 9 mois (*Stratégie pédagogique globale v01*), alors que le rythme prévu
  est de 15 à 30 min par jour.
- **Options** : A — garder 40 à 60 h ; B — garder 240 à 400 h ;
  C — exprimer la durée en rythme et en mois indicatifs.
- **Décision** : **option C**.
  - Rythme de référence : 20 à 30 min par jour.
  - Module 0 : environ 4 à 6 mois, soit 40 à 80 h, **à titre indicatif**.
  - Le passage d'une étape à l'autre est décidé par les **verrous**, pas par
    le calendrier.
  - Le pourcentage « 30 à 40 % du parcours » est supprimé.
  - Le total A0→A2 reste **ouvert, « à préciser »**, à partir des mesures
    réelles de progression (statistiques Anki).
- **Raison** : 240 à 400 h sont incompatibles avec 15 à 30 min par jour ;
  l'option C est cohérente avec le paradigme (progression pilotée par les
  verrous, non par le temps).
- **Impacte** : `01_FONDATIONS/01_intention_et_objectifs.md`,
  `03_PROGRAMME/progression_M0.md`.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-28 | Création, DEC-0001 à DEC-0003. |
| 1.1 | 2026-10-28 | Ajout de DEC-0004 (durée du Module 0). |

## Liens

- **Sorties** : [REGLES_DOCUMENTAIRES.md](REGLES_DOCUMENTAIRES.md)
