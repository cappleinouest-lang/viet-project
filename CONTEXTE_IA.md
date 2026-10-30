---
id: CTX-IA
titre: Contexte du projet pour une IA
statut: VALIDE
version: 1.12
date: 2026-10-30
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
- Ne rien supprimer : une voix ou un fichier écarté passe au statut
  `inactive` ou reste en place, ignoré.
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
| Toutes les décisions (DEC-0001 à DEC-0056) | `02_REGLES/DECISIONS.md` |
| Types d'activités par étape | `03_PROGRAMME/01_types_activites.md` |
| Les 14 leçons du Module 0 | `03_PROGRAMME/progression_M0.md` |
| Fichiers de données et leurs colonnes | `04_DONNEES/00_modele_donnees.md` |
| Outils : lecteur d'activités, enveloppe (WordPress ou Firebase), Anki | `05_PRODUCTION/01_architecture_outils.md` |
| Lecteur d'activités : fichiers, génération, règles appliquées | `05_PRODUCTION/02_lecteur_activites.md` |
| Lecteur : besoin, fonctions, écrans, règles de gestion, écarts | `05_PRODUCTION/04_analyse_fonctionnelle_lecteur.md` |
| Audios : voix, génération FPT, commandes, validation | `05_PRODUCTION/03_audio.md` |
| Vue d'ensemble des documents et de leurs liens | `CARTE_DOCUMENTAIRE.md` (générée) |

## 4. Décisions structurantes (résumé)

| Thème | Décision |
|---|---|
| Structure | 7 dossiers + `_ARCHIVES` ; Markdown et CSV ; Git (DEC-0001 à 0003) |
| Module 0 | **14 leçons** (L03 nặng, L07 hỏi, L11 ngã, L14 recyclage) ; durée indicative 4–6 mois (DEC-0004 à 0006, 0019) ; L01 en deux parties dans le lecteur (DEC-0037), 14 séries, i retiré des contrastes, u gardé (DEC-0044, 0046) |
| Parcours | 5 étapes **E1 Écouter → E2 Distinguer → E3 Opposer → E4 Répéter → E5 Stabiliser** ; volets écoute (E1–E3) / production (E4–E5) ; écoute ≤ 3 leçons d'avance (DEC-0007, 0010) |
| E1 | **découverte de chaque son seul**, sans opposition : 3 mots au plus par son, voix de femme puis d'homme, boutons « Écouter » / « Écouter lentement », choix de la voix (DEC-0039) |
| E2–E3 | échauffement « Pareil ou différent ? » non noté au début d'E2 (DEC-0041) ; place du son indiquée (début ▸, ◂ fin, voyelle, ton) et consigne « quoi écouter » (DEC-0042) |
| Leçons de tons | **jamais d'audio lent** (DEC-0043) ; une seule voix (F1) à l'échauffement et en phase « avec images », plusieurs voix en phase « symboles seuls » (DEC-0045) |
| Verrous | 85 %, 90 % pour les tons, sur ≥ 2 voix ; chaque série réussie au moins 2 fois au débit normal (DEC-0012, 0032) ; finales : 85 % par leçon, 80 % en sortie (DEC-0036) |
| Écrit | jamais en E1–E2, fin d'E3, visible en E4–E5 ; **images** pour donner le sens sans écrit (DEC-0011, 0024) |
| Étiquettes E2–E3 | débit lent : image + symbole ; débit normal : symbole seul. Ton → pictogramme + couleur ; son → `ipa_main` du son contrasté ; symboles présentés dès E1 (DEC-0028, 0029) ; mots repères et catégories de sons (DEC-0038), repères propres aux finales -m « pomme », -n « laine » (DEC-0046) |
| Accent | courant de Hanoï : tr/ch, s/x, d/gi/r = orthographe, pas écoute ; **un code par son** (76 sons) (DEC-0009, 0018) |
| Mots | **100 mots supports** en M0 ; 9 sons rares reportés en A1–A2 (DEC-0031) ; séries minimales de **2 à 4 termes**, paire en E2, série complète en E3 ; contraste de ton ou de son (DEC-0020, 0024 à 0026, 0031) |
| Outils | **Lecteur d'activités** + page de prononciation (courbe mélodique), développés d'abord en **site statique** ; enveloppe définitive **WordPress ou Firebase** choisie quand le lecteur fonctionne ; **Anki** pour les révisions (DEC-0015, 0016, 0030) ; mode test qui affiche ce qui est joué (DEC-0047) |
| Données | **CSV** comme source de vérité, contrôle par SQLite temporaire (DEC-0017) |
| Audio | FPT AI Marketplace, mot envoyé seul, volume égalisé à −20 dBFS (DEC-0040). Écoute des **leçons de sons** : **F3 Thu Minh** et **H4 Huy Phong** ; **leçons de tons** : F1, H3, H4 provisoirement, choix à faire (DEC-0055, mesure dans `07_QUALITE/contraste_tons_voix_2026-10-30.md`). **Modèle d'E4 : F1 Ban Mai**. Débit lent : F1 0,7 ; H3, H4 0,6 |

