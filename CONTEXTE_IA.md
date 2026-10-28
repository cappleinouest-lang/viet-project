---
id: CTX-IA
titre: Contexte du projet pour une IA
statut: VALIDE
version: 1.0
date: 2026-10-28
resume: >
  Seul document à donner à une IA en début de session (DOC-28) : le projet
  en une page, son état, la manière de travailler avec Christophe, les
  documents à lire selon la tâche et les points ouverts.
entrees: [DIR-00]
sorties: []
sources: []
---

# Contexte du projet pour une IA

## 1. Le projet en bref

Formation **autonome** au **vietnamien du Nord** (accent courant de Hanoï),
niveaux **A0 → A2**, pour un **adulte francophone** (Christophe d'abord,
d'autres apprenants ensuite). Thèse : la difficulté est d'abord
**perceptive** ; on installe l'oreille, puis la voix, puis le vocabulaire.
Rythme : 20 à 30 min par jour ; progression pilotée par des **verrous**.

## 2. Comment travailler avec Christophe

- Répondre **en français**, clairement, sans jargon inutile.
- Manipulations informatiques : **pas à pas**, une étape à la fois, avec les
  noms exacts des menus ; attendre son retour.
- **Distinguer** faits vérifiés, hypothèses et recommandations ; citer les
  sources.
- Ne **jamais** contredire une décision de `02_REGLES/DECISIONS.md` sans le
  signaler et proposer une nouvelle décision.
- Ne rien modifier dans `_ARCHIVES` (DOC-02).
- Après chaque modification validée : rappeler `git add .` puis
  `git commit -m "…"` dans `C:\VIET_PROJECT`.

## 3. Où trouver quoi

| Besoin | Document |
|---|---|
| Règles de rangement, nommage, en-têtes, liens | `02_REGLES/REGLES_DOCUMENTAIRES.md` (DOC-01 à DOC-35) |
| Pourquoi la formation, pour qui, objectifs | `01_FONDATIONS/01_intention_et_objectifs.md` |
| Tons, sons, écriture, grammaire du vietnamien | `01_FONDATIONS/02_specificites_vietnamien.md` |
| Difficultés des francophones | `01_FONDATIONS/03_difficultes_francophones.md` |
| Parcours E1 → E5, volets, verrous, écrit, images, audio | `01_FONDATIONS/04_principes_pedagogiques.md` |
| Règles vérifiables (R-…) | `02_REGLES/REGISTRE_REGLES.md` |
| Toutes les décisions (DEC-0001 à DEC-0027) | `02_REGLES/DECISIONS.md` |
| Outils : WordPress, lecteur d'activités, Anki | `05_PRODUCTION/01_architecture_outils.md` |
| Fichiers de données et leurs colonnes | `04_DONNEES/00_modele_donnees.md` |
| Vue d'ensemble des documents et de leurs liens | `CARTE_DOCUMENTAIRE.md` (générée) |

## 4. Décisions structurantes (résumé)

| Thème | Décision |
|---|---|
| Structure | 7 dossiers + `_ARCHIVES` ; Markdown et CSV ; Git (DEC-0001 à 0003) |
| Module 0 | **14 leçons** (L03 nặng, L07 hỏi, L11 ngã, L14 recyclage) ; durée indicative 4–6 mois (DEC-0004 à 0006, 0019) |
| Parcours | 5 étapes **E1 Écouter → E2 Distinguer → E3 Opposer → E4 Répéter → E5 Stabiliser** ; volets écoute (E1–E3) / production (E4–E5) ; écoute ≤ 3 leçons d'avance (DEC-0007, 0010) |
| Verrous | 85 %, 90 % pour les tons, sur ≥ 2 voix (DEC-0012) |
| Écrit | jamais en E1–E2, fin d'E3, visible en E4–E5 ; **images** pour donner le sens sans écrit (DEC-0011, 0024) |
| Accent | courant de Hanoï : tr/ch, s/x, d/gi/r = orthographe, pas écoute ; **un code par son** (76 sons) (DEC-0009, 0018) |
| Mots | 98 mots supports en M0 (79 imageables) ; séries minimales de **2 à 4 termes**, paire en E2, série complète en E3 ; contraste de ton ou de son (DEC-0020, 0024 à 0026) |
| Outils | **WordPress sans LMS** + lecteur d'activités sur mesure + page de prononciation (courbe mélodique) ; **Anki** pour les révisions (DEC-0015, 0016) |
| Données | **CSV** comme source de vérité, contrôle par SQLite temporaire (DEC-0017) |
| Audio | regénéré, FPT.AI (banmai, thuminh, leminh), variété des voix et débits (DEC-0023) |

## 5. État au 2026-10-28

| Partie | État |
|---|---|
| Fondations FOND-01 à 04 | **VALIDE** |
| Règles documentaires, registre (61 règles), architecture des outils | brouillons |
| Données (`04_DONNEES`, 12 fichiers CSV) | reprises ; séries minimales et mots hors corpus à confirmer |
| Programme du Module 0 (`03_PROGRAMME/progression_M0.md`) | **à écrire** |
| Audios, images | **à générer / choisir** |
| Lecteur d'activités, page de prononciation, extension de progression | **à développer** |
| Règles de code (SQL, Python, PowerShell) | hors périmètre pour l'instant |

## 6. Points ouverts

- Mesure du verrou de production : seuils de la courbe mélodique à calibrer
  (test « ma » juste / faux concluant ; paires 2 à 5 à enregistrer).
- Reconnaissance vocale en complément (FPT.AI ou PhoWhisper) : plus tard ;
  Azure jugé peu performant en vietnamien.
- Voix d'enfant et deuxième voix masculine du Nord : source à trouver.
- Liste de fréquence de référence (R-LEX-07) ; traductions à relire
  (*chưng*, *à*, *chi*, *lẽ*) ; étymologies manquantes.
- Termes hors corpus vérifiés (DEC-0027) : 74 mots réels dont le sens reste à vérifier ; 9 séries utilisent une syllabe inventée dès E2.
- Valeurs `imageable` à corriger ; choix des images (OpenMoji privilégié).
- Le raccourci « VIET_PROJECT » épinglé dans l'Explorateur pointe vers
  `D:\VIET_PROJECT`, qui n'existe plus.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-28 | Création, en fin de session de refonte. |
