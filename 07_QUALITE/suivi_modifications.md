---
id: QUAL-SUIVI-MODIF
titre: Suivi des modifications du projet
statut: BROUILLON
version: 0.38
date: 2026-11-07
resume: >
  Registre vivant : (1) le journal de toutes les modifications faites au
  projet depuis la refonte du 2026-10-28, jour par jour, avec les commits Git
  et les décisions ; (2) la liste de tous les besoins de modification futurs
  relevés dans les documents, numérotés, classés par thème et par priorité.
entrees: [REG-DOC, REG-DEC, CTX-IA, QUAL-AVANCEMENT-20261031]
sorties: []
sources:
  - Historique Git de C:\VIET_PROJECT (.git/logs/HEAD), relevé le 2026-11-01
  - Dates de modification des fichiers de C:\VIET_PROJECT, relevées le 2026-11-01
  - Sections « Historique », « À décider », « Hypothèse », « Points ouverts », « Reste à faire » et « Écarts » de tous les documents .md du projet
  - 07_QUALITE/audios_a_refaire.csv (170 lignes, 2026-10-31)
---

# Suivi des modifications du projet

## Résumé

- **Ce qui a été fait** : 73 décisions (DEC-0001 à DEC-0073) et 34 commits Git
  entre le 28 octobre et le 1er novembre 2026. Le travail du 31/10 après
  15 h 15 (DEC-0067 à DEC-0070) est enregistré dans Git depuis le 01/11
  (commit `1d5c57e`, MOD-A01).
- **Ce qui reste à faire** : **86 besoins** relevés (section 3), dont
  **17 de priorité haute** (MOD-A01 à MOD-A04 et MOD-B01 à MOD-B06 faits le 01/11 ; MOD-A05 décidé : DEC-0071).
  L'historique est sauvegardé hors du PC depuis le 01/11 (dépôt privé GitHub,
  MOD-A02). Les documents sont d'accord avec DEC-0067 (MOD-B02 à B06).
  MOD-H01, H02 et H04 sont faits ou clos (DEC-0072 à DEC-0075 : t et m
  avant les voyelles de L01, syllabes sans sens, tons des mots d'exemple
  vérifiés conformes, rappel court pour -m/-n en L08/L10). Le plus
  urgent : générer les audios Ultra des autres leçons (MOD-C01).

| Thème | Nombre | Haute | Moyenne | Basse |
|---|---|---|---|---|
| A. Git et sauvegarde | 5 | 3 | 2 | 0 |
| B. Cohérence des documents après DEC-0067 | 13 | 7 | 6 | 0 |
| C. Audios et voix | 17 | 5 | 8 | 4 |
| D. Lecteur d'activités | 24 | 1 | 16 | 7 |
| E. Contenus et relecture par un locuteur | 10 | 1 | 7 | 2 |
| F. Règles et fondations | 7 | 0 | 4 | 3 |
| G. Outils, enveloppe, Anki | 6 | 0 | 1 | 5 |
| H. Pédagogie et programme | 4 | 1 | 3 | 0 |
| **Total** | **86** | **18** | **47** | **21** |

---

## 1. Mode d'emploi

### 1.1 Ajouter un besoin

1. Choisir le thème (A à H) et prendre le **numéro suivant** du thème
   (`MOD-C16`, par exemple). Un numéro ne change jamais et n'est jamais
   réutilisé (DOC-26).
2. Remplir une ligne : besoin, origine (document ou constat), documents ou
   fichiers touchés, priorité, état.
3. Si le besoin demande un **arbitrage**, il passe à l'état `à décider` ; la
   réponse devient une décision `DEC-xxxx` dans `02_REGLES/DECISIONS.md`
   (DOC-22).

### 1.2 Priorités et états

| Priorité | Sens |
|---|---|
| **Haute** | bloque la suite, risque de perte, ou contradiction entre documents |
| **Moyenne** | nécessaire avant d'ouvrir la formation à d'autres apprenants |
| **Basse** | plus tard, ou amélioration |

| État | Sens |
|---|---|
| `à faire` | rien de commencé |
| `en cours` | commencé |
| `à décider` | demande un choix de Christophe |
| `à vérifier` | fait ou hypothèse, à contrôler |
| `fait` | terminé ; la ligne passe au journal (section 2) avec la date |

### 1.3 Clore un besoin

Quand un besoin est fait : noter la date et la décision dans la colonne
« État », ajouter une ligne au journal (section 2), puis enregistrer dans
Git (`git add .` puis `git commit -m "MOD-xxx : …"`). Une ligne `fait` est
gardée, pas supprimée.

---

## 2. Journal des modifications réalisées

> **Fait** : chaque ligne vient de l'historique Git ou de
> `02_REGLES/DECISIONS.md`. Les heures sont celles de Paris.

### 2.1 Mardi 28 octobre 2026 : refonte (23 commits, DEC-0001 à DEC-0036)

| Heure | Commit | Modification |
|---|---|---|
| 13 h 56 | `769b939` | Nouvelle structure en 7 dossiers + `_ARCHIVES`, règles documentaires (DEC-0001 à 0003 : structure, noms en français, Git) |
| 14 h 04 – 14 h 38 | `24837a3` à `d75da9f` | Durée et ordre du Module 0 (DEC-0004, 0005), tons glottalisés (0006), deux volets écoute / production (0007), corrections factuelles (0008), accent courant de Hanoï (0009), étapes E1–E5 (0010), écrit (0011), seuils (0012), syllabes inventées (0013) ; fondations FOND-01 à 04 **validées** (DEC-0014) |
| 16 h 29 – 17 h 10 | `bd83f87` à `2ca570d` | Outils WordPress + Anki (DEC-0015, 0016), CSV source de vérité (0017), un code par son (0018), 14 leçons (0019), mots supports (0020), pas de transcription (0021), symboles des tons (0022), audio (0023), images (0024), séries de 2 à 4 termes (0025, 0026) ; `classificateurs.csv` ; 95 séries minimales |
| 17 h 22 – 19 h 02 | `ff84cfb` à `1cba974` | Termes hors corpus (DEC-0027) ; catalogue des activités (PROG-ACT) ; étiquettes E2–E3 (0028, 0029) ; test PhoWhisper ; lecteur d'abord en site statique (0030) ; programme du Module 0 (PROG-M0, 0031) ; points P2 à P6 (0032 à 0036) |
| 20 h 07 | `48aa141` | Lecteur d'activités, version d'essai 0.1 (volet écoute E1–E3) |

### 2.2 Mercredi 29 octobre 2026 (1 commit, DEC-0037 à DEC-0046)

| Heure | Commit | Modification |
|---|---|---|
| 10 h 19 | `4844bdb` | DEC-0036 corrigée ; L01 en deux parties (0037) ; mots repères et catégories de sons (0038) ; script audio FPT |
| (commit non identifié, au plus tard le 30/10 à 20 h 10) | — | E1 découverte de chaque son seul (0039) ; voix FPT retenues (0040) ; échauffement « Pareil ou différent ? » (0041) ; place du son (0042) ; tons sans audio lent (0043) ; i retiré des contrastes de L01 (0044) ; une voix d'abord pour les tons (0045) ; repères des finales (0046) ; 2 238 audios générés |

### 2.3 Jeudi 30 octobre 2026 (7 commits, DEC-0047 à DEC-0064)

| Heure | Commit | Modification |
|---|---|---|
| 12 h 41 – 12 h 59 | `2f94810`, `aaecad0`, `3200e5c` | Mode test (0047) ; Thu Minh écartée une première fois (0048) ; CONTEXTE_IA 1.12 ; volet production E4 d'abord (0049), page d'essai du micro |
| 20 h 10 | `410d383` | Thu Minh + Huy Phong pour les leçons de sons (0055) ; E4 avec micro et courbes (0050) ; mode essai (0051) ; page « Les 6 tons » (0052, 0053) ; « Combien de fois ? » (0054) ; mesure du contraste des tons |
| 20 h 37 | `29f83ea` | Phrases de « Combien de fois ? » (0056), écoute lente non comptée (0057) |
| 22 h 21 | `627c075` | Trois écoutes des phrases (0058) ; débit lent de Thu Minh 0,8 (0059) ; classificateurs en E1 et E4 (0060 à 0062) |
| 22 h 31 | `8966ee6` | Lettres vietnamiennes du son dès E1 (0063) ; « Les 6 tons » : 10 séries (0064) |

### 2.4 Vendredi 31 octobre 2026 (2 commits + travail enregistré le 01/11)

| Heure | Commit | Modification |
|---|---|---|
| 13 h 40 | `0fab1ab` | État d'avancement au 31/10 (QUAL-AVANCEMENT-20261031) |
| 15 h 15 | `5002119` | Thu Minh écartée, Ban Mai pour les leçons de sons (DEC-0066) ; probablement aussi l'outil de validation des audios (DEC-0065, non cité dans le message) ; CONTEXTE_IA 1.14 |
| 15 h 17 – 23 h 36 | — | Travail enregistré le 01/11 dans `1d5c57e` : voir 2.5 et 2.6 |

### 2.5 Modifications du 31/10 après 15 h 15 (enregistrées le 2026-11-01, commit `1d5c57e`)

