---
id: REG-DEC
titre: Journal des décisions
statut: VALIDE
version: 1.42
date: 2026-10-30
resume: >
  Trace chaque arbitrage du projet : la question posée, les options, la
  décision et sa raison. Une décision ne se modifie pas : on en prend une
  nouvelle qui la remplace.
entrees: []
sorties: [REG-DOC, REG-REGLES, DATA-MODELE, PROD-ARCH, QUAL-REPRISE-MOTS-20261028, QUAL-VERIF-HORS-CORPUS-20261028, PROG-ACT, PROD-AF-LECT]
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

### DEC-0010 — Vocabulaire du parcours et étapes E1 à E5

- **Date** : 2026-10-28
- **Question** : comment nommer les niveaux de la formation sans ambiguïté
  et sans présupposer le support (cartes, écrans…) ? Les archives emploient
  « unité » dans deux sens, numérotent U1, U2, U4, U5, U6 (pas de U3) dans un
  ordre qui n'est pas l'ordre pédagogique, et le contrat v1.9 contient deux
  architectures incompatibles (§ 2 par leçon, § 3 par phase).
- **Décision** :
  1. **Cinq termes**, un par niveau : **module** > **leçon** > **étape** >
     **activité** > **item**. Aucun terme ne désigne un support (« carte »
     n'est pas employé avant le choix de l'outil).
  2. **Cinq étapes**, dans cet ordre, pour chaque leçon : **E1 Écouter**
     (ex-U1) → **E2 Distinguer** (ex-U2) → **E3 Opposer**, paires minimales
     (ex-U5) → **E4 Répéter** (ex-U4) → **E5 Stabiliser** (ex-U6).
  3. Le **parcours** d'une leçon est la suite E1 → E5. Les deux ensembles de
     DEC-0007 s'appellent **volets** : volet **écoute** = E1–E3 ; volet
     **production** = E4–E5. La règle d'écart de DEC-0007 (3 leçons) porte
     sur ces volets.
  4. L'organisation **par leçon** (§ 2 du contrat v1.9) est retenue ; le
     modèle « par phase » (§ 3, R-ARCH-01, verrou de phase) est **remplacé**.
- **Raison** : un mot = un sens ; ordre des numéros = ordre réel ;
  neutralité vis-à-vis du support, choisi plus tard ; cohérence avec DEC-0007.
- **Impacte** : `01_FONDATIONS/04_principes_pedagogiques.md`, glossaire,
  `03_PROGRAMME`, données d'exercices.

### DEC-0011 — Place de l'écrit

- **Date** : 2026-10-28
- **Question** : l'écrit vietnamien est-il visible pendant le Module 0 ?
  (*Objectifs v2* l'interdisaient « avant maîtrise phonétique » ; le contrat
  v1.9, R-CU-05, l'autorise en production.)
- **Décision** : reprise de R-CU-05, adaptée aux étapes :
  - **E1, E2** : écrit **jamais** visible ;
  - **E3** : écrit absent au début, visible en fin d'étape ;
  - **E4, E5** : écrit **visible**, à l'appui de l'audio.
  Les points d'orthographe (tr/ch, s/x, d/gi/r — DEC-0009) s'apprennent en
  E4–E5.
- **Raison** : l'oreille d'abord, sans béquille visuelle ; l'écrit est
  nécessaire ensuite pour fixer l'orthographe.
- **Impacte** : FOND-01 (question levée), FOND-04.

### DEC-0012 — Seuils des verrous d'écoute

- **Date** : 2026-10-28
- **Question** : 85 % (contrat v1.9), ou 90 % pour les tons (*Objectifs v2*) ?
- **Décision** : **85 %** par défaut ; **90 %** pour les leçons de tons.
  Mesuré sur **au moins 2 voix**. Valeurs paramétrables, à ajuster avec les
  statistiques réelles.
- **Raison** : les tons sont la difficulté n° 1 (FOND-03).
- **Impacte** : FOND-04, `03_PROGRAMME`.

### DEC-0013 — Syllabes inventées dans les paires minimales

- **Date** : 2026-10-28
- **Question** : la règle de choix des mots exige des syllabes réelles, mais
  20 des 77 paires minimales des archives utilisent des syllabes inventées
  (notamment pour les tons glottalisés).
- **Décision** : syllabes inventées **autorisées uniquement à l'étape E3**,
  comme second terme d'une paire minimale, quand aucune paire de mots réels
  n'existe. Elles respectent la structure de la syllabe vietnamienne
  (FOND-02 § 2). Elles sont **seulement entendues, jamais affichées**,
  y compris en fin d'E3 (exception à DEC-0011).
- **Raison** : sans elles, plusieurs contrastes (tons en particulier) ne
  pourraient pas être travaillés ; ne jamais les afficher évite d'ancrer une
  forme écrite qui n'existe pas.
- **Impacte** : FOND-04 § 9, paires minimales dans `04_DONNEES`.

### DEC-0014 — Validation des fondations

- **Date** : 2026-10-28
- **Décision** : FOND-01, FOND-02, FOND-03 et FOND-04 passent au statut
  **VALIDE** (version 1.0), validés par Christophe.

### DEC-0015 — Outils de formation : WordPress pour l'apprentissage, Anki pour les révisions

- **Date** : 2026-10-28
- **Question** : quel outil (ou quelle combinaison) pour diffuser la
  formation ? Besoins : vous d'abord puis d'autres apprenants ; PC,
  Android, iPhone, navigateur ; budget modeste ; mesure de la production
  par la machine.
- **Options étudiées** : A — Anki seul ; B — application web sur mesure ;
  C — Anki + page de prononciation ; D — LMS Moodle ; E — LMS sur WordPress.
- **Constats** (2026-10-28) :
  - Azure Speech jugé peu performant en vietnamien (expérience de
    Christophe) ;
  - le code des cartes Anki n'a pas accès au micro (refus du développeur,
    juin 2025) ;
  - aucun LMS (Moodle ou WordPress) n'offre de vraie révision espacée ;
  - l'analyse de la courbe mélodique fonctionne (test du 2026-10-28 sur
    « ma » juste / faux) et peut tourner dans un navigateur.
- **Décision** :
  - **WordPress + extension LMS** pour l'**apprentissage** : leçons, parcours
    E1 → E5, verrous, volets, et page de **prononciation** (courbe
    mélodique) intégrée au site ;
  - **Anki** pour les **révisions périodiques** (répétition espacée) des
    éléments appris.
- **Raison** : chaque outil fait ce qu'il fait le mieux ; WordPress facilite
  l'intégration d'une page sur mesure (micro) et le partage futur ; Anki
  reste la référence éprouvée et gratuite de la révision espacée.
- **Conséquences à traiter** :
  - choisir l'extension LMS (critère clé : déblocage sur **score minimum**) ;
  - relier les deux outils : les éléments validés dans WordPress sont
    ajoutés aux révisions Anki, générés à partir de la même source
    (`04_DONNEES`) ;
  - définir l'hébergement (développement en local avec Local, puis en ligne).
- **Impacte** : `05_PRODUCTION`, `03_PROGRAMME`, R-VOL-08 (mesure de la
  production : courbe mélodique, reconnaissance vocale plus tard).

### DEC-0016 — WordPress sans extension LMS au départ

- **Date** : 2026-10-28
- **Question** : faut-il une extension LMS (Sensei, LearnDash…) sur
  WordPress ? (précise DEC-0015)
- **Constats** : les quiz des extensions LMS ne documentent pas les questions
  audio A/B sans écrit ; un lecteur d'activités sur mesure est de toute façon
  nécessaire (E1–E5, courbe mélodique) et porte déjà scores, verrous et
  volets ; les prérequis des LMS sont moins précis que les règles du projet.
- **Options** : WordPress + LMS (Sensei) + lecteur ; WordPress seul +
  lecteur + petite extension de progression.
