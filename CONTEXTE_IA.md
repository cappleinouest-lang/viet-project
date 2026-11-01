---
id: CTX-IA
titre: Contexte du projet pour une IA
statut: VALIDE
version: 1.15
date: 2026-11-01
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
- Après chaque modification validée : la noter dans
  `07_QUALITE/suivi_modifications.md` (numéro `MOD-…`), puis rappeler
  `git add .` et `git commit -m "MOD-… : …"` dans `C:\VIET_PROJECT`.

## 3. Où trouver quoi

| Besoin | Document |
|---|---|
| Règles de rangement, nommage, en-têtes, liens | `02_REGLES/REGLES_DOCUMENTAIRES.md` (DOC-01 à DOC-35) |
| Pourquoi la formation, pour qui, objectifs | `01_FONDATIONS/01_intention_et_objectifs.md` |
| Tons, sons, écriture, grammaire du vietnamien | `01_FONDATIONS/02_specificites_vietnamien.md` |
| Difficultés des francophones | `01_FONDATIONS/03_difficultes_francophones.md` |
| Parcours E1 → E5, volets, verrous, écrit, images, audio | `01_FONDATIONS/04_principes_pedagogiques.md` |
| Règles vérifiables (R-…) | `02_REGLES/REGISTRE_REGLES.md` |
| Toutes les décisions (DEC-0001 à DEC-0071) | `02_REGLES/DECISIONS.md` |
| Types d'activités par étape | `03_PROGRAMME/01_types_activites.md` |
| Les 14 leçons du Module 0 | `03_PROGRAMME/progression_M0.md` |
| Fichiers de données et leurs colonnes | `04_DONNEES/00_modele_donnees.md` |
| Outils : lecteur d'activités, enveloppe (WordPress ou Firebase), Anki | `05_PRODUCTION/01_architecture_outils.md` |
| Lecteur d'activités : fichiers, génération, règles appliquées | `05_PRODUCTION/02_lecteur_activites.md` |
| Lecteur : besoin, fonctions, écrans, règles de gestion, écarts | `05_PRODUCTION/04_analyse_fonctionnelle_lecteur.md` |
| Audios : voix, génération FPT, commandes, validation | `05_PRODUCTION/03_audio.md` |
| Modifications faites et besoins de modification à venir (MOD-A01…) | `07_QUALITE/suivi_modifications.md` |
| Dernier point complet d'avancement | `07_QUALITE/etat_avancement_2026-10-31.md` (antérieur à DEC-0067) |
| Essai des voix FPT.TTS-ultra | `07_QUALITE/essai_tts_ultra_2026-10-31.md` |
| Vue d'ensemble des documents et de leurs liens | `CARTE_DOCUMENTAIRE.md` (générée ; datée du 29/10, à regénérer) |

## 4. Décisions structurantes (résumé)