## 5. État au 2026-10-30

| Partie | État |
|---|---|
| Fondations FOND-01 à 04 | **VALIDE** |
| Règles documentaires, registre des règles, architecture des outils | brouillons |
| Données (`04_DONNEES`, 15 fichiers CSV) | reprises ; mots hors corpus à confirmer |
| Programme du Module 0 (`progression_M0.md`) | brouillon ; points P1 à P6 décidés (DEC-0031 à 0036) |
| Audios | **2 237 générés** chez FPT (mots, syllabes, syllabes inventées ; 2 débits) ; **aucun validé** (`validated = false`). Depuis DEC-0048, 56 mots d'exemple d'E1 attendent leur audio F1 (112 fichiers) ; outil de validation par l'écoute **à faire** |
| Images | emoji provisoires ; OpenMoji **à choisir** |
| Lecteur d'activités | **version d'essai 0.13** : volet écoute E1–E3 de toutes les leçons, réglages, « Mes progrès », mode test ; audios FPT lus en mode d'essai (`generer_lecteur.py . --non-valides`) ; version autonome en un fichier dans `06_LIVRABLES/lecteur/`. Volet production **commencé** (DEC-0049 : E4 d'abord, sur PC ; page d'essai `essai_micro.html` + `prononciation.js` ; DEC-0050 : modèle lent FPT puis normal, courbe partout, courbes du modèle calculées par `tools/courbes_modele.py` ; **E4 intégré au lecteur**, sans verrou ; page « Les 6 tons » avec schémas, DEC-0052, DEC-0053) ; L14, paquets Anki **à développer** |
| Règles de code (SQL, Python, PowerShell) | hors périmètre pour l'instant |

## 6. Points ouverts

- **Validation des audios** : écouter et passer `validated = true` ;
  outil d'écoute à faire (R-AUD-01).
- **Deuxième voix de femme du Nord** à trouver depuis l'écartement de F3
  (DEC-0048) ; voix d'enfant : source à trouver.
- Mesure du verrou de production : seuils de la courbe mélodique à calibrer
  (test « ma » juste / faux concluant ; paires 2 à 5 à enregistrer).
- Reconnaissance vocale en complément (FPT.AI ou PhoWhisper) : plus tard ;
  Azure jugé peu performant en vietnamien.
- Mode test (DEC-0047) et mode essai « tout ouvert » (DEC-0051) : à
  désactiver par défaut avant d'ouvrir la formation à d'autres apprenants.
- Liste de fréquence de référence (R-LEX-07), pour A1 (en M0 : « mot courant », DEC-0035) ; traductions à relire
  (*chưng*, *à*, *chi*, *lẽ*) ; étymologies manquantes.
- Termes hors corpus vérifiés (DEC-0027) : 74 mots réels dont le sens reste à vérifier ; 9 séries utilisent une syllabe inventée dès E2.
- Valeurs `imageable` à corriger ; choix des images (OpenMoji privilégié).
- Le seul emplacement du projet est **`C:\VIET_PROJECT`** : ne jamais
  utiliser `D:\VIET_PROJECT` (n'existe plus). Le raccourci épinglé dans
  l'Explorateur doit être refait vers `C:\VIET_PROJECT`.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-28 | Création, en fin de session de refonte. |
| 1.1 | 2026-10-28 | Étiquettes de réponse E2–E3 (DEC-0028, DEC-0029). |
| 1.2 | 2026-10-28 | Outils : lecteur d'abord en site statique (DEC-0030). |
| 1.3 | 2026-10-28 | Programme du M0 écrit ; 100 mots, sons rares reportés (DEC-0031). |
| 1.4 | 2026-10-28 | Verrou d'écoute : minimum par série (DEC-0032). |
| 1.5 | 2026-10-28 | Ordre des termes des séries (DEC-0033). |
| 1.6 | 2026-10-28 | L01 reste une seule leçon (DEC-0034). |
| 1.7 | 2026-10-28 | Critère « mot courant » en Module 0 (DEC-0035). |
| 1.8 | 2026-10-28 | Seuils des finales (DEC-0036). |
| 1.9 | 2026-10-28 | Lecteur d'activités, version d'essai 0.1 (volet écoute). |
| 1.10 | 2026-10-29 | L01 en deux parties (DEC-0037). |
| 1.11 | 2026-10-29 | Mots repères et catégories de sons (DEC-0038). |
| 1.12 | 2026-10-30 | Mise à jour d'ensemble : décisions DEC-0039 à DEC-0048 (E1 découverte, échauffement E2, place du son, leçons de tons, L01, repères des finales, mode test, voix F3 écartée) ; état au 2026-10-30 (audios générés non validés, lecteur 0.13) ; documents PROD-AUDIO et PROD-AF-LECT ajoutés au § 3 ; points ouverts revus ; emplacement unique C:\VIET_PROJECT. |