| Fichier | Modification |
|---|---|
| `02_REGLES/DECISIONS.md` (v1.61 à 1.64) | **DEC-0067** voix FPT.TTS-ultra F4 Ban Mai et H6 Quang Anh, débit lent emprunté à F1 et H4, mots espacés par virgules ; **DEC-0068** silence de début gardé brut, fin complétée à 0,35 s ; **DEC-0069** bouton « ⚑ Signaler un son » ; **DEC-0070** voyelle seule avant les mots en E1 |
| `04_DONNEES/voix.csv` | F4 et H6 actives ; F1, H3, H4 inactives ; colonne `slow_from` |
| `04_DONNEES/exemples_e1.csv`, `audios.csv`, `courbes_modele.csv` | voix F4 / H6 ; nouveaux audios ; courbes du modèle |
| `04_DONNEES/00_modele_donnees.md` | colonne `slow_from` (en-tête non mis à jour : voir MOD-B06) |
| `05_PRODUCTION/03_audio.md` (v0.14 à 0.17) | § 1 bis voix actuelles ; signalement ; voyelle seule |
| `05_PRODUCTION/lecteur/lecteur.js`, `lecteur.css` | signalement d'un son (DEC-0069), voyelle seule (DEC-0070) |
| `05_PRODUCTION/tools/` | `generer_audio_fpt.py`, `generer_lecteur.py`, `valider_audios.py`, `courbes_modele.py`, `decoupe_audio.py`, `choisir_exemples_e1.py`, `validation_audios.html` modifiés ; `essai_ultra.py`, `essai_espacement.py`, `essai_voyelles.py` nouveaux (vérifié avec `git status` le 01/11) |
| `07_QUALITE/` | `essai_tts_ultra_2026-10-31.md` (v1.0 à 1.5), `audios_a_refaire.csv` (170 lignes), `validations/validations_audios_2026-10-31_1527.csv` |
| `04_DONNEES/audio/` | 1 015 fichiers nouveaux, modifiés ou supprimés (`git status`, 01/11), dont : F1 (« Combien de fois ? », DEC-0066) pour L01, L04, L05, L06, L08, L09 ; **F4 et H6 pour L01** (essai de DEC-0067). Le premier relevé, partiel, en comptait au moins 592 |

### 2.6 Dimanche 1er novembre 2026