| Thème | Décision |
|---|---|
| Structure | 7 dossiers + `_ARCHIVES` ; Markdown et CSV ; Git (DEC-0001 à 0003) ; audios intermédiaires `_bruts`, `_anciens`, `_essais` **suivis par Git** (DEC-0071) |
| Module 0 | **14 leçons** (L03 nặng, L07 hỏi, L11 ngã, L14 recyclage) ; durée indicative 4–6 mois (DEC-0004 à 0006, 0019) ; L01 en deux parties dans le lecteur (DEC-0037), 14 séries, i retiré des contrastes, u gardé (DEC-0044, 0046) |
| Parcours | 5 étapes **E1 Écouter → E2 Distinguer → E3 Opposer → E4 Répéter → E5 Stabiliser** ; volets écoute (E1–E3) / production (E4–E5) ; écoute ≤ 3 leçons d'avance (DEC-0007, 0010) |
| E1 | **découverte de chaque son seul**, sans opposition : 3 mots au plus par son, voix de femme puis d'homme, boutons « Écouter » / « Écouter lentement », choix de la voix (DEC-0039) ; pour une **voyelle simple**, la voyelle seule avant les mots, au débit normal seulement (DEC-0070) |
| E2–E3 | échauffement « Pareil ou différent ? » non noté au début d'E2 (DEC-0041) ; place du son indiquée (début ▸, ◂ fin, voyelle, ton) et consigne « quoi écouter » (DEC-0042) |
| Leçons de tons | **jamais d'audio lent** (DEC-0043) ; une seule voix à l'échauffement et en phase « avec images », plusieurs voix en phase « symboles seuls » (DEC-0045) ; voix : F4 et H6 (DEC-0067) |
| Verrous | 85 %, 90 % pour les tons, sur ≥ 2 voix ; chaque série réussie au moins 2 fois au débit normal (DEC-0012, 0032) ; finales : 85 % par leçon, 80 % en sortie (DEC-0036) |
| Écrit | aucun **mot** écrit en E1–E2 (mais lettres du son étudié en E1 et phase 1, DEC-0063), mots à la fin d'E3, visibles en E4–E5 ; **images** pour donner le sens sans écrit (DEC-0011, 0024) |
| Étiquettes E2–E3 | débit lent : image + symbole ; débit normal : symbole seul. Ton → pictogramme + couleur ; son → `ipa_main` du son contrasté ; symboles présentés dès E1 (DEC-0028, 0029) ; mots repères et catégories de sons (DEC-0038), repères propres aux finales -m « pomme », -n « laine » (DEC-0046) |
| Accent | courant de Hanoï : tr/ch, s/x, d/gi/r = orthographe, pas écoute ; **un code par son** (76 sons) (DEC-0009, 0018) |
| Mots | **100 mots supports** en M0 ; 9 sons rares reportés en A1–A2 (DEC-0031) ; séries minimales de **2 à 4 termes**, paire en E2, série complète en E3 ; contraste de ton ou de son (DEC-0020, 0024 à 0026, 0031) |
| Outils | **Lecteur d'activités** + page de prononciation (courbe mélodique), développés d'abord en **site statique** ; enveloppe définitive **WordPress ou Firebase** choisie quand le lecteur fonctionne ; **Anki** pour les révisions (DEC-0015, 0016, 0030) ; mode test qui affiche ce qui est joué (DEC-0047), avec bouton « ⚑ Signaler un son » (DEC-0069) |
| Données | **CSV** comme source de vérité, contrôle par SQLite temporaire (DEC-0017) |
| Audio | FPT AI Marketplace, mot envoyé seul, volume égalisé à −20 dBFS (DEC-0040). **Deux voix seulement**, en **FPT.TTS-ultra**, pour toutes les écoutes (leçons de sons et de tons), E1, la page « Les 6 tons » et le **modèle d'E4** : **F4 Ban Mai** (femme) et **H6 Quang Anh** (homme) (DEC-0067, remplace DEC-0055 et DEC-0066). Ultra ignore la vitesse : **débit lent emprunté** (colonne `slow_from` de `voix.csv`) à F1 Ban Mai (FPT.TTS-pro, 0,7) et à H4 Huy Phong (FPT.AI-VITs, 0,6) ; la voix d'homme change donc entre lent et normal. F1, F3, H3, H4 : `inactive` (F1 et H4 restent la source du lent). Fichiers Ultra : début gardé brut, silence final complété à 0,35 s (DEC-0068). Mots espacés des phrases : **virgules** (« Tôi, ăn, nem. »). Locuteur le plus adapté aux leçons de tons : encore à choisir (contraste des tons plus faible en Ultra) |

## 5. État au 2026-11-01

