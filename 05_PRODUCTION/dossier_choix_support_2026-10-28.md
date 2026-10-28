---
id: PROD-DOSSIER-SUPPORT-20261028
titre: Dossier pour le choix du support de formation
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Rassemble, en un seul endroit, tout ce que le projet contient d'utile pour
  choisir le support de formation : documents à lire, exigences extraites
  (avec leur source), constats déjà établis, options étudiées, points
  ouverts, et ce que les archives apportent ou non.
entrees: []
sorties: []
sources:
  - Exploration de C:\VIET_PROJECT le 2026-10-28 (dossiers 01 à 07 et _ARCHIVES)
  - FOND-01, FOND-04, REG-REGLES, REG-DEC, PROG-ACT, PROD-ARCH, DATA-MODELE (documents analysés)
---

# Dossier pour le choix du support de formation

## Résumé

> **À savoir d'abord (fait)** : le choix est **déjà tranché** dans le journal
> des décisions : **DEC-0015** (WordPress pour l'apprentissage, Anki pour les
> révisions) et **DEC-0016** (WordPress **sans** extension LMS au départ, avec
> un lecteur d'activités et une petite extension de progression sur mesure).
> Ce dossier sert donc à **revalider** ce choix ou à le **remettre en cause**.
> Dans ce second cas, il faut une nouvelle décision (DEC-0030) qui
> « remplace DEC-0015 / DEC-0016 » (DOC-22).

Sur les 2 000 fichiers environ du dossier, **7 documents actuels** suffisent
pour décider. Les archives n'apportent que du contexte : elles supposaient
toutes **Anki seul** (« 1 exercice = 1 carte Anki »).

## 1. Documents à lire, par ordre d'importance

### 1.1 Indispensables (projet actuel)

| Priorité | Document | Fichier | Ce qu'il apporte au choix |
|---|---|---|---|
| 1 | **REG-DEC** Journal des décisions | `02_REGLES/DECISIONS.md` | DEC-0015 et DEC-0016 (options A à E, constats, décision) ; DEC-0007, 0012 (volets, verrous) ; DEC-0017 (CSV) ; DEC-0023 (audio) ; DEC-0028–0029 (étiquettes de réponse) |
| 2 | **PROG-ACT** Types d'activités E1–E5 | `03_PROGRAMME/01_types_activites.md` | Le **cahier des charges fonctionnel** : ce que l'élève entend, voit, comment il répond, score, fin d'étape |
| 3 | **PROD-ARCH** Architecture des outils | `05_PRODUCTION/01_architecture_outils.md` | La solution retenue décrite composant par composant ; parcours de l'élève ; lien WordPress–Anki ; hébergement ; points ouverts |
| 4 | **REG-REGLES** Registre des règles | `02_REGLES/REGISTRE_REGLES.md` | Règles vérifiables que l'outil doit appliquer : R-VOL, R-AUD, R-ECR, R-REV, **R-SUP** (neutralité du support) |
| 5 | **FOND-04** Principes pédagogiques | `01_FONDATIONS/04_principes_pedagogiques.md` | § 5 verrous et question ouverte « mesurer la production sans enseignant » ; § 8 audio ; § 10 révisions |
| 6 | **FOND-01** Intention et objectifs | `01_FONDATIONS/01_intention_et_objectifs.md` | Public, autonomie, 20–30 min/jour, principes non négociables, objectifs chiffrés |
| 7 | **CTX-IA** Contexte pour une IA | `CONTEXTE_IA.md` | Synthèse d'une page : décisions, état, points ouverts |

### 1.2 Utiles en complément

| Document | Fichier | Pourquoi |
|---|---|---|
| **DATA-MODELE** Modèle des données | `04_DONNEES/00_modele_donnees.md` | Ce que le générateur devra lire ; l'outil doit s'alimenter depuis ces CSV |
| Test de reconnaissance vocale | `05_PRODUCTION/tools/test_asr/` (`enregistrer.py`, `transcrire.py`, `liste_test.csv`) | Test PhoWhisper en cours : conditionne la mesure du verrou de production |
| **REG-DOC** Règles documentaires | `02_REGLES/REGLES_DOCUMENTAIRES.md` | DOC-03 (livrables regénérables), DOC-04 (pas de clés d'accès dans le projet) |

### 1.3 Archives : contexte seulement

| Document | Fichier (sous `_ARCHIVES/`) | Intérêt |
|---|---|---|
| Stratégie pédagogique globale v01 | `OLD/DOCS/00_CADRAGE/CADR_STRAT_pedagogie_globale_v01.md` | § 6.1 « toutes les unités doivent être exportables vers Anki » : **ancienne contrainte**, remplacée par R-SUP-02 |
| Structure du Module 0 hybride v02 | `OLD/DOCS/00_CADRAGE/CADR_SPEC_STRUCTURE_MODULE_0_HYBRIDE_v02.md` | Modèle « 1 exercice = 1 carte Anki » ; 5 phases reprises dans PROG-ACT |
| Guide d'implémentation M0 hybride | `OLD/PROD/00_GLOBAL/01_DB/05_DOCS/GUIDES/GUIDE_IMPLEMENT_MODULE_0_HYBRIDE_v01.md` | Estimation de **1 500 à 3 500 cartes** Anki pour le M0 : montre la lourdeur d'Anki seul |
| Contrat d'unité pédagogique v1.9 | `Projet de Formation_Vietnamien_A0_to_A2/DOCS/02_RULES/P2_PEDA_M0_RULE_Contrat_Unite_Pedagogique_v1_9.md` | Unité = carte Anki ; variantes de voix générées à l'export |
| Cible / support / variantes de voix v1.1 | `Projet de Formation_Vietnamien_A0_to_A2/DOCS/02_RULES/P2_PEDA_M0_RULE_Cible_Support_Variantes_Voix_v1_1.md` | « Multi-cartes » par voix (ici, « support » = mot support, pas outil) |
| Images dans les cartes Anki v1.0 | `OLD/DOCS/03_ARCHITECTURE/P4_ARCHI_IMAGE_Anki_v1_0.docx` | Ancien câblage des images dans Anki (déconseillées en perception) |

### 1.4 Écartés (sans rapport avec le choix)

Scripts SQL, Python et PowerShell des archives, journaux (`QUAL/LOGS`),
exports PostgreSQL, guides PostgreSQL / UTF-8 / PowerShell, environnements
Python (`.venv`), dictionnaires, fichiers audio, `.git`.

## 2. Exigences extraites (cahier des charges du support)

Chaque ligne est tirée d'un document du projet. **O** = obligatoire,
**S** = souhaité.

### 2.1 Public, appareils, coût

| N° | Exigence | Niv. | Source |
|---|---|---|---|
| EX-01 | Utilisable par Christophe d'abord, **partageable** ensuite avec d'autres apprenants | O | DEC-0015 |
| EX-02 | Fonctionne sur **PC Windows, Android, iPhone et navigateur** | O | DEC-0015 |
| EX-03 | **Même progression** sur tous les appareils (compte de l'élève) | O | DEC-0016 |
| EX-04 | Budget **modeste** ; développement gratuit en local | O | DEC-0015 ; PROD-ARCH § 5 |
| EX-05 | Apprentissage **autonome**, sans enseignant | O | FOND-01 § 3 |
| EX-06 | Séances de **20 à 30 min/jour** | O | FOND-01 § 3 ; PROG-ACT § 4 |

### 2.2 Parcours et verrous

| N° | Exigence | Niv. | Source |
|---|---|---|---|
| EX-07 | 5 étapes **E1 → E5** par leçon, en deux **volets** (écoute E1–E3, production E4–E5) | O | DEC-0010 ; R-VOL-01 |
| EX-08 | Volets **indépendants** ; l'écoute peut avoir **3 leçons d'avance** au plus (paramètre) | O | DEC-0007 ; R-VOL-02 à 04 |
| EX-09 | **Verrou d'écoute** calculé : ≥ 85 % (≥ 90 % pour les tons), au **débit normal**, sur **≥ 2 voix** | O | DEC-0012 ; R-VOL-05 à 07 |
| EX-10 | Score sur les **20 dernières réponses** (paramètre) | O | PROG-ACT § 2 |
| EX-11 | Passage au débit normal **automatique** quand le seuil est atteint au débit lent | O | PROG-ACT § 2 |
| EX-12 | Passage à la suite sur **verrou**, jamais au calendrier | O | R-VOL-10 |

### 2.3 Activités

| N° | Exigence | Niv. | Source |
|---|---|---|---|
| EX-13 | Question **audio seule** avec choix **A/B** (E2) puis 2 à 4 choix (E3) | O | PROG-ACT ; R-PARC-04 |
| EX-14 | **Aucun écrit** en E1–E2 ; écrit révélé en fin d'E3 ; visible en E4–E5 | O | DEC-0011 ; R-ECR |
| EX-15 | Étiquettes de réponse : **image + symbole** (lent), **symbole seul** (normal) ; pictogramme et couleur de ton ; `ipa_main` pour les sons | O | DEC-0028 ; DEC-0029 |
| EX-16 | **Correction immédiate** ; rejouer le(s) terme(s) après la réponse | O | PROG-ACT § 2 |
| EX-17 | **Tirage aléatoire** ; pas plus de 3 fois de suite la même bonne réponse ; voix alternées | O | PROG-ACT § 4 |
| EX-18 | Réécoute toujours permise ; **pas de chronomètre** en écoute | O | PROG-ACT § 4 |
| EX-19 | Syllabes inventées présentées comme **bouton sonore** | O | DEC-0027 ; R-LEX-06 |

### 2.4 Audio et production orale

| N° | Exigence | Niv. | Source |
|---|---|---|---|
| EX-20 | **Plusieurs voix** (≥ 2) et **débits** (lent, normal, rapide) en écoute ; **une voix modèle** en production | O | R-AUD-02 à 04 ; DEC-0023 |
| EX-21 | **Enregistrer la voix** de l'élève et la réécouter à côté du modèle | O | ACT-E4-REPETE |
| EX-22 | **Courbe mélodique** de l'élève superposée au modèle, dans le navigateur, sans service extérieur | O | PROD-ARCH § 2 |
| EX-23 | Accès au micro → site en **https** | O | PROD-ARCH § 5 |
| EX-24 | Reconnaissance vocale en **complément** (plus tard) | S | CTX-IA § 6 |

### 2.5 Révisions et données

| N° | Exigence | Niv. | Source |
|---|---|---|---|
| EX-25 | **Répétition espacée** ; une erreur rapproche la révision suivante | O | FOND-01 § 5 ; R-REV-04 |
| EX-26 | Tous les contenus **générés** depuis `04_DONNEES` (CSV), jamais saisis à la main | O | DEC-0017 ; R-AUD-06 ; DOC-03 |
| EX-27 | Changer d'outil ne doit **pas** modifier fondations ni registre : seule une couche d'adaptation dans `05_PRODUCTION` | O | R-SUP-02 |
| EX-28 | Suivi de la **non-régression** après le Module 0 | S | R-VOL-09 ; PROD-ARCH § 4 |

## 3. Constats déjà établis

| Constat | Nature | Source |
|---|---|---|
| Azure Speech peu performant en vietnamien | expérience de Christophe | DEC-0015 |
| Le code des cartes Anki n'a **pas accès au micro** (refus du développeur, juin 2025) | fait noté au projet | DEC-0015 |
| Aucun LMS (Moodle, WordPress) n'offre de **vraie révision espacée** | fait noté au projet | DEC-0015 |
| Les quiz des LMS ne documentent pas les questions **audio A/B sans écrit** | fait noté au projet | DEC-0016 |
| La **courbe mélodique** distingue un « ma » juste d'un faux et tourne dans un navigateur | test du 2026-10-28 | DEC-0015 ; PROD-ARCH |
| FPT.AI : reconnaissance vocale **absente** de la console et de la Marketplace | constaté le 2026-10-28 | PROD-ARCH § 6 |
| Méta-analyse HVPT : identification (« Lequel ? ») > « même / différent » ; plafond vers 400 min ; voix variées utiles | recherche citée | PROG-ACT § 5 |

## 4. Options déjà étudiées (DEC-0015, DEC-0016)

| Option | Écartée parce que… |
|---|---|
| A — Anki seul | pas de micro, pas de verrous, pas de volets |
| B — Application web sur mesure | *raison non écrite dans DEC-0015* |
| C — Anki + page de prononciation | *raison non écrite* |
| D — LMS Moodle | pas de révision espacée ; quiz inadaptés |
| E — LMS sur WordPress | quiz audio A/B non documentés ; lecteur sur mesure nécessaire de toute façon (DEC-0016) |
| **Retenu** — WordPress (pages, comptes) + lecteur d'activités + extension de progression + page de prononciation, **Anki** pour les révisions | — |

## 5. Points ouverts qui pèsent sur le choix

| Point | Source |
|---|---|
| Mesure du **verrou de production** (R-VOL-08) : seuils de la courbe mélodique à calibrer ; proposition provisoire « proche » sur 80 % des items d'E5 | PROG-ACT § 3 ; PROD-ARCH § 6 |
| Reconnaissance vocale : **PhoWhisper** en test, FPT.AI indisponible | PROD-ARCH § 6 |
| Les révisions Anki **ne remontent pas** au site : non-régression contrôlée par les statistiques Anki (*hypothèse à confirmer*) | PROD-ARCH § 4 |
| Choix de l'**hébergeur** en ligne | PROD-ARCH § 6 |
| Ajout d'un **LMS** au moment du partage | DEC-0016 |

## 6. Remarques (recommandations, à valider)

1. **Combler un trou de traçabilité** : DEC-0015 ne dit pas pourquoi
   l'option **B** (application web sur mesure, sans WordPress) a été écartée.
   Or l'architecture retenue développe déjà sur mesure l'essentiel (lecteur,
   page de prononciation, extension) ; WordPress n'apporte « que » les pages,
   les comptes et la connexion. Il vaut la peine d'écrire cette comparaison
   B / WordPress noir sur blanc (coût d'hébergement, sécurité et mises à jour
   de WordPress, gestion des comptes).
2. **Coût d'Anki sur iPhone** (*fait à vérifier sur l'App Store*) : Anki est
   gratuit sur PC, Android (AnkiDroid) et navigateur (AnkiWeb), mais
   **AnkiMobile** sur iPhone est payant (environ 25 $, achat unique). À
   intégrer à EX-04 si la formation est partagée avec des utilisateurs
   d'iPhone.
3. **Vérifier EX-22 sur iPhone** : l'enregistrement du micro dans Safari
   fonctionne en https, mais le format audio diffère d'Android/PC. Un essai
   de la page de courbe mélodique sur iPhone avant de figer le choix
   éviterait une mauvaise surprise.

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création à partir de l'exploration de C:\VIET_PROJECT. |

## Liens

- **Entrées** :
  [Journal des décisions](../02_REGLES/DECISIONS.md) ·
  [Types d'activités](../03_PROGRAMME/01_types_activites.md) ·
  [Architecture des outils](01_architecture_outils.md) ·
  [Registre des règles](../02_REGLES/REGISTRE_REGLES.md) ·
  [Principes pédagogiques](../01_FONDATIONS/04_principes_pedagogiques.md) ·
  [Intention et objectifs](../01_FONDATIONS/01_intention_et_objectifs.md)
- **Sorties** : aucune pour l'instant (DEC-0030 si le choix change)
