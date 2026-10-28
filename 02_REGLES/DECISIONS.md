---
id: REG-DEC
titre: Journal des décisions
statut: VALIDE
version: 1.6
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

### DEC-0005 — Ordre de progression du Module 0

- **Date** : 2026-10-28
- **Question** : quel ordre de progression retenir ? Quatre ordres coexistent
  dans les archives :
  - A — Référentiel phonétique R02 (OLD) ;
  - B — `module_0_lecons_structure.csv` (OLD, 2026-02-08) ;
  - C — Référentiel des groupes pédagogiques v1.1 (dossier récent, 2026-03-02) ;
  - D — `pedagogical_groups.csv` (dossier récent, 2026-02-25).
- **Options** : 1 — C comme référence + décision séparée sur les tons
  glottalisés ; 2 — C tel quel ; 3 — repartir de A ou B.
- **Décision** : **option 1**. L'ordre **C** (12 leçons, L01 à L12) est
  l'ordre de référence. A, B et D sont **remplacés**. La place des tons
  glottalisés (hỏi, ngã, nặng, aujourd'hui en L09) fait l'objet d'une
  décision séparée (DEC-0006, à prendre).
- **Raison** : C est le plus récent, le plus détaillé, appliqué par la base
  et par la règle d'atomicité (0 violation) ; D contient une erreur de fond
  (ă et â qualifiés de « longues » alors qu'elles sont brèves).
- **Impacte** : `03_PROGRAMME/progression_M0.md`, `04_DONNEES` (numérotation
  des groupes pédagogiques).
- **Pièce jointe** : classeur `decision_02_ordre_progression_M0.xlsx`.

### DEC-0006 — Place des tons glottalisés (hỏi, ngã, nặng)

- **Date** : 2026-10-28
- **Question** : où placer, par défaut, hỏi, ngã et nặng (tous trois en L09
  dans l'ordre C) ? Crainte : surcharge cognitive si les trois arrivent
  ensemble, alors qu'ils sont difficiles à percevoir.
- **Options** : 1 — les répartir un par un dans le Module 0 ;
  2 — L09 découpée en 3 sous-leçons ; 3 — statu quo (les trois en L09).
- **Décision** : **option 1**. Ordre par défaut, chaque ton opposé à un ton
  déjà connu qui lui ressemble :
  1. **nặng** juste après les tons simples (vers L03), opposé à huyền ;
  2. **hỏi** au milieu du Module 0 (vers L06), opposé à huyền puis à nặng ;
  3. **ngã** en L09, opposé à sắc ;
  4. contraste final **hỏi / ngã**.
  Positions exactes à fixer dans `03_PROGRAMME/progression_M0.md`, sans
  jamais deux nouveautés dans la même leçon. **ngã** doit être acquis avant
  le début de A1 (marqueurs *đã*, *sẽ*). L'élève peut prendre de l'avance en
  écoute dans la limite de DEC-0007.
- **Raison** :
  - **Recherche** : en vietnamien du Nord, ces trois tons reposent en partie
    sur la qualité de la voix (glottalisation), indice nouveau pour un
    francophone (Brunelle, 2009) et mal exploité par les apprenants
    (Bauman et al., 2009) ; aucune étude trouvée sur l'ordre d'introduction.
  - **Fréquences** (comptage sur `word_frequency_vi_underthesea_v4.csv`,
    1 000 mots, pondéré par l'usage) : nặng 17 % des syllabes, hỏi 10 %,
    ngã 4 % ; nặng présent dans 17 des 100 mots les plus fréquents
    (*được, một, bạn…*).
- **Impacte** : `03_PROGRAMME/progression_M0.md` ; groupes pédagogiques et
  `tones.csv` dans `04_DONNEES` (le groupe 9 est éclaté) ; règle d'atomicité v2.0.

### DEC-0007 — Deux parcours indépendants : écoute et production

- **Date** : 2026-10-28
- **Question** : un élève doit-il terminer la production d'une leçon avant
  de commencer l'écoute de la suivante ?
- **Décision** : **non**. Chaque leçon a deux volets, chacun avec son verrou :
  - **parcours écoute** : valider l'écoute de la leçon N ouvre l'écoute de N+1 ;
  - **parcours production** : valide la prononciation, **sans bloquer**
    l'avancée en écoute ;
  - **contrainte unique entre les deux** : un élément ne se produit qu'après
    validation de son écoute (perception avant production) ;
  - **écart maximal** : l'écoute peut avoir **3 leçons d'avance** au plus sur
    la production (valeur paramétrable). Au-delà, l'écoute est mise en pause
    jusqu'à ce que la production rattrape son retard.
- **Options écartées** : B — aucune limite (avertissement seul) ;
  C — limite en nombre de micro-leçons actives.
- **Raison** : laisser l'élève travailler tôt l'écoute des tons difficiles
  sans attendre la production des tons simples ; l'écart limité évite de
  négliger la production, qui progresse peu sans pratique dédiée
  (Li et DeKeyser, 2017). Prolonge le modèle hybride (micro-leçons en
  parallèle) de `CADR_SPEC_STRUCTURE_MODULE_0_HYBRIDE_v02` (archives OLD).
- **Impacte** :
  - règle d'atomicité v1.1 → **v2.0** (cartes d'écoute / cartes de production) ;
  - `04_DONNEES` : leçon d'écoute et leçon de production pour chaque son et ton ;
  - outil de formation : deux familles de cartes activables séparément ;
  - DEC-0006 : ne fixe plus qu'un **ordre recommandé par défaut**.

### DEC-0008 — Corrections factuelles des spécificités de la langue

- **Date** : 2026-10-28
- **Question** : corriger deux erreurs de
  `P0_CADR_GLOB_01_NORM_Specificites_Langue_Vietnamienne_v3` (OLD) ?
- **Décision** :
  1. Le français **n'est pas** une langue tonale : c'est la **prosodie**
     qui prime (intonation, rythme, accent de fin de groupe), à l'échelle
     de la phrase ; la hauteur de la voix ne change pas le sens d'un mot.
     Risque pour le francophone : plaquer sa prosodie sur les tons.
  2. Notation phonétique unique pour le projet : **ư = /ɨ/**, **ơ = /ə/**
     (celle de la base). La notation /ɯ/, /ɤ/, également répandue, est
     mentionnée en note.
- **Raison** : (1) fait établi, cohérent avec « tons ≠ intonation » dans le
  même document ; (2) le document et `phonemes.csv` se contredisaient ; la
  notation de la base évite toute reprise des 84 phonèmes.
- **Impacte** : `01_FONDATIONS/02_specificites_vietnamien.md`.

### DEC-0009 — Norme de prononciation : accent courant de Hanoï

- **Date** : 2026-10-28
- **Question** : quelle prononciation pour l'audio et les exercices ?
  À Hanoï, tr/ch, s/x et d/gi/r se confondent dans l'usage courant.
- **Options** : a — accent courant de Hanoï (avec ces fusions) ;
  b — prononciation du Nord « soignée » qui les distingue.
- **Décision** : **option a**, l'accent courant de Hanoï.
  - L'audio (voix natives ou de synthèse) suit cet accent.
  - **tr/ch**, **s/x** et **d/gi/r** ne font **pas** l'objet d'exercices
    d'écoute : ce sont des points d'**orthographe** à mémoriser
    (association mot ↔ écriture).
  - La discrimination « ch / tr » prévue en L08 dans les archives est
    supprimée.
- **Raison** : c'est l'accent effectivement entendu au quotidien à Hanoï ;
  cohérent avec l'objectif de compréhension des natifs (FOND-01).
- **Impacte** : `01_FONDATIONS/02_specificites_vietnamien.md` (§ 4.3),
  `03_PROGRAMME/progression_M0.md` (L08), choix des voix de synthèse.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-28 | Création, DEC-0001 à DEC-0003. |
| 1.1 | 2026-10-28 | Ajout de DEC-0004 (durée du Module 0). |
| 1.2 | 2026-10-28 | Ajout de DEC-0005 (ordre de progression du Module 0). |
| 1.3 | 2026-10-28 | DEC-0006 ouverte (tons glottalisés) ; ajout de DEC-0007 (deux parcours écoute / production). |
| 1.4 | 2026-10-28 | DEC-0006 prise : nặng → hỏi → ngã, répartis dans le Module 0. |
| 1.5 | 2026-10-28 | Ajout de DEC-0008 (corrections factuelles : prosodie du français, notation de ư et ơ). |
| 1.6 | 2026-10-28 | Ajout de DEC-0009 (accent courant de Hanoï). |

## Liens

- **Sorties** : [REGLES_DOCUMENTAIRES.md](REGLES_DOCUMENTAIRES.md)