- **Décision** : **WordPress sans LMS au départ** :
  - **pages** WordPress pour la structure (module > leçon) ;
  - **lecteur d'activités** sur mesure pour E1–E5, scores, verrous, volets ;
  - **petite extension** qui enregistre la progression sur le compte
    WordPress (même progression sur PC, téléphone, tablette) ;
  - **Anki** pour les révisions (DEC-0015).
  Un LMS pourra être ajouté au moment du partage s'il apporte un réel gain.
- **Raison** : une seule logique de progression, la vôtre ; plus léger ;
  pas de dépendance à un éditeur d'extension.
- **Impacte** : `05_PRODUCTION/01_architecture_outils.md`.

### DEC-0017 — Format des données : CSV comme source de vérité

- **Date** : 2026-10-28
- **Question** : fichiers CSV, Excel, ou base de données (SQLite,
  PostgreSQL) pour les données de la formation ?
- **Décision** :
  - **source de vérité** : fichiers **CSV** dans `04_DONNEES`, un par table
    (UTF-8, séparateur `;`, conformes à DOC-07) ;
  - **contrôle** : un script charge les CSV dans une base **SQLite
    temporaire** et vérifie liens entre tables, règles « auto » du registre
    et encodage ; rapport dans `07_QUALITE` ;
  - **Excel** : consultation seulement, jamais d'enregistrement (DOC-08) ;
  - **PostgreSQL** : abandonné comme outil de travail ; sa dernière version
    sert de **source de reprise** (export unique), puis reste archivée.
- **Raison** : faible volume (quelques milliers de lignes), suivi ligne à
  ligne par Git, aucun serveur à entretenir ; la rigueur relationnelle est
  apportée par le contrôle automatique.
- **Réexamen** : si plusieurs personnes modifient les données en même temps,
  ou au-delà de quelques dizaines de milliers de lignes.
- **Impacte** : `04_DONNEES`, `05_PRODUCTION` (générateur, script de
  contrôle), `07_QUALITE`.

### DEC-0018 — Un seul code par son (fusion des écritures)

- **Date** : 2026-10-28
- **Question** : les archives donnent plusieurs codes à un même son
  (c/k, g/gh, ng/ngh, i/y) ; à Hanoï, d/gi/r, ch/tr et s/x se prononcent
  aussi pareil (DEC-0009). Fusionner ou garder des codes séparés ?
- **Décision** : **fusionner** : un code par son entendu ; les différentes
  écritures sont listées dans la colonne `spellings` de `sons.csv`.

| Code absorbé | Code conservé | Écritures |
|---|---|---|
| PH-CO-k | PH-CO-c | c, k |
| PH-IN-gh | PH-IN-g | g, gh |
| PH-IN-ngh | PH-IN-ng | ng, ngh |
| PH-VS-y | PH-VS-i | i, y |
| PH-CO-gi, PH-CO-r | PH-IN-d | d, gi, r |
| PH-IN-tr | PH-IN-ch | ch, tr |
| PH-CO-s | PH-IN-x | x, s |

- **Non fusionnés** : les finales -c / -ch et -ng / -nh (la voyelle qui
  précède se prononce différemment : *anh*, *ach*) ; qu (PH-CO-qu, /kw/).
- **Raison** : la règle d'atomicité compte les **sons** entendus ; un même
  son ne doit pas compter pour deux nouveautés. L'orthographe est travaillée
  séparément, en E4–E5 (DEC-0011).
- **Conséquences** : 84 → **76** sons ; lors de la reprise des mots et des
  paires minimales, les codes absorbés sont remplacés par les codes
  conservés (table ci-dessus).
- **Impacte** : `04_DONNEES/sons.csv`, `00_modele_donnees.md`, reprise des
  données.

### DEC-0019 — Les 14 leçons du Module 0 et la place de quelques sons

- **Date** : 2026-10-28
- **Question** : comment appliquer DEC-0006 (tons glottalisés un par un)
  sans mettre deux familles de nouveautés dans une même leçon (R-ATOM-01) ?
  Où placer ê ? Que faire des diphtongues qui contiennent une voyelle pas
  encore vue ?
- **Décision** :
  1. **Une leçon dédiée** par ton glottalisé : le Module 0 passe de 12 à
     **14 leçons** — L03 nặng, L07 hỏi, L11 ngã + contraste hỏi/ngã ;
     L14 = recyclage. Détail dans `04_DONNEES/lecons.csv`.
  2. **ê** passe en **L01** (voyelle avant, proche du « é » français) ; il
     n'est pas une voyelle centrale.
  3. **ơi** passe en **L06** (avec ơ, ư) ; **au** et **ay** passent en **L09**
     (avec ă, â), car ils contiennent ces voyelles.
  4. Par défaut, chaque son et ton s'ouvre **dans la même leçon** en écoute
     et en production (`ouvertures.csv`).
- **Raison** : respect de R-ATOM-01 et de l'atomicité par sons entendus ;
  correction d'erreurs héritées des archives.
- **Impacte** : `04_DONNEES/lecons.csv`, `ouvertures.csv` ; registre
  (R-PROG-01, R-PROG-02, R-ATOM-05, R-REV-03) ; FOND-03 et FOND-04
  (numéros de leçon, à revalider).

### DEC-0020 — Mots supports du Module 0

- **Date** : 2026-10-28
- **Question** : quels mots servent de supports dans chaque leçon du Module 0,
  avec les 14 leçons (DEC-0019) ? Les 84 mots supports des archives étaient
  répartis pour l'ancien ordre (1 seul mot pour L03, L07, L11).
- **Décision** :
  - sélection **automatique** dans `mots.csv` selon R-ATOM-03, R-ATOM-05,
    R-LEX-03 (critère 5) et R-LEX-04, en privilégiant la couverture des
    éléments nouveaux, puis les mots des archives, les monosyllabes et la
    fréquence ;
  - quotas : 10 mots en L01, 7 ailleurs, **plus** 7 mots ajoutés hors corpus
    pour combler des manques : *dạ, bị, lạ* (L03), *pha* (L05), *thư, tư*
    (L06), *tu* (L01) — sens et fréquence **à vérifier** ;
  - **98 mots** au total (≤ 100, R-LEX-02), enregistrés dans
    `04_DONNEES/mots_lecons.csv` ; la colonne `m0_vector` de `mots.csv` est
    supprimée (une seule source).
- **Non couverts** (sons rares) : L06 *ơu, ưi* ; L12 *uơ, uê, uâ* ; L13
  *oeo, uyu, oao, uây, oay* — à travailler par syllabes d'exercice.
- **Source** : `07_QUALITE/proposition_mots_supports_M0.md`.

### DEC-0021 — Pas de transcription phonétique des mots

- **Date** : 2026-10-28
- **Question** : faut-il calculer et afficher la transcription phonétique des
  mots (par exemple *một* → [mot̚˨˩ʔ]) ?
- **Décision** : **non**. Seule la notation phonétique des **sons**
  (`sons.csv`, colonne `ipa`) est conservée et peut être affichée en
  production. Pas de colonne `ipa_main`, pas de transcription des mots.
- **Raison** : la notation des sons suffit à l'élève ; une transcription
  assemblée serait de plus approximative (variations de contexte à Hanoï,
  par exemple *anh*, *sách*).
- **Impacte** : FOND-04 § 7 (à revalider), R-ECR-04, `00_modele_donnees.md`.

### DEC-0022 — Symboles des tons