| Besoin | Résultat |
|---|---|
| MOD-A01 | Fait à 12 h 09, commit `1d5c57e` (`git add -A`) : les 23 fichiers de documents, données, lecteur et scripts de la section 2.5 (dont `suivi_modifications.md` v0.7), et 1 015 audios nouveaux, modifiés ou supprimés. Vérification demandée : `git status` vide après le commit |
| MOD-A03 | Vérifié : 6 784 MP3 suivis par Git (88 Mo), dont 2 296 dans des dossiers que le `.gitignore` devrait exclure ; dépôt compatible avec GitHub. Suite : MOD-A05 |
| MOD-A05 | Décidé (DEC-0071, option B) : `_bruts`, `_anciens` et `_essais` restent suivis par Git ; leurs lignes sont retirées du `.gitignore` |
| MOD-A04 | Fait (commit `429419e`) : `cle api FPT.txt` retiré du suivi de Git, toujours vide dans l'historique (aucune clé envoyée sur GitHub) |
| MOD-A02 | Fait vers 12 h 40 : dépôt privé GitHub `cappleinouest-lang/viet-project` créé vide, relié (`git remote add origin`), historique envoyé (`git push -u origin main`, 14 079 objets, 233 Mo) |
| MOD-B01 | `CONTEXTE_IA.md` v1.15 : voix F4 / H6 et débit lent emprunté (§ 4), état au 01/11 (§ 5 : 5 506 audios dont 3 494 validés, F4 / H6 pour L01 seulement, lecteur 0.21, Git), points ouverts renvoyés à ce suivi (§ 6), décisions jusqu'à DEC-0071 ; document repassé en BROUILLON (DOC-21), à revalider par Christophe |
| MOD-B02 à B06 | Documents mis d'accord avec DEC-0067 (voix F4 / H6, débit lent emprunté à F1 / H4) et complétés avec DEC-0069 (signalement) et DEC-0070 (voyelle seule) : PROD-AUDIO 0.18 (titre, § 1 refait avec les 5 506 audios comptés par voix, liens), PROD-LECT 0.21, PROD-AF-LECT 0.3 (« Combien de fois ? », E4, page des tons, RG-16 à RG-19, écart EC-06 : en-tête de `lecteur.js`), PROG-M0 0.12, PROG-ACT 0.16, DATA-MODELE 0.20. Écart relevé : 10 voyelles seules dans `audios.csv` contre 22 prévues (DEC-0070), à vérifier |
| Incident | Entre 12 h 46 et 12 h 49, une autre conversation travaillant en même temps a réécrit `CONTEXTE_IA.md` (version 1.15 sans MOD-A02) et `suivi_modifications.md` (ancienne 0.8). Réparé : conversation arrêtée, suivi récupéré par `git restore` (0.11), CONTEXTE_IA remis en 1.16 validée. Règle : **une seule conversation à la fois** sur `C:\VIET_PROJECT` |
| MOD-H01 | Décidé : **DEC-0072** (choix de Christophe) : t et m découverts en E1 avant les voyelles de L01 ; mots d'exemple t/m + voyelle au ton ngang ; règle de préférence pour L02 à L13 ; un mot pour ê à chercher. Mise en œuvre à faire. Nouveau besoin MOD-H03 (séries d'E2 de la partie A) |
| MOD-H01 | **Fait** : DEC-0073 (syllabes sans sens en E1 : *te*, *mo*, *mô*, *be*) ; 5 mots ajoutés au corpus (W0340 à W0344) ; `choisir_exemples_e1.py` (règle de préférence), `fabriquer_syllabes_e1.py` et `syllabes_e1.csv` ; lecteur (t et m d'abord en partie A de L01, mot écrit en mode test) ; 42 audios de L01 (écoutés : « très bien ») ; 4 documents mis à jour. Reste : valider ces audios (MOD-C03) |
| MOD-B13 | `CONTEXTE_IA.md` v1.17 (DEC-0072, DEC-0073, audios de L01, tarif d'Ultra, points ouverts) ; résumé de ce suivi corrigé (73 décisions, 84 besoins) ; CONTEXTE_IA repassé en BROUILLON, à revalider |
| MOD-H03 | DEC-0074 : séries S0001, S0004 et S0007 de `paires_minimales.csv` remplacées par des syllabes t/m + voyelle ; aucun audio à produire (déjà générées pour l'E1 avec DEC-0072, DEC-0073) |
| MOD-H02 | Contrôle systématique des 265 mots d'exemple de L02 à L13 : aucun ton pas encore ouvert à sa leçon. Clos sans modification |
| MOD-H04 | DEC-0075 : rappel court (1 mot, 1 voix, « déjà vu en L01 ») pour -m et -n en L08/L10, au lieu d'une découverte complète. **Mise en œuvre faite** : colonne `e1_rappel` dans `lecons.csv` (L08 : -m et -n ; L10 : -n), `generer_lecteur.py` (1 mot rang 1, voix F4), `lecteur.js` (écran « Rappel », bouton Écouter seul). Reste : régénérer le lecteur et tester dans le navigateur |

### 2.7 Lundi 2 novembre 2026

| Besoin | Résultat |
|---|---|
| MOD-C01 | Plan de génération de L02 à L13 refait selon DEC-0077 (choix de Christophe : leçons de tons L02, L03, L07, L11 entièrement en F1 + H3, sans débit lent ; lent de F4 = F1, lent natif de H4 0,6, de F1 0,7, de H3 0,6 ; audios existants réutilisés). Résultat : 985 fichiers à créer, 13 016 caractères, environ 6 200 ₫ (dont « Combien de fois ? » en H3 : 644 fichiers, 11 730 caractères, environ 4 900 ₫). Existence vérifiée dans `audios.csv` seulement. `voix.csv` : `listen_sounds` vrai pour F4 et H4 seulement, `listen_tones` vrai pour F1 et H3 seulement. `generer_audio_fpt.py` : table `VOIX_USAGE` / `VOIX_TONS`, pas de débit lent en leçon de tons (DEC-0043) pour toutes les écoutes, `VOIX_REFERENCE_TONS = ['F1', 'H3']`, colonnes `voice_f` / `voice_h` d'`exemples_e1.csv` plus lues. Plan du script modifié vérifié (mêmes totaux), aucun audio généré |
| MOD-D01 | Lecteur adapté à DEC-0077. `generer_lecteur.py` : tableau `VOIX_PAR_USAGE` (E1 voyelle seule et syllabes sans sens F1 + H4, mots d'exemple F4 + H4, leçons de tons et page « Les 6 tons » F1 + H3, « Combien de fois ? » F1 + H3), modèle d'E4 F4 ; colonnes `voice_f` / `voice_h` d'`exemples_e1.csv` plus lues ; nouvelles données par leçon `voix_combien` et `voix_unique` (F1 en leçon de tons, à la place de la voix modèle F4 : DEC-0045) ; avertissement si une voix prévue est inactive. `lecteur.js` : « Combien de fois ? » sur `l.voix_combien`, phases à une voix des leçons de tons sur `l.voix_unique`. Test sur une copie (Chromium, `--non-valides`, audios absents remplacés par un fichier factice) : page des tons F1 / H3 (52/52 audios et courbes), E1 de L01 voyelle e (seule F1 + H4, mots F4 + H4, syllabe F1 + H4), E4 F4 (lent F1), « Combien de fois ? » F1 / H3, L02 échauffement et E2 en F1 seule ; aucune erreur JavaScript. PROD-LECT 0.24 |
| MOD-D25 | E1 : séquences d'écoute. Nouveau `tools/concatener_e1.py` (numpy + soundfile de `.venv-asr`) : un MP3 par voix, morceaux collés sans silence ajouté, ordre voyelle seule → syllabes sans sens → mots ; une voix par fichier (choix de Christophe) : femme F1 (voyelle + syllabes) puis F4 (mots), homme H4 (H3 en leçon de tons) ; sortie `04_DONNEES/audio/e1_sequences/` + `sequences_e1.csv` (morceaux, débuts, durée). `generer_lecteur.py` : clé `sequence` dans `decouverte` (seulement si les morceaux sont à jour), tuiles syllabes avant mots, séquences copiées. `lecteur.js` : écoute **automatique** à l'ouverture de l'écran (F puis H), séquence au débit normal, surlignage et « ⚑ Signaler » sur le fichier d'origine ; lent, clic sur une tuile, E2–E5, page des tons inchangés ; leçons de tons et rappels courts inclus. Ordre : `generer_lecteur` → `concatener_e1 --lecon M0-L01` → `generer_lecteur`. Test sur une copie (Chromium, audios factices) : L01 36 séquences (15 sons ; 6 sons ont 2 parties femme), lecture auto F1 → F4 → H4, « Homme » et « lentement » corrects, aucune erreur JavaScript. À faire sur le PC : lancer les 3 commandes, écouter L01 |

---

## 3. Besoins de modification futurs

### A. Git et sauvegarde

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-A01 | **Enregistrer dans Git** tout le travail du 31/10 après 15 h 15 (section 2.5) | constat du 2026-11-01 | tout le projet | **Haute** | **fait** (2026-11-01, commit `1d5c57e`) |
| MOD-A02 | **Sauvegarde hors du PC** : dépôt privé GitHub (l'historique n'existe que sur le PC) | QUAL-AVANCEMENT § 7 n° 2 ; risque « perte totale » | Git | **Haute** | **fait** (2026-11-01) : dépôt **privé** `https://github.com/cappleinouest-lang/viet-project`, branche `main` suivie (`git push -u origin main`, 233 Mo envoyés, commit `429419e`). Désormais : `git push` après chaque commit |
| MOD-A03 | Vérifier si les **milliers de MP3** de `04_DONNEES/audio/` sont suivis par Git (le `.gitignore` n'exclut que `_bruts`, `_essais`, `_anciens`) : poids du dépôt, limite de GitHub. **Résultat (lecture de `.git/index`, 2026-11-01 ; recoupé par Christophe avec `git ls-files 04_DONNEES/audio/_bruts` : 2 232)** : hypothèse **confirmée**. Sur 6 860 fichiers suivis, **6 784 sont des MP3** (88 Mo sur 89 Mo) : 4 486 à la racine de `audio/` (46,6 Mo), **mais aussi 2 232 dans `_bruts` (40,5 Mo), 45 dans `_essais` et 19 dans `_anciens`** : ces fichiers ont été ajoutés à Git avant la règle du `.gitignore`, qui ne retire jamais un fichier déjà suivi (voir MOD-A05). Le dossier `audio/Nouveau dossier` (2 MP3) est encore suivi mais n'existe plus sur le disque : sa suppression sera enregistrée avec MOD-A01. Dépôt compressé (`.git/objects/pack`) : 88 Mo. Plus gros fichier suivi : `audios.csv`, 0,4 Mo. **Compatible avec GitHub** (limite stricte de 100 Mo par fichier ; dépôt conseillé sous 1 Go, à revérifier dans la documentation de GitHub). Point de vigilance : chaque génération d'audios ajoute son poids à l'historique, même si les fichiers sont ensuite supprimés. Non compté : les MP3 créés après le dernier commit (MOD-A01) | constat du 2026-11-01 | `.gitignore`, MOD-A02, MOD-A05 | **Haute** | **fait** (2026-11-01) |
| MOD-A04 | Fichier vide `cle api FPT.txt` à la racine : la clé doit rester **hors** du projet (DOC-04). Il est ignoré par Git, mais à déplacer ou laisser vide | constat du 2026-11-01 | DOC-04 | Moyenne | **fait** (2026-11-01) : le fichier était en réalité **suivi** par Git (ajouté le 30/10 dans `2f94810`, avant la règle du `.gitignore`), mais toujours **vide** (`git log --stat` : 0 ligne) : aucune clé dans l'historique. Retiré du suivi avec `git rm --cached` (commit `429419e`), resté sur le disque, désormais ignoré (`git check-ignore`). Fait avant MOD-A02 |
| MOD-A05 | **Retirer de Git les audios intermédiaires** déjà suivis malgré le `.gitignore` (`_bruts`, `_essais`, `_anciens` : 2 296 MP3, 41 Mo), avec `git rm -r --cached` (retire les fichiers de Git **sans les effacer du disque**). Ils restent dans l'historique déjà enregistré : le dépôt ne maigrit pas, mais les prochains commits ne les suivent plus. À décider : retirer (cohérent avec la règle DOC-19) ou garder suivis (et alors corriger le `.gitignore`). À faire **avant** MOD-A02 (MOD-A01 a été fait avant, le 01/11 : les audios intermédiaires déjà suivis et modifiés y sont donc enregistrés) | MOD-A03, 2026-11-01 | `.gitignore`, DOC-19, MOD-A01, MOD-A02 | Moyenne | **fait** (2026-11-01) : option B, **garder** dans Git et corriger le `.gitignore` (DEC-0071) ; le texte « cohérent avec DOC-19 » était inexact, DOC-19 n'exclut pas ces dossiers |

### B. Cohérence des documents après DEC-0067

> **Fait** : DEC-0067 remplace les voix F1, F3, H3, H4 par **F4 Ban Mai** et
> **H6 Quang Anh** (FPT.TTS-ultra) pour toutes les écoutes, E1, la page des
> tons et le modèle d'E4. Les documents ci-dessous disent encore autre chose.

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-B01 | **CONTEXTE_IA** v1.15 : § 4 « Audio » (dit encore F1 + H4 pour les sons, F1/H3/H4 pour les tons, modèle F1), § 5 état (daté du 30/10, lecteur 0.13 au lieu de 0.21, 4 491 audios), § 6 points ouverts, nombre de décisions (DEC-0070) | constat du 2026-11-01 | CTX-IA | **Haute** | **fait** (2026-11-01, CTX-IA v1.15 ; à revalider) |
| MOD-B02 | **PROD-AUDIO** : titre « FPT.TTS-pro » périmé ; § 1 tableau des voix et totaux du 29/10 ; historique (ligne 0.10 mal placée) ; champs `entrees` et `sorties` vides (DOC-30) | constat du 2026-11-01 | `05_PRODUCTION/03_audio.md` | **Haute** | **fait** (2026-11-01, PROD-AUDIO v0.18) |
| MOD-B03 | **PROD-LECT** : § 4 « voix F1, H3, H4 simulées » ; § 5 « modèle F1 » ; version 0.20 du 30/10 sans DEC-0065 à DEC-0070 | constat du 2026-11-01 | `05_PRODUCTION/02_lecteur_activites.md` | **Haute** | **fait** (2026-11-01, PROD-LECT v0.21) |
| MOD-B04 | **PROD-AF-LECT** (analyse fonctionnelle, état du 29/10) : voix F1 dans les règles RG-11, § 6 ; exemples `W0057-H3`, Le Minh ; ajouter signalement (DEC-0069), voyelle seule (DEC-0070), « Combien de fois ? », E4, page des tons | constat du 2026-11-01 | `05_PRODUCTION/04_analyse_fonctionnelle_lecteur.md` | **Haute** | **fait** (2026-11-01, PROD-AF-LECT v0.3) |
| MOD-B05 | **PROG-M0** § 3 : « 3 voix actives (F1, H3, H4) », « 2 238 audios » ; **PROG-ACT** ligne 47 : « une seule voix (F1) » | constat du 2026-11-01 | `03_PROGRAMME/` | **Haute** | **fait** (2026-11-01, PROG-M0 v0.12, PROG-ACT v0.16) |
| MOD-B06 | **DATA-MODELE** : en-tête (v0.19, date du 30/10) non mis à jour alors que `slow_from` a été ajouté ; exemples F1 / H3 dans `voice_f` / `voice_h` | constat du 2026-11-01 | `04_DONNEES/00_modele_donnees.md` | **Haute** | **fait** (2026-11-01, DATA-MODELE v0.20) |
| MOD-B07 | **REG-REGLES** R-AUD-02 (« au moins 2 voix », variété) : depuis DEC-0067, une seule femme et un seul homme, et le personnage d'homme change entre lent (Huy Phong) et normal (Quang Anh). Vérifier la conformité, ou noter l'écart | DEC-0066, DEC-0067 | `02_REGLES/REGISTRE_REGLES.md` | **Haute** | à décider |
| MOD-B08 | **Regénérer** `CARTE_DOCUMENTAIRE.md` (datée du 29/10) avec `build_doc_map.py` | QUAL-AVANCEMENT § 7 n° 15 | carte | Moyenne | à faire |
| MOD-B09 | Rendre les **liens réciproques** (DOC-32) : CTX-IA, PROD-AUDIO, PROD-LECT, REG-DEC et QUAL-CONTRASTE-TONS ne citent pas en `sorties` les rapports QUAL-AVANCEMENT, QUAL-CONTRASTE-TONS, QUAL-ESSAI-ULTRA ; et ce document (QUAL-SUIVI-MODIF) | essai de `build_doc_map.py` du 2026-11-01 | en-têtes | Moyenne | en cours (PROD-AUDIO et PROD-LECT faits le 2026-11-01 avec MOD-B02, B03) |
| MOD-B10 | Relier ou classer les 2 documents **sans aucun lien** : PROD-COMP-SUPPORT-20261028, PROD-DOSSIER-SUPPORT-20261028 | carte documentaire | `05_PRODUCTION/` | Moyenne | à faire |
| MOD-B11 | **PROD-ARCH** (v0.4) : rédigé autour de WordPress (extension de progression, Local, hébergeur) alors que DEC-0030 laisse le choix WordPress ou Firebase ; point ouvert 3 « voix de référence » à mettre à jour (DEC-0067) | constat du 2026-11-01 | `05_PRODUCTION/01_architecture_outils.md` | Moyenne | à faire |
| MOD-B12 | `README.md` de la racine et des dossiers : brouillons v0.1–0.2 du 28/10, à relire | constat du 2026-11-01 | `README.md` | Moyenne | à faire |
| MOD-B13 | **CONTEXTE_IA** v1.16 en retard sur DEC-0072, DEC-0073, MOD-H01 et MOD-B02 à B06 (§ 3 à § 6) ; résumé de ce suivi (70 décisions, MOD-H01 « à mettre en œuvre ») | relecture du 2026-11-01 | `CONTEXTE_IA.md`, ce document | Moyenne | **fait** (2026-11-01, CONTEXTE_IA v1.17, à revalider par Christophe) |

### C. Audios et voix

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-C01 | **Écouter L01 en F4 / H6 dans le lecteur**, puis générer les autres leçons (environ 1 700 fichiers, 19 000 caractères) | DEC-0067 « Mise en œuvre » | audios | **Haute** | **plan refait** (2026-11-02, DEC-0077) : L02 à L13, **985 fichiers à créer, 13 016 caractères, environ 6 200 ₫** (F4 240 fichiers / 870 car. ; H3 651 / 11 852 ; H4 59 / 192 ; F1 35 / 102) ; audios F1, H3, H4 existants réutilisés ; `voix.csv` et `generer_audio_fpt.py` mis à jour (section 2.7). **Reste** : lancer la génération, leçon par leçon (`--lecon`) ; L01 et `generer_lecteur.py` encore à mettre d'accord avec DEC-0077 |
| MOD-C02 | **Vérifier le tarif de FPT.TTS-ultra** avant la génération complète | PROD-AUDIO § 1 bis | coût | **Haute** | **fait** (2026-11-01) : le tarif n'est pas affiché sur la marketplace ; déduit de l'historique des transactions (1 jeton = 1 caractère envoyé, vérifié le 01/11 : 19 caractères → 19 jetons par voix). FPT.TTS-pro et FPT.AI-VITs : environ **0,42 ₫** par caractère (8 ₫ pour 19) ; **FPT.TTS-ultra : environ 1,3 ₫** (13 ₫ pour 10, 4 ₫ pour 3, le 31/10), soit environ 3 fois plus. Débits arrondis au đồng. Estimation pour les autres leçons : de l'ordre de 25 000 ₫ en Ultra. Solde le 01/11 avant génération : 988 058 ₫ |
| MOD-C03 | **Valider les audios** à l'écoute (R-AUD-01) ; sans cela le lecteur reste en mode d'essai. Le nombre à écouter (3 664 au plan du 31/10) change avec DEC-0067 : à recompter | QUAL-AVANCEMENT § 7 n° 1 ; DEC-0065 | `audios.csv` | **Haute** | à faire |
| MOD-C04 | **Trier `audios_a_refaire.csv`** : sur 170 refus, **138** concernent des voix devenues inactives au débit concerné (F3 : 95 ; F1 normal : 22 ; H4 normal : 13 ; H3 : 8). Seuls **32 restent utiles** : les lents de H4 (25) et de F1 (7), empruntés par H6 et F4. Ne pas tout regénérer (coût inutile) | calcul du 2026-11-01 sur le fichier | `07_QUALITE/audios_a_refaire.csv`, `generer_audio_fpt.py --liste` | **Haute** | à faire |
| MOD-C05 | **Contraste des tons plus faible en Ultra** (2,3 contre environ 4 pour F1 et H4) alors que F4 et H6 servent aussi aux leçons de tons : réévaluer le choix des voix des leçons de tons (le « locuteur le plus adapté » reste à choisir) | QUAL-ESSAI-ULTRA ; DEC-0067 | voix des tons | Moyenne | **fait** (DEC-0077) : tons confiés à F1 + H3 (meilleur contraste à l'audit), plus à F4/H6 |
| MOD-C06 | **Voix d'homme différente** entre lent (Huy Phong) et normal (Quang Anh) : vérifier que cela ne gêne pas | DEC-0067 point 2 | `voix.csv` | Moyenne | **plus pertinent** (DEC-0077) : H6 écartée, Huy Phong (H4) sert au même débit normal pour ses usages |
| MOD-C07 | **Phrases lentes** à 0,75 : jugées bonnes, non appliquées (coût) ; à revoir | DEC-0067 point 7 | `comptage.csv`, audios | Moyenne | à décider |
| MOD-C08 | Silence de début des fichiers Ultra (plus de 200 ms) gardé brut : le raccourcir (`ROGNER_ULTRA = True`) s'il gêne à l'usage | DEC-0068 | `generer_audio_fpt.py` | Moyenne | à vérifier |
| MOD-C09 | **Deuxième voix de femme du Nord** (autre fournisseur ou enregistrement natif) | DEC-0066 « Conséquence » ; CTX-IA § 6 | `voix.csv` | Moyenne | à faire |
| MOD-C10 | **Enregistrement natif** au moins pour la page des tons et le modèle d'E4 (la synthèse FPT rend mal *hỏi* et *nặng*) | QUAL-AVANCEMENT, risques ; QUAL-CONTRASTE-TONS | audios | Moyenne | à décider |
| MOD-C11 | Huy Phong (H4) : son « numérique » par moments ; mots concernés et origine (synthèse ou traitement) à préciser. Concerne toujours le débit lent de H6 | QUAL-ESSAI-ULTRA | H4 lent | Moyenne | à vérifier |
| MOD-C12 | Diphtongues et triphtongues **seules** en E1 : à essayer d'abord | DEC-0070 point 2 | `essai_voyelles.py` | Basse | à faire |
| MOD-C13 | **Voix d'enfant** : source à trouver | DEC-0023 ; `voix.csv` (E1 `planned`) | `voix.csv` | Basse | à faire |
| MOD-C14 | Audios lents des mots qui ne servent qu'en leçons de tons : générés mais jamais joués (coût inutile, faible) | PROD-AF-LECT EC-03 | plan de génération | Basse | à faire |
| MOD-C15 | Réévaluer FPT.TTS-ultra plus tard pour les **phrases et dialogues** (A1–A2) | QUAL-ESSAI-ULTRA, résumé | audios A1 | Basse | plus tard |
| MOD-C16 | **Repli « voix système » de mauvaise qualité** : quand une leçon n'a pas encore de MP3 FPT validé, le lecteur lit le texte avec la synthèse vocale de l'appareil (Web Speech API, `vi-VN`, section 3 de `lecteur.js`). Christophe la juge mauvaise (2026-11-01). Les vrais fichiers F4 / H6 **ne sont pas en cause**. Repli provisoire qui disparaît dès que les MP3 existent (MOD-C01) ; à décider : le **désactiver** pendant la production (afficher « audio à venir » au lieu d'une mauvaise voix) | Christophe, 2026-11-01 | `lecteur.js` (section 3, `jouer`, `afficherBandeau`) | Moyenne | à décider |
| MOD-C17 | **Audit approfondi des locuteurs FPT** déjà utilisés (F1, F3, H3, H4, F4, H6) : noter chaque voix sur 4 dimensions — lettres/voyelles seules, mots courts CV et VC (consonnes de début et de fin), ralenti, espacement des mots — sur une batterie de test commune, en réutilisant `valider_audios.py` et les validations existantes (3 664 écoutes, anciennes voix seulement ; F4 / H6 Ultra à écouter car seulement L01 produit). Sortie : tableau voix × type d'activité → valable / à éviter. Tranche aussi MOD-B07 (R-AUD-02). À faire avant MOD-C01 | Christophe, 2026-11-01 | `voix.csv`, `07_QUALITE/validations`, `valider_audios.py`, batterie de test à écrire | **Haute** | **fait** (2026-11-02, DEC-0077) : 322 audios (4 passages), stratégie A retenue — F1/F4/H3/H4 répartis par usage, F3/H1/H2/H5/H6 écartées |

### D. Lecteur d'activités

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-D01 | Regénérer le lecteur avec F4 / H6 et vérifier la page des tons, E1 (voyelle seule) et E4 (courbes F4) | DEC-0067, DEC-0070 | `generer_lecteur.py`, `courbes_modele.py` | **Haute** | **fait** (2026-11-02, DEC-0077) : répartition F1/F4/H3/H4 par usage codée et testée sur une copie ; regénération du lecteur sur le PC à lancer |
| MOD-D02 | **E5 Stabiliser** : enchaînements, lecture avant écoute, classificateurs, débit rapide | QUAL-AVANCEMENT n° 5 ; R-AUD-04 | lecteur | Moyenne | à faire |
| MOD-D03 | **Verrou de production** (R-VOL-08) : méthode de mesure ; proposition provisoire « proche » sur 80 % des items d'E5 ; seuils de la courbe à calibrer sur voix natives (paires 2 à 5 à enregistrer) | REG-REGLES ; PROG-ACT § 6 ; FOND-04 § 4 ; PROD-ARCH point 1 | lecteur, règles | Moyenne | à décider |
| MOD-D04 | **L14** : leçon de recyclage, à partir de toutes les séries | PROG-M0 ; PROD-LECT § 5 | lecteur, données | Moyenne | à faire |
| MOD-D05 | Contrôler l'**écart de 3 leçons** entre écoute et production (R-VOL-04) | PROD-LECT § 5 | lecteur | Moyenne | à faire |
| MOD-D06 | R-VOL-07 : le verrou ne contrôle pas « l'absence de confusion majeure avec la leçon précédente » | PROD-AF-LECT EC-01 | lecteur | Moyenne | à faire |
| MOD-D07 | **Phrases de « Combien de fois ? »** pour toutes les leçons (aujourd'hui L01, L02, L04) | QUAL-AVANCEMENT n° 7 | `comptage.csv` | Moyenne | à faire |
| MOD-D08 | **Présenter chaque classificateur** à sa première apparition | QUAL-AVANCEMENT n° 9 | lecteur | Moyenne | à faire |
| MOD-D09 | Verrou ou simple avertissement sur l'échauffement (par exemple 8 justes sur 10) ? | PROD-AF-LECT § 10 | lecteur | Moyenne | à décider |
| MOD-D10 | Essayer un **parcours complet avec les verrous** (mode essai coupé) | QUAL-AVANCEMENT, risques | lecteur | Moyenne | à faire |
| MOD-D11 | Compter le temps d'E1 et de l'échauffement dans « Mes progrès » ? | PROD-AF-LECT § 10 | lecteur | Basse | à décider |
| MOD-D12 | Réglage « Vitesse de la voix de synthèse » : sans objet une fois les audios validés | PROD-AF-LECT EC-04 | lecteur | Basse | à faire |
| MOD-D13 | En-tête de `lecteur.js` : EC-05 (décisions non citées) semble résolu (il cite DEC-0069 et DEC-0070) ; à vérifier puis clore | PROD-AF-LECT EC-05 | `lecteur.js` | Basse | à vérifier |
| MOD-D14 | Progression conservée après regénération : vérifier sur **Android et iPhone** | PROD-AF-LECT, hypothèse ; PROD-COMP-SUPPORT (iPhone) | lecteur | Basse | à vérifier |
| MOD-D16 | **Rendre visible la position de l'apprenant dans la leçon.** À tout moment, l'apprenant doit voir où il en est : quels sons (ou tons) de la leçon il a **déjà étudiés**, lequel il **étudie en ce moment**, et lesquels **restent à étudier**. Exemple en L01, E1 : une frise des sons de la leçon (symbole ou lettres de chaque son), avec un état visible pour chacun (vu / en cours / à venir), et la partie A ou B. Même principe à étendre aux autres étapes (E2–E3 : séries réussies / à travailler ; E4) et à la leçon entière (étapes faites / ouvertes / fermées). **Fait** (lecteur 0.21) : l'écran E1 n'affiche qu'un compteur « Son 3 sur 12 », sans la liste des sons vus et à venir. À décider : contenu exact de la frise, possibilité de toucher un son déjà vu pour y revenir **Partiel** (2026-11-07, lot 2) : la frise des étapes de la leçon montre les étapes faites, en cours et à venir ; restent la frise des sons en E1 et l'état des séries en E2–E3. **Fait** (lecteur du 2026-11-07, lot 6, validé) : en E1, frise des sons de la partie (pastilles avec symbole), état visible (vu ✓, en cours, à venir), toucher un son déjà vu = y revenir. | proposition de Christophe, 2026-11-01 | `lecteur.js`, `lecteur.css` ; PROD-LECT ; PROD-AF-LECT (écrans) | Moyenne | fait |
| MOD-D17 | **Développer le bloc « Écoute de la leçon »** (écran de la leçon, après « Fin d'E3 · L'écrit »). **Fait** (lecteur 0.21) : ce n'est pas une activité, seulement un **état** sans bouton : « Pas encore validée » ou « Validée le … », avec la phrase « Valider l'écoute ouvre la leçon suivante ». La validation se fait en réalité par le bouton « Valider l'écoute de la leçon » de l'écran de l'écrit, sans contrôle supplémentaire. **Choix de Christophe (2026-11-01) : les deux.** (1) Un **bilan d'écoute de fin de leçon** : toutes les séries de la leçon mêlées, débit normal, plusieurs voix, avec un seuil ; il couvrirait R-VOL-07 et MOD-D06 (pas de confusion majeure avec la leçon précédente). (2) Un **récapitulatif** : sons étudiés, scores par série, confusions fréquentes (lien avec MOD-D16 et « Mes progrès »). Restent à décider avant d'écrire la décision DEC : nombre de questions et seuil du bilan, part d'items de la leçon précédente, ordre (bilan puis récapitulatif), et si la validation de l'écoute passe désormais par le bilan plutôt que par l'écran de l'écrit | proposition de Christophe, 2026-11-01 | `lecteur.js` (écran de la leçon, `ecranEcrit`) ; R-VOL-07 ; PROD-LECT ; PROD-AF-LECT | Moyenne | à décider (contenu choisi, paramètres à fixer) |
| MOD-D18 | **Guider vers la prochaine étape.** Constat (lecteur du 31/10, téléphone) : l'écran de L01 aligne 12 cartes semblables, toutes avec le même bouton vert (environ 3,5 hauteurs d'écran), sans indication de l'étape à faire. Proposition : bouton « Continuer : L01 · E2 Distinguer » sur l'accueil ; une seule étape mise en avant dans la leçon ; étapes d'une partie en frise compacte (E1 → E2 → E3 → Combien → Écrit) avec leur état. Lié à MOD-D16 **Fait en partie** (lecteur du 2026-11-07, lot 2, validé) : écran de la leçon avec frise des étapes (✓ E1 → E2 → …), une seule étape en cours en grand bloc, étapes faites en une ligne, étapes fermées dans « Ensuite : … », mode essai : ligne « Aller à : … ». **Reste** : bouton « Continuer : L01 · E2 Distinguer » sur l'accueil (lot 3, avec MOD-D21). **Fait** (lecteur du 2026-11-07, lots 2 et 3, validés) : écran de la leçon avec frise des étapes (✓ E1 → E2 → …) et une seule étape en cours en grand bloc ; bouton « Continuer : L01A · E2 · Distinguer » sur l'accueil, qui ouvre directement la prochaine étape ; mode essai : ligne « Aller à : … ». | relecture de l'interface, 2026-11-01 ; accord de Christophe | `lecteur.js` (accueil, écran de la leçon), `lecteur.css` | Moyenne | fait |
| MOD-D19 | **Le bouton flottant « ⚑ Signaler un son » masque du contenu** : une tuile de mot en E1, la courbe en E4, un réglage, une case de l'écrit. Le placer dans la barre du haut, ou réserver une marge en bas de page **Fait** (lecteur du 2026-11-07, lot 1) : le bouton est dans la barre du haut (⚑ seul sur téléphone, texte complet sur PC) ; il ne masque plus rien. | relecture de l'interface, 2026-11-01 | `lecteur.css`, `lecteur.js` | Moyenne | fait |
| MOD-D20 | **Textes plus clairs.** « 0 justes sur les 0 dernières » et « — séries réussies 2 fois » sont peu compréhensibles ; remplacer par « Pas encore commencé » et une seule barre vers le verrou (« Encore 6 bonnes réponses pour valider ») au lieu des trois cases de chiffres. À vérifier : E3 affiche « Continuer » sans aucune réponse donnée (anomalie possible) **Fait** (lecteur du 2026-11-07, lot 1) : « Pas encore commencé » ; une carte avec barre et phrase (« Encore au moins N bonnes réponses… ») remplace les trois cases ; anomalie d'E3 corrigée (le bouton disait « Continuer » sans réponse : « Commencer » désormais). | relecture de l'interface, 2026-11-01 | `lecteur.js` | Moyenne | fait |
| MOD-D21 | **Accueil avec l'avancement réel** : pour chaque leçon, « en cours, 40 % » ou « validée le … » ; en tête, avancement global écoute et production (rend visible R-VOL-04) ; date de la dernière séance. Aujourd'hui, seulement « Ouverte » **Fait** (lecteur du 2026-11-07, lot 3, validé) : en tête, « N / N leçons · écoute validée · dernière séance le JJ/MM » avec barre ; par leçon, pastille « ✓ Validée le JJ/MM », « En cours · N % » (avec barre sous la ligne), « Ouverte », « Fermée » ou « À venir ». | relecture de l'interface, 2026-11-01 | `lecteur.js` (accueil) | Moyenne | fait |
| MOD-D22 | **Écran de l'écrit** : grouper les termes par série (un cadre par série) ; réduire la place des cases « syllabe inventée (jamais écrite) » (3 sur 13 en L01, partie A) **Fait** (lecteur du 2026-11-07, lot 7, validé) : écran de l'écrit avec un cadre par série (« Série 1, 2… »), syllabes inventées en tuile étroite (classe `tuile-invente`, opacité réduite). | relecture de l'interface, 2026-11-01 | `lecteur.js` (`ecranEcrit`), `lecteur.css` | Basse | fait |
| MOD-D23 | **Détails** : en E1, une tuile de mot sans image (🔊 seul) ; « Mes progrès » vide avant E2 (y montrer les sons d'E1 découverts, lien MOD-D11) ; sur PC, écran de la leçon sur deux colonnes (secondaire, le téléphone passe d'abord) **Partiel** (lecteur du 2026-11-07, lot 8, validé) : « Mes progrès » affiche les sons d'E1 déjà découverts quand il n'y a pas encore de réponses E2 ; écran de la leçon élargi sur PC (≥ 900 px). **Reste** : une image sur la tuile 🔊 seul (à régler dans `images_provisoires.csv` + `generer_lecteur.py`). **Fait** (2026-11-07) : 129 emojis provisoires ajoutés dans `images_provisoires.csv` pour les mots imageables qui n'en avaient pas ; les tuiles 🔊 seul disparaissent après régénération. | relecture de l'interface, 2026-11-01 | `lecteur.js`, `images_provisoires.csv` | Basse | fait |
| MOD-D24 | **Nouvelle case « mot mal prononcé par ce locuteur »** dans le panneau « ⚑ Signaler un son » (et, par cohérence, dans la page de validation des audios, DEC-0065). **Fait** : la liste actuelle (`DEFAUTS` dans `lecteur.js`, 18 cases) contient « son faux », « ton faux ou peu net », « accent non conforme à Hanoï », mais aucune case qui dise que **ce locuteur** prononce mal **ce mot**. **Différence de traitement** : aujourd'hui, tout refus va dans `audios_a_refaire.csv` et l'audio est regénéré **avec la même voix** ; pour ce défaut, une nouvelle génération risque de redonner la même erreur (**hypothèse** : la synthèse est à peu près constante d'un tirage à l'autre). À décider : traitement de ce cas, par exemple (1) noter le couple mot + voix comme « à ne pas utiliser » (nouveau fichier ou colonne dans `04_DONNEES`) et faire jouer ce mot par l'autre voix ; (2) chercher une autre source (autre voix, enregistrement natif) ; (3) essayer d'abord une nouvelle génération, puis (1) si l'erreur revient | demande de Christophe, 2026-11-01 | `lecteur.js` (`DEFAUTS`), `validation_audios.html`, `valider_audios.py`, `generer_audio_fpt.py`, `generer_lecteur.py`, `04_DONNEES` ; DEC-0065, DEC-0069 ; R-AUD-02 (2 voix par mot) | Moyenne | à décider |
| MOD-D25 | **E1 : audios d'un son enchaînés en une séquence par locuteur** (voyelle seule → syllabes → mots), écoute automatique F puis H | demande de Christophe, 2026-11-02 | `concatener_e1.py` (nouveau), `generer_lecteur.py`, `lecteur.js` | Moyenne | **fait** (2026-11-02) : testé sur une copie ; génération des séquences sur le PC à lancer |
| MOD-D26 | **Objectifs pédagogiques au début de chaque leçon et de chaque exercice.** Proposition de Christophe (2026-11-07), forme validée : (1) en tête de l'écran de la leçon, 2 lignes « À la fin de cette leçon, vous saurez… » **générées** à partir des sons ou tons de la leçon ; (2) pour chaque étape (E1, E2, E3, Combien de fois ?, écrit, E4), une phrase fixe dans un encadré « 🎯 Objectif » repliable, sous le titre (phrases dans `lecteur.js`, pas de nouvelle donnée). À prévoir : DEC si une règle de contenu est fixée ; mise à jour de PROD-AF-LECT § 5 **Fait** (lecteur du 2026-11-07, lot 4, validé) : en tête de leçon, « À la fin de cette leçon, vous saurez reconnaître à l'écoute : <titre>. » ; dans chaque écran d'étape, encadré « 🎯 Objectif » repliable (`<details>`), replié par défaut, avec une phrase fixe par étape. | proposition de Christophe, 2026-11-07 | `lecteur.js`, `lecteur.css` ; PROD-LECT ; PROD-AF-LECT | Moyenne | fait |
| MOD-D27 | **Descriptif de chaque nouveau son et de chaque ton.** Proposition de Christophe (2026-11-07), forme validée : encadré « Comment le dire » sur l'écran E1 de chaque son (ouvert par défaut ; pas en E2–E3), en trois couches : (1) analogie avec le français (colonne `listening_cue` de `reperes_sons.csv`, déjà remplie pour 61 sons sur 76) ; (2) « comment le produire » en 1 ou 2 phrases (colonnes `body_part`, `change`, `check`, vides aujourd'hui) ; (3) schéma articulatoire : **second temps**, simplifié par famille (voyelles : lèvres et hauteur de la langue ; tons : schémas de « Les 6 tons », DEC-0053). Les 76 descriptifs sont rédigés par l'IA dans un CSV à relire, marqués « hypothèse » jusqu'à la relecture par un locuteur du Nord (MOD-E01) ; faits articulatoires et analogies distingués. À faire avant le code : **DEC-0078** (règle de contenu), `generer_lecteur.py`, `00_modele_donnees.md` **Partiel** (lecteur du 2026-11-07, lot 5, validé) : affichage « 🔊 Comment le dire » sur l'écran E1 de chaque son (encadré ouvert par défaut : partie du corps, mouvement, à vérifier, mention « à confirmer par un locuteur du Nord » pour les descriptifs marqués `hypothese`) ; descriptifs des **16 sons de L01** rédigés dans `reperes_sons.csv` (colonnes existantes `body_part`, `change`, `check`, `certainty`) : a, e, ê, i, u, o, ô, t, m, n, l, v, c, p, -m, -n (tous `hypothese`). **Reste** : 46 sons des leçons L02 à L13, DEC-0078 (règle de contenu), schémas articulatoires simplifiés par famille. Les descriptifs restent à relire par un locuteur du Nord (MOD-E01). **Complété pour toute la rédaction** (2026-11-07) : 9 descriptifs ajoutés pour les sons de L02 à L13 (z, aj, uj, wi, f, ɲ, s, wa, wɛ), tous `hypothese`. Les 52 sons de `reperes_sons.csv` ont maintenant un descriptif. **Reste** : DEC-0078 (règle de contenu), schémas articulatoires simplifiés par famille (lot à part), relecture par un locuteur du Nord (MOD-E01). | proposition de Christophe, 2026-11-07 | `04_DONNEES/reperes_sons.csv`, `generer_lecteur.py`, `lecteur.js`, `lecteur.css` ; PROD-LECT ; PROD-AF-LECT | Moyenne (texte), élevée (schémas) | en cours |
| MOD-D15 | **Couper le mode test et le mode essai** par défaut avant d'ouvrir à d'autres apprenants | DEC-0047, DEC-0051 ; CTX-IA § 6 | lecteur | Basse | plus tard |

### E. Contenus et relecture par un locuteur vietnamien

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-E01 | **Trouver un relecteur** vietnamien du Nord pour l'ensemble des points E02 à E06 | QUAL-AVANCEMENT n° 3 | — | **Haute** | à faire |
| MOD-E02 | Relire les **19 phrases** de « Combien de fois ? » | QUAL-AVANCEMENT § 2 | `comptage.csv` | Moyenne | à faire |
| MOD-E03 | Vérifier les **24 classificateurs** « à vérifier » | QUAL-AVANCEMENT § 2 | `mots.csv` | Moyenne | à faire |
| MOD-E04 | Sens des mots de la page des tons ; syllabes inventées *tũ*, *cõ*, *muổi* | DEC-0064 | `reference_tons.csv` | Moyenne | à faire |
| MOD-E05 | Sens des **74 termes hors corpus** réels ; 5 termes trouvés dans un seul dictionnaire (*côm*, *mú*, *nen*, *nuốc*, *pa*) | DEC-0027 ; QUAL-HORS-CORPUS | `paires_minimales.csv` | Moyenne | à faire |
| MOD-E06 | Traductions à relire : *chưng*, *à*, *chi*, *lẽ* ; relecture des 100 mots supports (*tu* douteux) | rapport de reprise des mots § 5 ; PROG-M0 P5 | `mots.csv` | Moyenne | à faire |
| MOD-E07 | Corriger les valeurs **`imageable`** (79 sur 100 estimés) | PROG-M0 § 3 ; CTX-IA § 6 | `mots.csv` | Moyenne | à faire |
| MOD-E08 | **Images définitives** OpenMoji à la place des emoji (`images.csv` vide) | DEC-0024 ; QUAL-AVANCEMENT n° 10 | `images.csv`, lecteur | Moyenne | à faire |
| MOD-E09 | Étymologies manquantes | CTX-IA § 6 | `mots.csv` | Basse | à faire |
| MOD-E10 | **Liste de fréquence de référence** (R-LEX-07), pour A1 | REG-REGLES ; DEC-0035 | `04_DONNEES` | Basse | à décider |

### F. Règles et fondations

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-F01 | Faire valider **REG-DOC** (règles documentaires, brouillon v0.4) | statut du document | `02_REGLES/REGLES_DOCUMENTAIRES.md` | Moyenne | à faire |
| MOD-F02 | Faire valider **REG-REGLES** (registre, brouillon v0.18) | statut du document | `02_REGLES/REGISTRE_REGLES.md` | Moyenne | à faire |
| MOD-F03 | Seuils de FOND-01 venus des archives **sans source** | FOND-01, « À décider » | FOND-01 | Moyenne | à décider |
| MOD-F04 | Mesurer la production en autonomie (lié à MOD-D03) | FOND-04 § 4, « À décider » | FOND-04 | Moyenne | à décider |
| MOD-F05 | Durées du Module 0 : hypothèse à corriger avec les mesures réelles (« Mes progrès ») | PROG-M0, hypothèse ; DEC-0004 | PROG-M0 | Basse | plus tard |
| MOD-F06 | Points « à vérifier » de FOND-02 : ordre de grandeur des combinaisons de syllabes ; transcription de *ông* | FOND-02 | FOND-02 | Basse | à vérifier |
| MOD-F07 | **Règles de code** (SQL, Python, PowerShell) à reprendre de `IA_RULES_STRICT` | REG-DOC ; REG-REGLES | `02_REGLES` | Basse | plus tard |

### G. Outils, enveloppe, Anki

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-G01 | Nettoyer `05_PRODUCTION/tools/` : scripts d'essai et abandonnés (`choisir_appuis.py`, DEC-0061 ; `essai_*.py`) à signaler comme tels ou ranger (sans supprimer) | QUAL-AVANCEMENT § 5 ; règle « ne rien supprimer » | `tools/` | Moyenne | à faire |
| MOD-G02 | **Paquets Anki** par leçon validée | DEC-0015 | `06_LIVRABLES` | Basse | plus tard |
| MOD-G03 | **Enveloppe** WordPress ou Firebase, hébergeur, mise en ligne en https (micro sur téléphone) | DEC-0030 ; PROD-ARCH points 5 et 6 | tout | Basse | plus tard |
| MOD-G04 | **Reconnaissance vocale** en complément (PhoWhisper en test, `tools/test_asr/`) | PROD-ARCH point 2 | E4–E5 | Basse | plus tard |
| MOD-G05 | Hypothèse : les révisions Anki ne remontent pas au site ; contrôle par les statistiques Anki | PROD-ARCH, hypothèse | PROD-ARCH | Basse | à vérifier |
| MOD-G06 | Coût d'Anki sur iPhone (App Store) | PROD-DOSSIER-SUPPORT, « fait à vérifier » | — | Basse | à vérifier |

### H. Pédagogie et programme

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-H01 | **E1 : étudier d'abord 1 ou 2 consonnes initiales**, pour que les mots d'exemple d'une voyelle soient de **simples syllabes consonne + voyelle**, faites seulement de sons déjà vus. Aujourd'hui, les mots d'exemple contiennent des consonnes initiales et finales pas encore étudiées. Constat chiffré (`exemples_e1.csv`, 2026-11-01) : en L01, 10 mots d'exemple de voyelles sur 13 ont une finale (*xem*, *em*, *nên*, *trên*, *lên*, *trong*, *con*, *môn*, *không*, *ông*…) ; *trong*, *không* et *nghe* utilisent tr-, kh-, ngh- et -ng, étudiés seulement en L10. Dans toutes les leçons : 73 mots d'exemple de voyelles, dont 66 avec une consonne initiale et 34 avec une finale. **Contredit l'ordre « voyelles → consonnes → finales » de L01** (DEC-0034, DEC-0037) : une nouvelle décision est nécessaire. À décider : quelles consonnes (de préférence proches du français et déjà dans L01) ; place dans L01 (avant la partie A ou au début de celle-ci) ; règle pour les leçons suivantes (mots d'exemple faits seulement de sons déjà ouverts). À trancher **avant de générer les audios Ultra des autres leçons** (MOD-C01), pour ne pas produire deux fois les mots d'exemple | proposition de Christophe, 2026-11-01 | DEC-0034, DEC-0037, DEC-0039 ; PROG-M0 (ordre de L01) ; FOND-04 ; `exemples_e1.csv`, `choisir_exemples_e1.py`, audios, lecteur | **Haute** | **fait** (2026-11-01, DEC-0072 et DEC-0073 : **t et m**, une brève et une longue, au début de la partie A ; mots t/m + voyelle au ton ngang ; règle de préférence pour L02 à L13). **Mise en œuvre** : 1) mot pour ê : **fait** le 2026-11-01, *mê* et *tê* présents dans les 3 dictionnaires (QUAL-VERIF-HORS-CORPUS § 3 bis) ; les deux retenus (choix de Christophe) ; 2) **fait** le 2026-11-01 : *me* W0340, *mu* W0341, *tô* W0342, *mê* W0343, *tê* W0344 ajoutés à `mots.csv` et `syllabes.csv` (sens à faire relire, MOD-E01). Point ouvert : dans `paires_minimales.csv`, *tô* (L01), *me* (L03) et *mu* (L11) restent sans `word_code` (leurs audios `S-…` existent déjà) ; les relier changerait le nom de leurs audios ; 3) **fait** le 2026-11-01 : `choisir_exemples_e1.py` (niveaux 0 / 1 / 2, consonnes « d'abord »), colonne `e1_first` de `lecons.csv` (`PH-CO-t PH-IN-m` pour L01), `exemples_e1.csv` regénéré (299 mots, 145 différences, dont L01 : t *to, tu, tô* ; m *ma, me, mu* ; e *me* ; ê *mê, tê* ; o *to* ; ô *tô* ; u *tu, mu*) ; lecteur regénéré sans erreur (essai sur une copie) ; 28 audios à créer pour L01 (environ 62 caractères) ; puis **DEC-0073** (syllabes sans sens, réelles d'abord, quand le corpus donne moins de 2 exemples) : `syllabes_e1.csv`, `fabriquer_syllabes_e1.py`, colonnes `syllable` / `invented` d'`exemples_e1.csv`, `generer_lecteur.py`, `generer_audio_fpt.py` ; ajouts L01 : e *te*, o *mo*, ô *mô*, b *be* ; 42 audios à créer pour L01 (environ 90 caractères) ; 4) **fait** le 2026-11-01 : E1 de la partie A dans le lecteur : t puis m en tête (7 sons), avec une ligne d'explication ; m revu en partie B ; `generer_lecteur.py` (liste `e1` de chaque partie, `e1_first`) et `lecteur.js` (`elementsDe`) ; « Combien de fois ? » et verrous inchangés ; essai dans un navigateur sans écran : écrans 1 à 3 justes, aucune erreur JavaScript ; puis, à la demande de Christophe : en **mode test** seulement, le **mot écrit** en tête des infos de la case jouée (toutes les étapes ; en E2–E3 après la réponse, comme les autres infos ; R-ECR-01 inchangé pour l'apprenant) ; tuile d'une syllabe sans sens marquée « syllabe » ; 5) **fait** le 2026-11-01 : 42 audios de L01 générés en deux passages (14 h 40 : 18 lents F1 / H4 ; 14 h 47 : 24 Ultra F4 / H6, 26 caractères par voix), aucune erreur ; écoutés dans le lecteur par Christophe : « très bien » ; non validés (R-AUD-01) ; 6) **fait** le 2026-11-01 : PROG-M0 0.13, PROG-ACT 0.17, PROD-LECT 0.22, PROD-AF-LECT 0.4 (RG-20). **MOD-H01 terminé**, sauf la validation des nouveaux audios (MOD-C03) |
| MOD-H02 | Même question pour les **tons** : plusieurs mots d'exemple de voyelles portent un ton pas encore étudié en L01 (*mẹ*, *bị*, *có*, *là*, *giờ*…, dans L04 à L12). **Vérifié** (2026-11-01) : contrôle systématique des 265 mots d'exemple de L02 à L13 (ton extrait de l'écriture, comparé aux tons déjà ouverts leçon par leçon). **Aucun écart** : les seuls mots au ton « nouveau » sont ceux des leçons de tons elles-mêmes (qui enseignent justement ce ton) ; tous les autres utilisent un ton déjà ouvert à leur leçon | constat du 2026-11-01 (relevé de `exemples_e1.csv`, à confirmer leçon par leçon) | `exemples_e1.csv`, `choisir_exemples_e1.py` | Moyenne | **clos** (2026-11-01, conforme, aucune modification) |
| MOD-H03 | **Séries d'E2 de la partie A de L01** remplacées : S0001 *xem / xêm* → *me / mê* ; S0004 *nên / nen* → *tê / te* ; S0007 *môn / mon / mun* → *mô / mo / mu* (S0012 *ho / hô* inchangée) | DEC-0072, conséquences ; Christophe, 2026-11-01 | `paires_minimales.csv` (S0001, S0004, S0007), DEC-0033, PROG-M0 (L01), audios | Moyenne | **fait** (2026-11-01, DEC-0074 ; aucun audio nouveau, les syllabes avaient déjà leurs audios F4 / H6) |
| MOD-H04 | **Finales -m et -n redécouvertes en L08/L10** : remplacé par un **rappel court** (1 mot, 1 voix, étiquette « déjà vu en L01 », bouton « Écouter » seul) au lieu d'une découverte complète. Les séries (S0061, S0063, S0065, S0074, S0076, S0077) et les suites « Combien de fois ? » ne changent pas (point d'appui utile) | proposition de Christophe, 2026-11-01 ; DEC-0036, DEC-0039, DEC-0046, DEC-0054 | `lecteur.js`, `generer_lecteur.py`, `exemples_e1.csv` ou `lecons.csv` (marquer -m/-n comme rappel) ; PROG-M0 (L08, L10) ; PROD-AF-LECT FP1 | Moyenne | **fait** (2026-11-01, DEC-0075 ; mise en œuvre dans le lecteur à faire) |

---

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-11-01 | Création : journal du 28 au 31 octobre, 69 besoins relevés dans les documents et les données. |
| 0.2 | 2026-11-01 | Thème H (pédagogie et programme) : MOD-H01, consonnes initiales en E1 avant les voyelles (proposition de Christophe) ; MOD-H02, tons des mots d'exemple. |
| 0.3 | 2026-11-01 | MOD-D16 : rendre visible la position de l'apprenant dans la leçon (sons vus, en cours, à venir), proposition de Christophe. |
| 0.4 | 2026-11-01 | MOD-D17 : développer le bloc « Écoute de la leçon » (aujourd'hui un simple état), proposition de Christophe. |
| 0.5 | 2026-11-01 | MOD-D17 : choix de Christophe, bilan d'écoute de fin de leçon et récapitulatif. |
| 0.6 | 2026-11-01 | MOD-D18 à MOD-D23 : améliorations de l'interface du lecteur (guidage, bouton flottant, textes, accueil, écrit, détails), après relecture des écrans. |
| 0.7 | 2026-11-01 | MOD-A03 fait : les MP3 sont suivis par Git (résultat chiffré) ; nouveau besoin MOD-A05 (audios intermédiaires suivis malgré le `.gitignore`) ; journal 2.6. |
| 0.8 | 2026-11-01 | MOD-A01 fait (commit `1d5c57e`) : journal 2.4 à 2.6, section 2.5 vérifiée avec `git status`. |
| 0.9 | 2026-11-01 | MOD-A05 fait : audios intermédiaires gardés dans Git (DEC-0071), `.gitignore` corrigé. |
| 0.10 | 2026-11-01 | MOD-B01 fait : CONTEXTE_IA v1.15. |
| 0.11 | 2026-11-01 | MOD-A04 fait (clé retirée du suivi Git, commit `429419e`) ; MOD-A02 fait (dépôt privé GitHub) ; CONTEXTE_IA v1.16. |
| 0.12 | 2026-11-01 | MOD-B02 à B06 faits ; MOD-B09 en cours ; incident des deux conversations simultanées noté au journal 2.6. |
| 0.13 | 2026-11-01 | MOD-H01 décidé (DEC-0072), mise en œuvre détaillée ; MOD-H02 précisé ; nouveau besoin MOD-H03 (séries d'E2 de la partie A de L01). |
| 0.14 | 2026-11-01 | MOD-H01, étape 1 : *mê* et *tê* vérifiés (3 dictionnaires sur 3). |
| 0.15 | 2026-11-01 | MOD-H01, étape 2 : 5 mots ajoutés au corpus (W0340 à W0344). |
| 0.16 | 2026-11-01 | MOD-H01, étape 3 : script des mots d'exemple, `e1_first`, `exemples_e1.csv`. |
| 0.17 | 2026-11-01 | DEC-0073 : syllabes sans sens en E1 (te, mo, mô, be). |
| 0.18 | 2026-11-01 | MOD-H04 : finales -m et -n reprises en L08 et L10, doublons d'exercices à examiner (proposition de Christophe) ; MOD-D24 (case « mot mal prononcé par ce locuteur ») réintégré, perdu une deuxième fois lors d'une écriture parallèle ; totaux recomptés. |
| 0.19 | 2026-11-01 | MOD-H01, étape 4 : t et m en tête de l'E1 de la partie A dans le lecteur. |
| 0.20 | 2026-11-01 | Mode test : mot écrit dans les infos du son ; tuile « syllabe » (MOD-H01, étape 4). |
| 0.21 | 2026-11-01 | Lignes 0.19 et 0.20 rétablies (effacées par l'écriture parallèle de 14 h 30, qui a gardé MOD-D24) ; MOD-H01, étape 5 : 42 audios de L01 ; MOD-C02 : tarifs constatés. |
| 0.22 | 2026-11-01 | MOD-H01 fait (étape 6 : PROG-M0, PROG-ACT, PROD-LECT, PROD-AF-LECT). |
| 0.23 | 2026-11-01 | MOD-B13 fait : CONTEXTE_IA v1.17 ; résumé corrigé ; totaux recomptés (84 besoins). |
| 0.24 | 2026-11-01 | MOD-H03 fait (DEC-0074) : séries S0001, S0004, S0007 de L01 remplacées par t/m + voyelle. |
| 0.25 | 2026-11-01 | MOD-H02 clos (vérifié, conforme) ; MOD-H04 décidé et fait (DEC-0075, rappel court -m/-n en L08/L10). |
| 0.26 | 2026-11-01 | MOD-H04 : mise en œuvre dans le lecteur (e1_rappel, generer_lecteur.py, lecteur.js) ; test navigateur à faire. MOD-C16 ajouté ; totaux : 85 besoins. |
| 0.27 | 2026-11-01 | MOD-C16 corrigé (le défaut est la synthèse système, pas les voix F4 / H6) ; MOD-C17 ajouté (audit approfondi des locuteurs) ; totaux : 86 besoins. |
| 0.28 | 2026-11-02 | DEC-0077 (stratégie A, multi-voix par usage) : MOD-C17 fait, MOD-C05 fait, MOD-C06 plus pertinent ; MOD-C01 et MOD-D01 impactés (plan à revoir). |
| 0.29 | 2026-11-02 | MOD-C01 : plan DEC-0077 refait pour L02 à L13 (985 fichiers, 13 016 caractères, environ 6 200 ₫) ; `voix.csv` et `generer_audio_fpt.py` mis à jour ; section 2.7 ajoutée. |
| 0.30 | 2026-11-02 | MOD-D01 fait : lecteur adapté à DEC-0077 (`generer_lecteur.py`, `lecteur.js`), testé sur une copie ; journal 2.7. |
| 0.31 | 2026-11-02 | MOD-D25 fait : séquences d'écoute de l'E1 (`concatener_e1.py`, `generer_lecteur.py`, `lecteur.js`), testé sur une copie ; journal 2.7. |
| 0.32 | 2026-11-07 | MOD-D19 et MOD-D20 faits (lot 1 de l'interface du lecteur : bouton Signaler dans la barre du haut, textes et barre du verrou, anomalie d'E3) ; testés sur une copie, captures avant/après, aucune erreur JavaScript. |
| 0.33 | 2026-11-07 | MOD-D18 en cours (lot 2 fait et validé : frise et étape en cours sur l'écran de la leçon), MOD-D16 partiel ; nouveaux besoins MOD-D26 (objectifs pédagogiques) et MOD-D27 (descriptif de chaque son et ton), formes validées par Christophe ; plan en lots : accueil, objectifs, descriptif en texte. |
| 0.34 | 2026-11-07 | MOD-D21 fait et MOD-D18 complété (lot 3 validé : avancement de chaque leçon, avancement global, bouton « Continuer » sur l'accueil). |
| 0.35 | 2026-11-07 | MOD-D26 fait (lot 4 validé : objectif en tête de leçon, encadré repliable par étape). |
| 0.36 | 2026-11-07 | MOD-D27 partiel (lot 5 validé : affichage « Comment le dire » en E1 + 16 descriptifs pour les sons de L01 dans `reperes_sons.csv`). |
| 0.37 | 2026-11-07 | MOD-D16, MOD-D22, MOD-D23 (partiel) faits (lots 6, 7, 8 validés) ; MOD-D27 : 9 derniers descriptifs rédigés dans `reperes_sons.csv` (sons de L02 à L13). |
| 0.38 | 2026-11-07 | DEC-0078 rédigée (règle de contenu des descriptifs de sons) ; MOD-D23 fait (129 emojis ajoutés dans `images_provisoires.csv`). |

## Liens

- **Entrées** : [REG-DOC](../02_REGLES/REGLES_DOCUMENTAIRES.md),
  [REG-DEC](../02_REGLES/DECISIONS.md), [CTX-IA](../CONTEXTE_IA.md),
  [QUAL-AVANCEMENT-20261031](etat_avancement_2026-10-31.md)
- **Sorties** : aucune