| Partie | État |
|---|---|
| Fondations FOND-01 à 04 | **VALIDE** |
| Règles documentaires, registre des règles, architecture des outils | brouillons |
| Décisions | **71** (DEC-0001 à DEC-0071) |
| Données (`04_DONNEES`, 18 fichiers CSV) | reprises ; mots hors corpus à confirmer ; `voix.csv` : F4 et H6 seules actives |
| Programme du Module 0 (`progression_M0.md`) | brouillon ; points P1 à P6 décidés (DEC-0031 à 0036) |
| Audios | `audios.csv` : **5 506 audios**, dont **3 494 validés** (`validated = true`), tous des anciennes voix (F1, F3, H3, H4). **F4 / H6 : générés pour L01 seulement** (227 fichiers, dont 10 voyelles seules), **aucun validé** ; autres leçons à générer après écoute de L01 (environ 1 700 fichiers ; tarif d'Ultra à vérifier). 170 audios marqués « à refaire » (`07_QUALITE/audios_a_refaire.csv`), dont 32 seulement restent utiles |
| Images | emoji provisoires ; OpenMoji **à choisir** |
| Lecteur d'activités | **version d'essai 0.21** (numéro de QUAL-AVANCEMENT ; PROD-LECT dit encore 0.20) : volet écoute E1, échauffement, E2, E3, « Combien de fois ? », écrit, pour toutes les leçons sauf L14 ; voyelle seule en E1 (DEC-0070) ; signalement d'un son (DEC-0069) ; réglages, « Mes progrès », mode test, mode essai « tout ouvert » ; page « Les 6 tons ». Volet production : **E4 intégré**, sans verrou (micro, courbes mélodiques du modèle) ; E5, L14, paquets Anki **à développer**. Version autonome en un fichier dans `06_LIVRABLES/lecteur/` |
| Git | tout le travail jusqu'au 31/10 enregistré (commit `1d5c57e`, 01/11) ; historique **seulement sur le PC** : dépôt privé GitHub prévu (MOD-A02) |
| Règles de code (SQL, Python, PowerShell) | hors périmètre pour l'instant |

## 6. Points ouverts

La liste complète, numérotée et classée par priorité, est dans
`07_QUALITE/suivi_modifications.md` (section 3). Les plus importants :

- **Sauvegarde hors du PC** (MOD-A02) : dépôt privé GitHub.
- **Documents à mettre d'accord avec DEC-0067** (MOD-B02 à MOD-B07) :
  PROD-AUDIO, PROD-LECT, PROD-AF-LECT, PROG-M0, PROG-ACT, DATA-MODELE et
  R-AUD-02 parlent encore des voix F1, F3, H3, H4.
- **E1, mots d'exemple** (MOD-H01, à décider) : étudier d'abord 1 ou 2
  consonnes initiales pour que les mots d'exemple des voyelles soient de
  simples syllabes consonne + voyelle. À trancher **avant** de générer les
  audios Ultra des autres leçons (MOD-C01).
- **Audios Ultra** : écouter L01 dans le lecteur, vérifier le tarif, puis
  générer les autres leçons (MOD-C01, MOD-C02) ; ne refaire que les 32
  audios « à refaire » encore utiles (MOD-C04).
- **Validation des audios** (R-AUD-01) : outil prêt (DEC-0065,
  `tools/valider_audios.py`, mode d'emploi dans `05_PRODUCTION/03_audio.md`
  § 5) ; les audios F4 / H6 sont à écouter et le nombre total à recompter
  (MOD-C03).
- **Voix des leçons de tons** : contraste des tons plus faible en Ultra
  (environ 2,3 contre 4 pour F1 et H4) ; enregistrement natif à envisager
  pour la page des tons et le modèle d'E4 (MOD-C05, MOD-C10).
- **Deuxième voix de femme du Nord** à trouver (DEC-0066) ; voix d'enfant :
  source à trouver.
- Mesure du verrou de production : seuils de la courbe mélodique à calibrer
  (test « ma » juste / faux concluant ; paires 2 à 5 à enregistrer).
- Reconnaissance vocale en complément (FPT.AI ou PhoWhisper) : plus tard ;
  Azure jugé peu performant en vietnamien.
- Mode test (DEC-0047) et mode essai « tout ouvert » (DEC-0051) : à
  désactiver par défaut avant d'ouvrir la formation à d'autres apprenants.
- **Relecture par un locuteur vietnamien du Nord** (MOD-E01) : phrases de
  « Combien de fois ? », classificateurs, page des tons, 74 termes hors
  corpus (DEC-0027 ; 9 séries utilisent une syllabe inventée dès E2),
  traductions (*chưng*, *à*, *chi*, *lẽ*) ; étymologies manquantes.
- Liste de fréquence de référence (R-LEX-07), pour A1 (en M0 : « mot
  courant », DEC-0035).
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
| 1.13 | 2026-10-31 | Outil de validation des audios (DEC-0065). |
| 1.14 | 2026-10-31 | Thu Minh écartée, Ban Mai pour les leçons de sons (DEC-0066). |
| 1.15 | 2026-11-01 | MOD-B01 : § 4 voix FPT.TTS-ultra F4 / H6 et débit lent emprunté (DEC-0067, 0068), voyelle seule en E1 (DEC-0070), signalement d'un son (DEC-0069), audios intermédiaires dans Git (DEC-0071) ; § 3 décisions jusqu'à DEC-0071, suivi des modifications, état d'avancement, essai Ultra ; § 5 état au 2026-11-01 (5 506 audios, lecteur 0.21, Git) ; § 6 points ouverts renvoyés au suivi des modifications ; § 2 noter chaque modification dans le suivi. Repassé en BROUILLON (DOC-21). Analyse d'impact (DOC-35) : `sorties` vide, aucun document en aval. |
| 1.15 | 2026-11-01 | Validé par Christophe (statut VALIDE). |