- **Date** : 2026-10-28
- **Question** : quels symboles utiliser pour représenter les tons ?
- **Décision** : `tons.csv` reçoit trois informations en plus des signes de
  l'écriture et des chiffres Chao :
  - **lettres de ton** de l'alphabet phonétique (norme) : ˧˧ ˧˥ ˨˩ ˧˩˧ ˧ˀ˥ ˨˩ʔ ;
  - **pictogramme** du projet : → (ngang), ↗ (sắc), ↘ (huyền), ↘↗ (hỏi),
    ↗ˀ↗ (ngã, cassé au milieu), ↘ʔ (nặng, arrêt final) ;
  - **couleur** : gris, rouge, bleu, vert, violet, orange.
  Les numéros de ton (1 à 6) ne sont **pas** utilisés (ordre variable selon
  les ouvrages).
- **Règles d'emploi** : symboles affichés seulement là où l'écrit est
  autorisé (fin d'E3, E4, E5 — DEC-0011) ; la couleur n'est **jamais** le seul
  porteur de l'information (toujours avec le pictogramme ou le signe), pour
  les personnes qui distinguent mal les couleurs.
- **Statut des valeurs** : pictogrammes et couleurs **proposés**, à confirmer
  à l'usage.
- **Impacte** : `04_DONNEES/tons.csv`, lecteur d'activités, page de
  prononciation.

### DEC-0023 — Audio : stockage, régénération, variété des voix

- **Date** : 2026-10-28
- **Constats** : les 274 audios de OLD enchaînent « son ; syllabe ; mot » dans
  un même fichier (inutilisables tels quels) ; les 93 audios récents ne
  couvrent que 19 mots (8 des 98 mots supports) ; il faut environ 211
  éléments sonores (mots supports et termes des paires minimales).
- **Décision** :
  1. Les fichiers audio sont des **données sources** : rangés dans
     `04_DONNEES/audio/`, suivis par Git, chacun **écouté et validé**.
  2. **Tout est regénéré** avec des réglages homogènes ; les audios des
     archives ne sont pas repris.
  3. **Au moins 2 voix**, avec pour objectif la **variété** : homme, femme,
     enfant, débits lent, normal et rapide — pour que l'élève entende
     plusieurs prononciations.
  4. Voix de départ (FPT.AI, accent du Nord) : **F1** *banmai*, **F2**
     *thuminh*, **H1** *leminh* (`04_DONNEES/voix.csv`).
- **Points ouverts** :
  - **voix d'enfant** : FPT.AI n'en propose aucune ; source à trouver
    (enregistrements natifs, autre fournisseur) ;
  - **une seule voix masculine** du Nord chez FPT.AI ;
  - **réglages de débit** FPT.AI (échelle −3 à +3) à calibrer à l'écoute.
- **Impacte** : `04_DONNEES` (`voix.csv`, `audios.csv`, `audio/`),
  R-AUD-02, R-AUD-04, `00_modele_donnees.md`.

### DEC-0024 — Images à la place de l'écrit au début

- **Date** : 2026-10-28
- **Question** : comment donner du sens et des choix de réponse sans écrit
  aux étapes d'écoute ?
- **Décision** :
  1. Les mots faciles à imager reçoivent une **image** (pictogramme ou
     dessin, style homogène), utilisable dès E1 ; en E2–E3 les choix de
     réponse sont des images.
  2. Mots sans image et syllabes inventées : **boutons sonores** A / B ou
     **pictogrammes de ton** (DEC-0022).
  3. Sélection des mots supports refaite (option « combiner ») : à
     couverture égale des sons nouveaux, le mot **imageable** est préféré —
     **79 mots imageables sur 98** (contre 48), validée par Christophe ;
     remplace la liste de DEC-0020.
  4. `mots.csv` reçoit une colonne `imageable` (estimation, à corriger) ;
     nouveau fichier `images.csv`, images dans `04_DONNEES/images/`.
  5. Source : licence compatible avec le partage ; **OpenMoji** (CC BY-SA 4.0,
     usage commercial permis) privilégié ; ARASAAC (CC BY-NC-SA, usage
     commercial interdit) à éviter si la formation est un jour vendue.
- **Impacte** : `mots_lecons.csv`, `mots.csv`, `images.csv`, R-PARC-04,
  R-IMG-01/02, FOND-04 (à revalider).

### DEC-0025 — Séries minimales de 2 à 4 termes

- **Date** : 2026-10-28
- **Question** : les « paires » minimales doivent-elles avoir exactement
  2 termes ?
- **Décision** : **2 termes au minimum, 4 au maximum** (mots ou pseudo-mots).
  `paires_minimales.csv` passe au format « une ligne par terme »
  (`series_code`, `position`…). Séries recalculées sur les nouveaux mots
  supports : **79 séries** (35 de 2 termes, 21 de 3, 23 de 4), **225 termes** ;
  hors corpus et hors listes de fréquence → traités comme syllabes
  inventées (DEC-0013), à confirmer. Le terme 1 est toujours le mot support.
- **Complément (même jour)** : ajout de **16 séries pour L01** (contrastes
  o/ô, e/ê, i/ê, đ/d, b/m/v, n/l, -m/-n ; exemples *to/tô*, *đi/di*,
  *ba/ma/va*) → **95 séries**, **260 termes**.
- **Impacte** : `paires_minimales.csv`, R-PARC-05, R-LEX-05, FOND-04.

### DEC-0026 — E2 et E3 utilisent la même série minimale

- **Date** : 2026-10-28
- **Question** : d'où viennent les deux possibilités de E2 ?
- **Options** : A) une **paire minimale** tirée de la série de E3 ;
  B) un contraste large et facile (deux mots très différents).
- **Décision** : **A**. E2 utilise **2 termes** de la série (le mot support
  et un autre terme) ; E3 utilise la **série complète** (2 à 4 termes). La
  difficulté monte par le nombre de choix, sur le même contraste fin.
- **Précision de Christophe** : le contraste ne se limite pas au ton ; il
  peut porter sur des **tons proches** ou des **sons proches** (voyelles,
  consonnes initiales ou finales). Les données le prévoient déjà
  (`contrast_type` = `tone` ou `sound` : 26 séries de tons, 69 de sons).
- **Conséquence** : le hasard donne 50 % de réussite en E2 et 25 % à 33 %
  en E3 ; le seuil d'E3 (85 %) est donc plus exigeant, à réévaluer à l'usage.
- **Point ouvert** : 52 séries sur 95 n'ont qu'**un seul mot réel** ; leur
  paire E2 contiendrait une syllabe hors corpus, aujourd'hui interdite
  hors E3 (R-LEX-05). Arbitrage à prendre.
- **Impacte** : R-PARC-04, R-PARC-05, FOND-04 § 3.

### DEC-0027 — Termes hors corpus et syllabes inventées en E2

- **Date** : 2026-10-28
- **Question** : point ouvert de DEC-0026 : 52 séries n'avaient qu'un mot
  réel, et la syllabe inventée était interdite hors E3.
- **Décision** : 1) **vérifier** les termes hors corpus dans des
  dictionnaires ; 2) pour les séries qui restent sans paire réelle,
  **autoriser la syllabe inventée en E2** aussi, présentée par des boutons
  sonores (pas d'image, jamais affichée).
- **Critère** : un terme présent dans **au moins 2 des 3 dictionnaires**
  (Hồ Ngọc Đức, Từ điển tiếng Việt, Wiktionnaire) est un mot réel.
- **Résultat** : 107 termes vérifiés → 74 réels, 33 inventés ; séries sans
  paire réelle : **52 → 9** (toutes des contrastes de son).
- **Remplace** : la restriction « uniquement en E3 » de DEC-0013.
- **Impacte** : `paires_minimales.csv`, R-LEX-05, FOND-04 § 9,
  DATA-MODELE, QUAL-VERIF-HORS-CORPUS-20261028.

### DEC-0028 — Étiquettes de réponse en E2–E3 : images, puis symboles

- **Date** : 2026-10-28
- **Question** : en E2–E3, l'élève répond-il en touchant des images ou des
  symboles ?
- **Options** : a) images ; b) symboles ; c) images, puis symboles.
- **Décision** : **c**. Au **débit lent**, chaque choix montre l'**image et
  le symbole** ; au **débit normal** (là où se mesure le verrou), le choix
  est le **symbole seul**, l'image restant visible en petit pour le sens.
  Le passage se fait au même moment que celui du débit (seuil atteint au
  débit lent).
- **Symboles** : tons → pictogramme et couleur de `tons.csv` (DEC-0022) ;
  sons → *à préciser*.
- **Raison** : méta-analyse de Uchihara, Karas et Thomson (2025) : effet
  plus faible avec des images comme étiquettes (g = 0,47) qu'avec des
  symboles ou l'écrit (0,90 à 1,03). Comparaison indirecte, donc indice.
- **Complète** : DEC-0024 (les images restent pour le sens).
- **Impacte** : PROG-ACT, R-PARC-04, FOND-04 § 7 bis.

### DEC-0029 — Symbole des sons en E1–E3 ; pictogrammes de ton dès E1

- **Date** : 2026-10-28
- **Question** : quel symbole sert d'étiquette de réponse pour les sons
  (DEC-0028, « à préciser ») ? Et que devient la règle de DEC-0022, qui
  limitait les symboles de ton aux étapes où l'écrit est autorisé ?
- **Options** : 1) symbole phonétique (`ipa`) ; 1 restreinte) symbole
  phonétique **court** (`ipa_main`) du seul son mis en contraste ;
  2) pictogramme maison ; 3) lettre vietnamienne ; 4) pas de symbole.
- **Décision** : **1 restreinte**.
  1. L'étiquette d'un son est la valeur `ipa_main` de `sons.csv`, entre
     barres obliques (ex. /ə/ contre /o/ pour ơ / ô). La notation complète
     (`ipa`) n'est pas utilisée comme étiquette.
  2. Seul le **son mis en contraste** dans la série est affiché, pas le mot
     entier : ce n'est pas une transcription de mot (DEC-0021 tient).
  3. Le symbole est **présenté en E1, avec son audio** (Découverte, Écoute
     contrastée), pour être appris comme une étiquette sonore et non lu.
  4. Les symboles qui ressemblent à une lettre française (/u/, /e/, /o/,
     /i/, /a/…) reçoivent une **mise en garde** à leur première apparition
     (ex. /u/ se dit « ou », pas le « u » de *lune*).
  5. **Pictogrammes et couleurs de ton** (DEC-0022) autorisés **dès E1** ;
     les **signes de l'écriture** (◌́, ◌̀…) restent réservés aux étapes où
     l'écrit est permis (DEC-0011).
- **Raison** : une seule notation de E2 à E5 ; pas de symboles arbitraires à
  inventer ; respecte « pas d'écrit en E1–E2 ». Charge acceptée : quelques
  symboles nouveaux (ə, ɨ, ɛ, ɔ, ŋ, ɲ, ɗ, ɓ…). Le risque de lecture à la
  française subsiste pour les symboles identiques à des lettres françaises,
  d'où la mise en garde.
- **Remplace** : dans DEC-0021, la phrase « pas de colonne `ipa_main` »
  (la colonne existe dans `sons.csv` et sert désormais d'étiquette) et la
  limite « en production » pour la notation des sons ; dans DEC-0022, la
  règle « symboles affichés seulement là où l'écrit est autorisé ».
- **Complète** : DEC-0028.
- **Point à vérifier** : quelles étiquettes la méta-analyse range sous
  « symboles » (alphabet phonétique ou autre) ; à relire dans l'article.
- **Impacte** : PROG-ACT, R-PARC-04, R-ECR-04, FOND-04 § 7 bis,
  `sons.csv` (colonne `ipa_main` à relire, triphtongues comprises).

### DEC-0030 — Lecteur d'activités développé d'abord en site statique

- **Date** : 2026-10-28
- **Question** : faut-il développer le lecteur d'activités directement dans
  WordPress (DEC-0016), ou sous une autre forme ? (précise DEC-0016)
- **Options** : W — WordPress + extension de progression (DEC-0016) ;
  S1 — site statique, progression dans l'appareil ; S2 — site statique +
  comptes Firebase. Supabase écarté (offre gratuite mise en pause après une
  semaine d'inactivité).
- **Constats** (2026-10-28) :
  - le lecteur d'activités et la page de prononciation (environ 80 % du
    travail) sont identiques dans toutes les options ;
  - un site statique est plus facile à développer et à tester par l'IA
    (un seul langage, essais sans WordPress, moins de manipulations pour
    Christophe) ;
  - Christophe a l'habitude de WordPress ; il accepte, si besoin, que la
    progression soit enregistrée chez Google (Firebase).
- **Décision** :
  1. Le lecteur d'activités et la page de prononciation sont **développés et
     testés comme un site statique**, la progression étant enregistrée
     **dans l'appareil**.
  2. L'**enveloppe définitive** (WordPress ou Firebase) est choisie **quand
     le lecteur fonctionne**.
  3. Dans les deux cas : contenus **générés** depuis `04_DONNEES` et suivis
     par Git, jamais saisis dans l'outil ; enregistrement de la progression
     **isolé** dans une seule partie du code, remplaçable.
  4. Anki reste l'outil des révisions (DEC-0015).
- **Raison** : commencer par ce qui sert dans tous les cas, au plus simple ;
  garder le choix de l'enveloppe ouvert sans travail perdu.
- **Précise** : DEC-0016 (WordPress n'est plus acquis ; il reste une des deux
  enveloppes possibles).
- **Impacte** : PROD-ARCH, `05_PRODUCTION` ;
  `05_PRODUCTION/comparaison_wordpress_application_web_2026-10-28.md`.

### DEC-0031 — Sons sans mot support : 2 gardés, 9 reportés en A1–A2

- **Date** : 2026-10-28
- **Question** : 11 sons ouverts en Module 0 n'avaient ni mot support ni
  série minimale ; or E1 et E4 exigent des mots réels (R-LEX-05). Que
  faire ? (point P1 de PROG-M0)
- **Options** : A — tout reporter en A1–A2 ; B — garder **uy** et **uyê**
  avec un mot fréquent, reporter les 9 autres ; C — comme B, avec *chuyên*
  (rang 626) au lieu de *chuyện*.
- **Décision** : **B**.
  1. **uy** (L04) : mot support *tuy* (« bien que », rang 359, déjà dans
     `mots.csv`) ; série S0096 *tuy / tu*.
  2. **uyê** (L12) : mot support ***chuyện*** (« histoire, affaire »),
     ajouté à `mots.csv` (W0339) et `syllabes.csv` ; série S0097
     *chuyện / chiện\** (syllabe inventée présumée, à vérifier).
  3. **Reportés en A1–A2** : ơu, ưi (L06) ; uê, uơ (L12) ; oao, oay, oeo,
     uây, uyu (L13). Retirés de `ouvertures.csv` ; marqués « reporté en
     A1–A2 » dans la colonne `note` de `sons.csv`. Leur leçon d'ouverture
     sera fixée dans la progression de A1 ou A2.
- **Résultat** : 100 mots supports (limite de R-LEX-02), 97 séries,
  264 termes ; 67 sons et 6 tons enseignés en M0 ; contrôle d'atomicité
  sans violation ; tous les éléments ouverts ont un mot ou une série.
- **À vérifier** : fréquence de *chuyện* (R-LEX-03, liste de R-LEX-07) ;
  statut de *chiện* dans les 3 dictionnaires (DEC-0027).
- **Raison** : *tuy* et *chuyện* sont utiles pour la suite ; les 9 sons
  reportés sont rares et seront mieux appris dans des mots qui servent.
- **Impacte** : `mots.csv`, `syllabes.csv`, `mots_lecons.csv`,
  `paires_minimales.csv`, `ouvertures.csv`, `sons.csv` ; R-ATOM-06 ;
  DATA-MODELE ; PROG-M0.

### DEC-0032 — Verrou d'écoute : un minimum de réussites par série

- **Date** : 2026-10-28
- **Question** : le score d'E2 et E3 porte sur les 20 dernières réponses,
  toutes séries mêlées. Dans une leçon de 16 séries (L01), une série
  difficile peut n'être jamais vérifiée. Faut-il compléter ce calcul ?
  (point P2 de PROG-M0)
- **Options** : A — garder le score mêlé seul ; B — score mêlé **et**
  minimum de réussites par série ; C — score séparé par série (85 % sur ses
  10 dernières réponses).
- **Décision** : **B**. Le verrou d'écoute d'E2 et d'E3 exige, en plus du
  seuil sur les 20 dernières réponses (R-VOL-05) : **chaque série** de la
  leçon a été réussie au moins **2 fois** au **débit normal** (paramètre).
- **Raison** : chaque contraste est vérifié au moins un peu, sans allonger
  beaucoup le volet écoute ; l'option C demanderait au moins 160 réponses
  justes en L01, alors que les gains plafonnent vers 400 minutes
  d'entraînement au total (Uchihara, Karas et Thomson, 2025).
- **Impacte** : R-VOL-05, PROG-ACT, PROG-M0, lecteur d'activités.

### DEC-0033 — Ordre des termes dans les séries minimales

- **Date** : 2026-10-28
- **Question** : quel terme sert de second choix en E2 ? (point P3 de
  PROG-M0)
- **Décision** :
  1. **Convention** : position 1 = mot support ; **position 2 = contraste
     principal** de la leçon. La paire d'E2 est position 1 / position 2.
     Quand la leçon oppose le nouveau ton à deux tons connus (L07 : huyền
     puis nặng ; L11 : sắc puis hỏi, DEC-0006), E2 se fait en deux temps :
     position 1 / 2, puis position 1 / 3.
  2. **Séries réordonnées** : S0026 (L03 : huyền en position 2) ; S0081,
     S0082, S0086 (L11 : sắc en position 2, hỏi en position 3).
  3. **Séries complétées** (4 termes au plus) : S0084 *cũng / cúng / củng /
     cùng* (*củng*, hỏi, remplace *cung*) ; S0085 *nghĩ / nghí\* / nghỉ /
     nghị* (*nghí*, syllabe inventée présumée, sắc, remplace *nghi*).
- **À vérifier** : *củng* et *nghí* dans les 3 dictionnaires (DEC-0027).
- **Raison** : appliquer l'ordre de DEC-0006 dans le lecteur sans
  sélection manuelle ; le générateur lit la position.
- **Impacte** : `paires_minimales.csv`, DATA-MODELE (colonne `position`),
  R-PARC-04, PROG-M0.

### DEC-0034 — L01 reste une seule leçon

- **Date** : 2026-10-28
- **Question** : faut-il couper L01 (21 éléments, 16 séries) en deux
  leçons ? (point P4 de PROG-M0)
- **Constat** : selon Christophe, les sons et le ton de L01 sont ceux du
  français. Vérification : vrai pour la plupart ; écarts réels pour **h**
  (muet en français), **ê / e** et **ô / o** (confondus par beaucoup de
  francophones du Sud de la France), les finales **-m / -n** (risque de
  nasaliser la voyelle), les implosives **b, đ** (écart faible) et le ton
  **ngang** (la hauteur fait partie du mot).
- **Options** : A — une seule leçon ; B — deux leçons (15 leçons au total,
  renumérotation).
- **Décision** : **A**. Ordre interne : voyelles → consonnes → finales.
  L01 sert aussi de **test d'entrée** : si une série ne se valide pas vite,
  le contraste est moins évident que prévu.
- **Réexamen** : couper L01 si l'usage la montre trop longue.
- **Raison** : sons de difficulté 4 (FOND-03), verrou par série (DEC-0032),
  pas de renumérotation.
- **Impacte** : PROG-M0.

### DEC-0035 — Critère de fréquence : « mot courant » en Module 0

- **Date** : 2026-10-28
- **Question** : R-LEX-03 exige des mots parmi les 500 plus fréquents ; le
  contrôle du 2026-10-28 montre que **46 mots supports sur 100** ne
  respectent pas ce critère (26 sans rang dans `mots.csv`, dont *cơm, gà,
  mười, điện thoại* ; 20 au-delà de 500, dont *uống, bàn, áo, đọc*).
  (point P5 de PROG-M0)
- **Options** : A — 500 strict (46 mots à remplacer) ; B — seuil de 2 000
  sur une liste à fixer ; C — « mot courant » en Module 0, fréquence à
  partir de A1.
- **Décision** : **C**. En Module 0, le critère 3 devient « mot **courant**
  de la vie quotidienne », vérifié par relecture ; le critère de fréquence
  s'applique à partir de A1, sur la liste de référence à fixer (R-LEX-07).
  Les rangs restent dans `mots.csv` à titre d'information.
- **Raison** : en Module 0, le mot est un support sonore, pas du vocabulaire
  (R-LEX-01) ; la liste importée est incomplète (rangs manquants pour des
  mots très courants).
- **À faire** : relire une fois les 100 mots supports (« courant ? ») ;
  cas douteux signalé : *tu* (« pratiquer une religion »).
- **Impacte** : R-LEX-03, FOND-04 § 9 (revalidé), PROG-M0.

### DEC-0036 — Seuils des finales : 85 % par leçon, 80 % en sortie

- **Date** : 2026-10-28
- **Question** : les verrous de L08 et L10 sont à 85 % (DEC-0012), l'objectif
  de sortie du Module 0 pour les finales à 80 % (FOND-01 § 6.1). Faut-il
  aligner ? (point P6 de PROG-M0)
- **Options** : A — garder les deux ; B — tout à 85 % ; C — tout à 80 %.
- **Décision** : **A**. 85 % pour le verrou d'écoute de L08 et L10 ; 80 %
  pour la sortie du Module 0, mesurée en L14.
- **Raison** : en L14, les finales sont mêlées à tous les contrastes, ce qui
  est plus difficile qu'une leçon isolée ; pas de modification de FOND-01.
  Valeurs paramétrables.
- **Impacte** : PROG-M0 § 4.

### DEC-0037 — L01 en deux parties dans le lecteur

- **Date** : 2026-10-29
- **Question** : comment raccourcir les séances de L01 (16 séries) ?
  (précise DEC-0034)
- **Options** : 1 — deux vraies leçons (15 leçons, renumérotation de 4
  fichiers de données et d'une dizaine de documents, DEC-0019 remplacée) ;
  2 — une seule leçon, présentée en deux parties.
- **Décision** : **2**. L01 reste une leçon (DEC-0019, DEC-0034 tiennent) ;
  le lecteur la présente en deux parties, faites l'une après l'autre, chacune
  avec E1 → E3, son verrou et sa révélation de l'écrit :
  - **partie A, voyelles** : les 8 séries dont le contraste porte sur le
    noyau ;
  - **partie B, consonnes et finales** : les 8 autres.
  L'écoute de la leçon est validée quand les deux parties le sont.
- **Données** : colonne `split_parts` dans `lecons.csv` (`true` pour L01) ;
  le partage suit la place du son contrasté (`sons.csv`, colonne
  `position`).
- **Raison** : séances plus courtes et première étape franchie plus tôt, sans
  renumérotation. Applicable plus tard à d'autres leçons si l'usage le
  montre.
- **Impacte** : `lecons.csv`, DATA-MODELE, PROG-M0 (fiche L01), lecteur
  d'activités (PROD-LECT).

### DEC-0038 — Mots repères, catégories de sons et chemins de prononciation

- **Date** : 2026-10-29
- **Question** : le symbole phonétique seul ne suffit pas pour apprendre le
  symbole (remarque de Christophe après l'essai de L01). Quelle aide donner ?
- **Décision** :
  1. **Mot repère** pour chaque symbole de son : un mot **français** quand le
     son existe en français (25 symboles, dont 2 « proches » : /ɓ/, /ɗ/) ;
     sinon un mot **vietnamien** illustré de la leçon (29), montré en
     image seulement (pas d'écrit en E1–E2) ; à défaut, symbole seul (5).
  2. **Catégorie** de chaque son, indiquée par une couleur **et** une
     marque : **=** son du français, **≈** son proche, **★** son nouveau.
     Couleurs choisies hors de la palette des tons (DEC-0022).
  3. **Indice d'écoute** d'une ligne pour chaque symbole (E1–E3).
  4. **Chemin de prononciation** pour les 36 sons absents ou proches du
     français, pour E4 : son français de départ, **un seul** changement
     (lèvres, langue, gorge, souffle, durée) ou **décomposition** des
     diphtongues et triphtongues, puis vérification.
  5. **Affichage** : repère, catégorie et indice en E1 ; repère et catégorie
     en petit en E2–E3 au débit lent ; **symbole seul** au débit normal, où
     se mesure le verrou (DEC-0028).
- **Données** : `04_DONNEES/reperes_sons.csv` (source unique) ; remplace
  `05_PRODUCTION/lecteur/indications_symboles.csv`.
- **À vérifier** : trois descriptions marquées « à vérifier » (finale -ch,
  g /ɣ/, ch /c/), par un natif ou un ouvrage ; images provisoires (emoji).
- **Précision** : dans les diphtongues, la lettre finale o / u se dit « ou »
  bref et i / y se dit « i » bref (*mèo* = mè + « ou » bref).
- **Raison** : partir de ce que l'apprenant connaît ; ne pas créer de faux
  équivalents pour les sons nouveaux (FOND-03, transferts) ; une seule
  nouveauté à la fois, y compris dans le geste de prononciation.
- **Impacte** : DATA-MODELE, PROG-ACT (E1, E2, E4), lecteur d'activités.

### DEC-0039 — E1 : découverte de chaque son seul, sans écoute contrastée

- **Date** : 2026-10-29
- **Question** : en E1, le lecteur faisait entendre les termes d'une série
  côte à côte (*xem* / *xêm*), avec toutes les voix mêlées. Christophe,
  après essai : cela prête à confusion ; en E1 on doit seulement
  « s'imprégner de ce qui est juste », les différences viennent en E2.
- **Options** : (A) chaque son seul, dans plusieurs mots ; (B) seulement le
  mot support de chaque série. Pour les mots : règle stricte (sons tous déjà
  vus) ou souple (ton déjà vu, autres sons libres).
- **Décision** :
  1. E1 = **ACT-E1-DECOUV seule** : un écran par son (ou ton) des séries de
     la leçon (ou de la partie, DEC-0037), avec son symbole, sa catégorie,
     son mot repère et son indice d'écoute (DEC-0038).
  2. **ACT-E1-CONTRA est supprimée** : aucune opposition entre sons en E1 ;
     la première opposition est la paire d'E2.
  3. Chaque son est entendu dans **3 mots au plus**, mots du corpus d'une
     syllabe, choisis par **règle souple** : le **ton** du mot est déjà
     ouvert à l'écoute ; les autres sons sont libres. Priorité au mot
     support de la série, puis à des mots dont le **début varie** (la
     voyelle, pour un son de début), du plus fréquent au moins fréquent.
  4. Chaque mot est dit par **une voix de femme puis une voix d'homme**,
     au **débit normal** ; un bouton « Plus lentement » passe au débit lent.
     Paires de voix alternées : F1 + H3, F3 + H4, F3 + H3 (F1 seule
     depuis DEC-0048).
- **Précision** (2026-10-29, demande de Christophe) : le bouton « Plus
  lentement » est remplacé par **deux boutons d'écoute**, « ▶ Écouter »
  (débit normal) et « 🐢 Écouter lentement » (débit lent) ; et l'élève
  choisit la voix : « Femme et homme » (par défaut), « Femme » ou « Homme ».
- **Données** : `04_DONNEES/exemples_e1.csv`, produit par
  `05_PRODUCTION/tools/choisir_exemples_e1.py` (305 mots pour 111 sons, le
  2026-10-29) ; corrigeable à la main. Audios : 326 fichiers de plus.
- **Limite** : la règle souple fait entendre en E1 des sons pas encore
  étudiés (*năm*, *cơm*…) ; ils ne sont ni montrés ni expliqués.
  Quelques sons n'ont qu'un ou deux mots (b, u, iu, oa, oe, uy…).
- **Raison** : écouter d'abord un modèle juste et varié (plusieurs mots,
  plusieurs voix), sans risque de confondre ; l'identification avec
  correction (E2–E3) est ce qui fait progresser (méta-analyse citée dans
  PROG-ACT).
- **Remplace** : la partie « écoute contrastée » de l'E1 décrite dans
  PROG-ACT et PROG-M0.
- **Impacte** : R-PARC-03, PROG-ACT, PROG-M0, DATA-MODELE, lecteur, audios.

### DEC-0040 — Voix et modèles de synthèse retenus (FPT AI Marketplace)

- **Date** : 2026-10-29
- **Question** : quelles voix du Nord, quel modèle, quel réglage, pour les
  audios de la formation (DEC-0023) ?
- **Constats** (écoute de Christophe et mesures) : avec FPT.TTS-pro, les voix
  d'homme Quang Anh et Viet Khoa avalent la consonne de départ d'un mot
  isolé (*xem* : syllabe d'environ 0,25 s, « x » absent) ; avec
  FPT.AI-VITs, Le Minh, Huy Phong et Minh Quan sont claires en mot seul ;
  les niveaux sonores diffèrent (Huy Phong environ 5 dB plus faible).
- **Décision** :
  1. **Deux femmes et deux hommes** : F1 Ban Mai (FPT.TTS-pro, voix
     modèle), F3 Thu Minh, H3 Le Minh, H4 Huy Phong (FPT.AI-VITs). Quang
     Anh (H1), Viet Khoa (H2) et Minh Quan (H5) sont écartés.
  2. Mot envoyé **seul** (le doublement « mot, mot. » puis découpage reste
     disponible en option).
  3. **Débit lent** propre à chaque voix : F1 0,7 ; F3, H3, H4 0,6
     (débit normal : 1).
  4. **Volume égalisé** : niveau de parole −20 dBFS, crête ≤ −1 dBFS ;
     fichier reçu de FPT conservé dans `audio/_bruts/`.
- **Données** : `voix.csv` (colonnes `provider_model`,
  `provider_speed_slow`) ; détails dans PROD-AUDIO.
- **Impacte** : DATA-MODELE, PROD-AUDIO, lecteur (voix).

### DEC-0041 — E2 : échauffement « Pareil ou différent ? » non noté

- **Date** : 2026-10-29
- **Question** : Christophe propose qu'en E2 l'élève entende deux mots et
  dise seulement s'ils ont le même son : marche plus douce après E1
  (DEC-0039), où aucune différence n'est encore entendue.
- **Options** : (A) E2 entièrement « même / différent » ; (B) échauffement
  « même / différent » non noté, puis le « Lequel ? » à 2 choix ;
  (C) sans changement.
- **Décision** : **B**.
  1. Au début de l'E2 de chaque partie, **10 paires** « Pareil ou
     différent ? » : deux termes de la paire d'E2 (positions 1 et 2), débit
     lent ; autant de paires pareilles que différentes, dans un ordre au
     hasard.
  2. Les deux mots d'une paire sont dits par **deux voix différentes**,
     même quand ils sont pareils : l'élève juge le son, pas l'enregistrement.
  3. Correction simple (juste / faux), puis les deux termes sont montrés
     (image et symbole) et peuvent être réécoutés.
  4. **Non noté, hors verrou** : rien n'entre dans le score ni dans la
     validation d'E2, qui reste le « Lequel ? » (identification).
  5. L'échauffement peut être refait à tout moment (« Pareil ou
     différent ? » sur l'étape E2) ; une E2 déjà commencée le saute.
- **Raison** : l'identification (« Lequel ? ») fait mieux progresser que la
  discrimination « même / différent » (g = 0,95 contre 0,57, méta-analyse
  citée dans PROG-ACT) ; elle reste donc l'exercice qui valide. La
  discrimination, plus facile, sert seulement de transition.
- **Remplace** : l'abandon complet du « même / différent » noté dans
  PROG-ACT (§ 4) est assoupli pour cet échauffement seulement.
- **Impacte** : PROG-ACT, R-PARC-04, lecteur.

### DEC-0042 — Indiquer la place du son : début, fin, voyelle, ton

- **Date** : 2026-10-29
- **Question** : en E2, Christophe ne savait pas s'il fallait comparer la
  consonne du début ou celle de la fin (*xem* / *xen* : finale ; *nên* /
  *lên* : début). Le symbole seul ne le dit pas (/m/ sert pour *ma* et
  pour *xem*).
- **Décision** :
  1. Chaque symbole de **consonne** porte une marque de place :
     **« début ▸ »** ou **« ◂ fin »**, partout (E1, échauffement, E2, E3,
     aux deux débits).
  2. En E1, l'en-tête précise : « consonne en début de mot », « consonne
     en fin de mot » ou « voyelle ».
  3. En E2 (échauffement compris) et E3, une consigne dit **quoi
     écouter** : « Écoutez la consonne du début du mot », « … de la fin du
     mot », « Écoutez la voyelle (le milieu du mot) », « Écoutez le ton (la
     mélodie du mot) ».
- **Données** : colonne `position` de `sons.csv` (initial, nucleus, final) ;
  aucun nouveau fichier.
- **À traiter** : les mots repères (DEC-0038) sont attachés au symbole, donc
  partagés par le début et la fin : pour **-m** et **-n** finals, le repère
  est « miel » / « neige », où le son est au début. Un repère propre aux
  finales est à choisir.
- **Raison** : une seule chose à écouter à la fois, nommée clairement
  (principe d'atomicité) ; éviter qu'un échec vienne de la consigne et non
  de l'oreille.
- **Impacte** : PROG-ACT, lecteur.

### DEC-0043 — Leçons de tons : jamais d'audio lent

- **Date** : 2026-10-29
- **Question** : Christophe, à l'écoute : dans les leçons de tons, le débit
  lent rend la mélodie (le ton) moins perceptible.
- **Décision** : dans les leçons de tons (`is_tone_lesson`, L02, L03, L07,
  L11), tous les audios sont joués au **débit normal** : E1 (pas de bouton
  « Écouter lentement »), échauffement « Pareil ou différent ? », E2 et E3.
  Les deux phases d'E2–E3 restent : d'abord **images et symboles**, puis
  **symboles seuls** (DEC-0028) ; le seuil se mesure de la même façon.
- **Non changé** : les audios lents de ces mots restent générés (beaucoup
  servent aussi dans des leçons de sons) ; ils ne sont simplement pas joués
  dans les leçons de tons.
- **Raison** : le ralenti de la synthèse étire et aplatit le contour
  mélodique ; or c'est lui qu'il faut entendre.
- **Remplace** : pour les leçons de tons seulement, le passage « débit lent
  puis débit normal » de R-VOL-05 à 07 devient « images puis symboles ».
- **Impacte** : PROG-ACT, lecteur.

### DEC-0044 — L01 : le son i n'est plus un contraste

- **Date** : 2026-10-29
- **Question** : Christophe, à l'essai de L01 : inutile de faire distinguer
  **i** en E1 et E2, aucun son proche ne le menace (son identique au
  français, « i » de « lit »).
- **Décision** : dans L01, i n'est plus opposé à aucun son :
  - série **S0010** (*đi* / *đê*) supprimée ;
  - série **S0013** (*pin* / *pên*\*) supprimée ;
  - série **S0004** : terme *nin*\* retiré, la série garde *nên* / *nen*\*
    (ê / e).
  L01 passe de 16 à **14 séries** (partie A : 6 séries, 5 sons en E1 ;
  partie B inchangée). Les mots *đi* et *pin* restent en L01 pour d'autres
  contrastes (đ / d, -n / -m).
- **Non changé** : i reste un point de comparaison là où il est proche d'un
  son nouveau : *iu* (L04), *ư* (L06), *iê* (L12). Il reste ouvert en L01
  dans `ouvertures.csv` (il peut figurer dans les mots).
- **À examiner** (même logique) : **u** en L01 (*mun* dans S0007, série
  S0016 *tu* / *tô*), autre son identique au français.
- **Raison** : ne faire distinguer que ce qui risque d'être confondu ; un
  contraste trop facile allonge la leçon sans rien apprendre.
- **Données** : `paires_minimales.csv` (5 lignes retirées),
  `exemples_e1.csv` regénéré.
- **Impacte** : PROG-M0 (fiche L01), lecteur, audios (fichiers de *nin*,
  *đê*, *pên* devenus inutiles, sans gêne).

### DEC-0045 — Leçons de tons : une seule voix d'abord, plusieurs ensuite

- **Date** : 2026-10-29
- **Question** : Christophe : pour les tons, il vaut mieux distinguer et
  opposer avec la **même voix** ; plusieurs voix ensuite, pour rendre
  l'exercice plus difficile.
- **Décision** (leçons `is_tone_lesson` seulement) :
  1. Échauffement « Pareil ou différent ? » : les deux mots sont dits par
     la **même voix**, la voix modèle F1 (exception à DEC-0041, point 2).
  2. E2 et E3, phase **« avec images »** : **une seule voix**, F1.
  3. E2 et E3, phase **« symboles seuls »** : voix tirées au hasard parmi
     les 4, comme avant ; le verrou (≥ 2 voix, R-VOL-05) s'y mesure.
  4. E1 inchangée : l'élève choisit femme, homme ou les deux (DEC-0039).
- **Raison** : un ton est une mélodie **relative** à la voix de celui qui
  parle ; changer de voix d'un mot à l'autre ajoute un écart de hauteur qui
  n'est pas le ton. On apprend d'abord la forme avec une voix, puis on la
  reconnaît malgré la variété des voix (variabilité, HVPT).
- **Impacte** : PROG-ACT, R-AUD-02 (exception pour la première phase des
  leçons de tons), lecteur.

### DEC-0046 — Repères des finales -m et -n ; u gardé en L01

- **Date** : 2026-10-29
- **Question** : suites de DEC-0042 (repère « miel » / « neige » trompeur
  pour une finale) et de DEC-0044 (faut-il aussi retirer **u** des
  contrastes de L01 ?).
- **Décision** (Christophe) :
  1. Repères propres aux finales : **-m** → « pomme » 🍎, **-n** → « laine »
     🧶, avec l'indice « sans voyelle après ». Les débuts gardent « miel »
     et « neige ». Les autres finales (-p, -t, -c, -ch, -ng, -nh) gardent
     leur repère vietnamien.
  2. **u reste** un contraste en L01 (*tu* / *tô*, *môn* / *mon*\* / *mun*).
- **Données** : `reperes_sons.csv`, lignes `-m` et `-n` ; le générateur du
  lecteur les prend en priorité pour une consonne finale.
- **Impacte** : DATA-MODELE, lecteur.

### DEC-0047 — Mode test : afficher ce qui est joué

- **Date** : 2026-10-30
- **Question** : pendant la phase d'essai, Christophe veut savoir, à chaque
  son, quel fichier est joué, quel personnage parle, homme ou femme, à
  quelle vitesse et avec quel modèle FPT.
- **Décision** : le lecteur affiche en bas de l'écran une **bande
  d'information** mise à jour à chaque son : chemin du fichier (ou « aucun
  fichier : voix de synthèse »), nom du personnage, femme / homme, code de
  voix et identifiant FPT, débit et valeur `speed`, modèle FPT. Activée par
  défaut ; réglage « Infos de test sur le son » pour la masquer.
- **Précision** (même jour, demande de Christophe) : l'information est notée
  **dans la case du mot joué** et non dans une bande en bas de l'écran ; une
  ligne par voix (fichier ; personnage · F/H · code ; modèle · débit ·
  `speed`). En E2, E3 et à l'échauffement, elle n'apparaît **qu'après la
  réponse** (le nom du fichier trahirait la bonne réponse).
- **Limite** : la valeur `speed` et le modèle affichés sont ceux de
  `voix.csv` **au moment de la génération du lecteur** ; ils ne sont pas
  enregistrés dans le fichier audio lui-même. Un fichier produit avec un
  ancien réglage afficherait le réglage actuel.
- **À décider** : désactiver cette bande par défaut avant d'ouvrir la
  formation à d'autres apprenants.
- **Impacte** : lecteur, PROD-AF-LECT.

### DEC-0048 — Voix F3 (Thu Minh) écartée

- **Date** : 2026-10-30
- **Question** : après écoute des audios générés, toutes les voix retenues
  par DEC-0040 sont-elles de qualité suffisante ?
- **Constat** (écoute de Christophe) : F3 Thu Minh est **la moins bonne des
  voix**.
- **Décision** :
  1. F3 passe au statut `inactive` dans `voix.csv` : le lecteur et le
     script de génération ne la prennent plus en compte. Remplace DEC-0040,
     point 1, pour F3.
  2. Voix actives : **F1 Ban Mai** (femme, voix modèle), **H3 Le Minh** et
     **H4 Huy Phong** (hommes).
  3. Mots d'exemple d'E1 (DEC-0039, point 4) : la voix de femme est
     toujours F1 ; paires F1 + H3, F1 + H4, F1 + H3.
  4. Les fichiers F3 déjà produits restent dans `04_DONNEES/audio/` et dans
     `audios.csv` (rien n'est supprimé) ; ils sont simplement ignorés.
- **Conséquences** : une seule voix de femme. Le verrou « ≥ 2 voix »
  (R-VOL-05) reste atteignable avec 3 voix. La variété des voix en phase
  « symboles seuls » (DEC-0045) est moindre.
- **À décider** : chercher une deuxième voix de femme du Nord (autre voix
  FPT ou enregistrement).
- **Impacte** : `voix.csv`, `exemples_e1.csv`, `choisir_exemples_e1.py`,
  PROD-AUDIO, PROD-LECT, PROG-M0, lecteur.

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
| 1.7 | 2026-10-28 | Ajout de DEC-0010 (vocabulaire, étapes E1–E5), DEC-0011 (écrit), DEC-0012 (seuils). |
| 1.8 | 2026-10-28 | Ajout de DEC-0013 (syllabes inventées) et DEC-0014 (validation des fondations). |
| 1.9 | 2026-10-28 | Ajout de DEC-0015 (WordPress pour l'apprentissage, Anki pour les révisions). |
| 1.10 | 2026-10-28 | Ajout de DEC-0016 (WordPress sans LMS au départ). |
| 1.11 | 2026-10-28 | Ajout de DEC-0017 (CSV comme source de vérité). |
| 1.12 | 2026-10-28 | Ajout de DEC-0018 (un seul code par son). |
| 1.13 | 2026-10-28 | Ajout de DEC-0019 (14 leçons, place de ê, ơi, au, ay). |
| 1.14 | 2026-10-28 | Ajout de DEC-0020 (98 mots supports du Module 0). |
| 1.15 | 2026-10-28 | Ajout de DEC-0021 (pas de transcription des mots). |
| 1.16 | 2026-10-28 | Ajout de DEC-0022 (symboles des tons). |
| 1.17 | 2026-10-28 | Ajout de DEC-0023 (audio : stockage, régénération, variété des voix). |
| 1.18 | 2026-10-28 | Ajout de DEC-0024 (images) et DEC-0025 (séries minimales de 2 à 4 termes). |
| 1.19 | 2026-10-28 | Ajout de DEC-0026 (E2 et E3 sur la même série minimale). |
| 1.20 | 2026-10-28 | Ajout de DEC-0027 (termes hors corpus vérifiés ; syllabe inventée permise en E2). |
| 1.21 | 2026-10-28 | Ajout de DEC-0028 (étiquettes de réponse : images, puis symboles). |
| 1.22 | 2026-10-28 | Ajout de DEC-0029 (symbole des sons : `ipa_main` du son contrasté ; pictogrammes de ton dès E1). |
| 1.23 | 2026-10-28 | Ajout de DEC-0030 (lecteur développé d'abord en site statique ; enveloppe WordPress ou Firebase choisie ensuite). |
| 1.24 | 2026-10-28 | Ajout de DEC-0031 (uy et uyê gardés avec *tuy* et *chuyện* ; 9 sons rares reportés en A1–A2). |
| 1.25 | 2026-10-28 | Ajout de DEC-0032 (verrou d'écoute : chaque série réussie au moins 2 fois au débit normal). |
| 1.26 | 2026-10-28 | Ajout de DEC-0033 (position 2 = contraste principal ; séries de L03 et L11 réordonnées). |
| 1.27 | 2026-10-28 | Ajout de DEC-0034 (L01 reste une seule leçon ; test d'entrée). |
| 1.28 | 2026-10-28 | Ajout de DEC-0035 (« mot courant » en Module 0 ; fréquence à partir de A1). |
| 1.29 | 2026-10-28 | Ajout de DEC-0036 (finales : 85 % par leçon, 80 % en sortie). |
| 1.30 | 2026-10-29 | Ajout de DEC-0037 (L01 en deux parties dans le lecteur). |
| 1.31 | 2026-10-29 | Ajout de DEC-0038 (mots repères, catégories de sons, chemins de prononciation). |
| 1.32 | 2026-10-29 | Ajout de DEC-0039 (E1 : découverte de chaque son seul, sans écoute contrastée). |
| 1.33 | 2026-10-29 | Ajout de DEC-0040 (voix et modèles de synthèse retenus). |
| 1.34 | 2026-10-29 | Ajout de DEC-0041 (E2 : échauffement « Pareil ou différent ? » non noté). |
| 1.35 | 2026-10-29 | Ajout de DEC-0042 (place du son : début, fin, voyelle, ton). |
| 1.36 | 2026-10-29 | Ajout de DEC-0043 (leçons de tons : jamais d'audio lent). |
| 1.37 | 2026-10-29 | Ajout de DEC-0044 (L01 : le son i n'est plus un contraste). |
| 1.38 | 2026-10-29 | Ajout de DEC-0045 (tons : une seule voix d'abord, plusieurs ensuite). |
| 1.39 | 2026-10-29 | Ajout de DEC-0046 (repères des finales -m et -n ; u gardé en L01). |
| 1.40 | 2026-10-29 | Liens : ajout de PROD-AF-LECT en sorties (DOC-32). |
| 1.41 | 2026-10-30 | Ajout de DEC-0047 (mode test : afficher ce qui est joué). |
| 1.42 | 2026-10-30 | Ajout de DEC-0048 (voix F3 Thu Minh écartée). |

## Liens

- **Sorties** : [REGLES_DOCUMENTAIRES.md](REGLES_DOCUMENTAIRES.md)
