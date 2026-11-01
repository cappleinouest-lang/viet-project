---
id: QUAL-SUIVI-MODIF
titre: Suivi des modifications du projet
statut: BROUILLON
version: 0.7
date: 2026-11-01
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

- **Ce qui a été fait** : 70 décisions (DEC-0001 à DEC-0070) et 33 commits Git
  entre le 28 et le 31 octobre 2026. **Tout ce qui a été fait après le
  31/10 à 15 h 15 n'est pas encore enregistré dans Git** (DEC-0067 à
  DEC-0070, voix FPT.TTS-ultra, signalement des sons, voyelle seule en E1).
- **Ce qui reste à faire** : **80 besoins** relevés (section 3), dont
  **17 de priorité haute**. Le plus urgent : enregistrer dans Git, puis
  mettre les documents d'accord avec DEC-0067 (plusieurs documents décrivent
  encore les anciennes voix F1, F3, H3, H4).

| Thème | Nombre | Haute | Moyenne | Basse |
|---|---|---|---|---|
| A. Git et sauvegarde | 5 | 3 | 2 | 0 |
| B. Cohérence des documents après DEC-0067 | 12 | 7 | 5 | 0 |
| C. Audios et voix | 15 | 4 | 7 | 4 |
| D. Lecteur d'activités | 23 | 1 | 15 | 7 |
| E. Contenus et relecture par un locuteur | 10 | 1 | 7 | 2 |
| F. Règles et fondations | 7 | 0 | 4 | 3 |
| G. Outils, enveloppe, Anki | 6 | 0 | 1 | 5 |
| H. Pédagogie et programme | 2 | 1 | 1 | 0 |
| **Total** | **80** | **17** | **42** | **21** |

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

### 2.4 Vendredi 31 octobre 2026 (2 commits + travail non enregistré)

| Heure | Commit | Modification |
|---|---|---|
| 13 h 40 | `0fab1ab` | État d'avancement au 31/10 (QUAL-AVANCEMENT-20261031) |
| 15 h 15 | `5002119` | Thu Minh écartée, Ban Mai pour les leçons de sons (DEC-0066) ; probablement aussi l'outil de validation des audios (DEC-0065, non cité dans le message) ; CONTEXTE_IA 1.14 |
| 15 h 17 – 23 h 36 | **aucun** | **Non enregistré dans Git** : voir 2.5 |

### 2.5 Modifications non enregistrées dans Git (au 2026-11-01)

| Fichier | Modification |
|---|---|
| `02_REGLES/DECISIONS.md` (v1.61 à 1.64) | **DEC-0067** voix FPT.TTS-ultra F4 Ban Mai et H6 Quang Anh, débit lent emprunté à F1 et H4, mots espacés par virgules ; **DEC-0068** silence de début gardé brut, fin complétée à 0,35 s ; **DEC-0069** bouton « ⚑ Signaler un son » ; **DEC-0070** voyelle seule avant les mots en E1 |
| `04_DONNEES/voix.csv` | F4 et H6 actives ; F1, H3, H4 inactives ; colonne `slow_from` |
| `04_DONNEES/exemples_e1.csv`, `audios.csv`, `courbes_modele.csv` | voix F4 / H6 ; nouveaux audios ; courbes du modèle |
| `04_DONNEES/00_modele_donnees.md` | colonne `slow_from` (en-tête non mis à jour : voir MOD-B06) |
| `05_PRODUCTION/03_audio.md` (v0.14 à 0.17) | § 1 bis voix actuelles ; signalement ; voyelle seule |
| `05_PRODUCTION/lecteur/lecteur.js`, `lecteur.css` | signalement d'un son (DEC-0069), voyelle seule (DEC-0070) |
| `05_PRODUCTION/tools/` | `generer_audio_fpt.py`, `generer_lecteur.py`, `valider_audios.py`, `courbes_modele.py`, `decoupe_audio.py`, `choisir_exemples_e1.py` modifiés ; `essai_ultra.py`, `essai_espacement.py`, `essai_voyelles.py`, `validation_audios.html` nouveaux (à confirmer avec `git status`) |
| `07_QUALITE/` | `essai_tts_ultra_2026-10-31.md` (v1.0 à 1.5), `audios_a_refaire.csv` (170 lignes), `validations/validations_audios_2026-10-31_1527.csv` |
| `04_DONNEES/audio/` | au moins 592 fichiers créés après 15 h 15 : F1 (« Combien de fois ? », DEC-0066) pour L01, L04, L05, L06, L08, L09 ; **F4 et H6 pour L01** (essai de DEC-0067). Liste partielle : le relevé s'arrête à 2 000 fichiers |

### 2.6 Dimanche 1er novembre 2026

| Besoin | Résultat |
|---|---|
| MOD-A03 | Vérifié : 6 784 MP3 suivis par Git (88 Mo), dont 2 296 dans des dossiers que le `.gitignore` devrait exclure ; dépôt compatible avec GitHub. Suite : MOD-A05 |

---

## 3. Besoins de modification futurs

### A. Git et sauvegarde

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-A01 | **Enregistrer dans Git** tout le travail du 31/10 après 15 h 15 (section 2.5) | constat du 2026-11-01 | tout le projet | **Haute** | à faire |
| MOD-A02 | **Sauvegarde hors du PC** : dépôt privé GitHub (l'historique n'existe que sur le PC) | QUAL-AVANCEMENT § 7 n° 2 ; risque « perte totale » | Git | **Haute** | à faire |
| MOD-A03 | Vérifier si les **milliers de MP3** de `04_DONNEES/audio/` sont suivis par Git (le `.gitignore` n'exclut que `_bruts`, `_essais`, `_anciens`) : poids du dépôt, limite de GitHub. **Résultat (lecture de `.git/index`, 2026-11-01)** : hypothèse **confirmée**. Sur 6 860 fichiers suivis, **6 784 sont des MP3** (88 Mo sur 89 Mo) : 4 486 à la racine de `audio/` (46,6 Mo), **mais aussi 2 232 dans `_bruts` (40,5 Mo), 45 dans `_essais` et 19 dans `_anciens`** : ces fichiers ont été ajoutés à Git avant la règle du `.gitignore`, qui ne retire jamais un fichier déjà suivi (voir MOD-A05). Le dossier `audio/Nouveau dossier` (2 MP3) est encore suivi mais n'existe plus sur le disque : sa suppression sera enregistrée avec MOD-A01. Dépôt compressé (`.git/objects/pack`) : 88 Mo. Plus gros fichier suivi : `audios.csv`, 0,4 Mo. **Compatible avec GitHub** (limite stricte de 100 Mo par fichier ; dépôt conseillé sous 1 Go, à revérifier dans la documentation de GitHub). Point de vigilance : chaque génération d'audios ajoute son poids à l'historique, même si les fichiers sont ensuite supprimés. Non compté : les MP3 créés après le dernier commit (MOD-A01) | constat du 2026-11-01 | `.gitignore`, MOD-A02, MOD-A05 | **Haute** | **fait** (2026-11-01) |
| MOD-A04 | Fichier vide `cle api FPT.txt` à la racine : la clé doit rester **hors** du projet (DOC-04). Il est ignoré par Git, mais à déplacer ou laisser vide | constat du 2026-11-01 | DOC-04 | Moyenne | à vérifier |
| MOD-A05 | **Retirer de Git les audios intermédiaires** déjà suivis malgré le `.gitignore` (`_bruts`, `_essais`, `_anciens` : 2 296 MP3, 41 Mo), avec `git rm -r --cached` (retire les fichiers de Git **sans les effacer du disque**). Ils restent dans l'historique déjà enregistré : le dépôt ne maigrit pas, mais les prochains commits ne les suivent plus. À décider : retirer (cohérent avec la règle DOC-19) ou garder suivis (et alors corriger le `.gitignore`). À faire **avant** MOD-A01 et MOD-A02 | MOD-A03, 2026-11-01 | `.gitignore`, DOC-19, MOD-A01, MOD-A02 | Moyenne | à décider |

### B. Cohérence des documents après DEC-0067

> **Fait** : DEC-0067 remplace les voix F1, F3, H3, H4 par **F4 Ban Mai** et
> **H6 Quang Anh** (FPT.TTS-ultra) pour toutes les écoutes, E1, la page des
> tons et le modèle d'E4. Les documents ci-dessous disent encore autre chose.

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-B01 | **CONTEXTE_IA** v1.15 : § 4 « Audio » (dit encore F1 + H4 pour les sons, F1/H3/H4 pour les tons, modèle F1), § 5 état (daté du 30/10, lecteur 0.13 au lieu de 0.21, 4 491 audios), § 6 points ouverts, nombre de décisions (DEC-0070) | constat du 2026-11-01 | CTX-IA | **Haute** | à faire |
| MOD-B02 | **PROD-AUDIO** : titre « FPT.TTS-pro » périmé ; § 1 tableau des voix et totaux du 29/10 ; historique (ligne 0.10 mal placée) ; champs `entrees` et `sorties` vides (DOC-30) | constat du 2026-11-01 | `05_PRODUCTION/03_audio.md` | **Haute** | à faire |
| MOD-B03 | **PROD-LECT** : § 4 « voix F1, H3, H4 simulées » ; § 5 « modèle F1 » ; version 0.20 du 30/10 sans DEC-0065 à DEC-0070 | constat du 2026-11-01 | `05_PRODUCTION/02_lecteur_activites.md` | **Haute** | à faire |
| MOD-B04 | **PROD-AF-LECT** (analyse fonctionnelle, état du 29/10) : voix F1 dans les règles RG-11, § 6 ; exemples `W0057-H3`, Le Minh ; ajouter signalement (DEC-0069), voyelle seule (DEC-0070), « Combien de fois ? », E4, page des tons | constat du 2026-11-01 | `05_PRODUCTION/04_analyse_fonctionnelle_lecteur.md` | **Haute** | à faire |
| MOD-B05 | **PROG-M0** § 3 : « 3 voix actives (F1, H3, H4) », « 2 238 audios » ; **PROG-ACT** ligne 47 : « une seule voix (F1) » | constat du 2026-11-01 | `03_PROGRAMME/` | **Haute** | à faire |
| MOD-B06 | **DATA-MODELE** : en-tête (v0.19, date du 30/10) non mis à jour alors que `slow_from` a été ajouté ; exemples F1 / H3 dans `voice_f` / `voice_h` | constat du 2026-11-01 | `04_DONNEES/00_modele_donnees.md` | **Haute** | à faire |
| MOD-B07 | **REG-REGLES** R-AUD-02 (« au moins 2 voix », variété) : depuis DEC-0067, une seule femme et un seul homme, et le personnage d'homme change entre lent (Huy Phong) et normal (Quang Anh). Vérifier la conformité, ou noter l'écart | DEC-0066, DEC-0067 | `02_REGLES/REGISTRE_REGLES.md` | **Haute** | à décider |
| MOD-B08 | **Regénérer** `CARTE_DOCUMENTAIRE.md` (datée du 29/10) avec `build_doc_map.py` | QUAL-AVANCEMENT § 7 n° 15 | carte | Moyenne | à faire |
| MOD-B09 | Rendre les **liens réciproques** (DOC-32) : CTX-IA, PROD-AUDIO, PROD-LECT, REG-DEC et QUAL-CONTRASTE-TONS ne citent pas en `sorties` les rapports QUAL-AVANCEMENT, QUAL-CONTRASTE-TONS, QUAL-ESSAI-ULTRA ; et ce document (QUAL-SUIVI-MODIF) | essai de `build_doc_map.py` du 2026-11-01 | en-têtes | Moyenne | à faire |
| MOD-B10 | Relier ou classer les 2 documents **sans aucun lien** : PROD-COMP-SUPPORT-20261028, PROD-DOSSIER-SUPPORT-20261028 | carte documentaire | `05_PRODUCTION/` | Moyenne | à faire |
| MOD-B11 | **PROD-ARCH** (v0.4) : rédigé autour de WordPress (extension de progression, Local, hébergeur) alors que DEC-0030 laisse le choix WordPress ou Firebase ; point ouvert 3 « voix de référence » à mettre à jour (DEC-0067) | constat du 2026-11-01 | `05_PRODUCTION/01_architecture_outils.md` | Moyenne | à faire |
| MOD-B12 | `README.md` de la racine et des dossiers : brouillons v0.1–0.2 du 28/10, à relire | constat du 2026-11-01 | `README.md` | Moyenne | à faire |

### C. Audios et voix

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-C01 | **Écouter L01 en F4 / H6 dans le lecteur**, puis générer les autres leçons (environ 1 700 fichiers, 19 000 caractères) | DEC-0067 « Mise en œuvre » | audios | **Haute** | en cours (L01 générée) |
| MOD-C02 | **Vérifier le tarif de FPT.TTS-ultra** avant la génération complète | PROD-AUDIO § 1 bis | coût | **Haute** | à vérifier |
| MOD-C03 | **Valider les audios** à l'écoute (R-AUD-01) ; sans cela le lecteur reste en mode d'essai. Le nombre à écouter (3 664 au plan du 31/10) change avec DEC-0067 : à recompter | QUAL-AVANCEMENT § 7 n° 1 ; DEC-0065 | `audios.csv` | **Haute** | à faire |
| MOD-C04 | **Trier `audios_a_refaire.csv`** : sur 170 refus, **138** concernent des voix devenues inactives au débit concerné (F3 : 95 ; F1 normal : 22 ; H4 normal : 13 ; H3 : 8). Seuls **32 restent utiles** : les lents de H4 (25) et de F1 (7), empruntés par H6 et F4. Ne pas tout regénérer (coût inutile) | calcul du 2026-11-01 sur le fichier | `07_QUALITE/audios_a_refaire.csv`, `generer_audio_fpt.py --liste` | **Haute** | à faire |
| MOD-C05 | **Contraste des tons plus faible en Ultra** (2,3 contre environ 4 pour F1 et H4) alors que F4 et H6 servent aussi aux leçons de tons : réévaluer le choix des voix des leçons de tons (le « locuteur le plus adapté » reste à choisir) | QUAL-ESSAI-ULTRA ; DEC-0067 | voix des tons | Moyenne | à décider |
| MOD-C06 | **Voix d'homme différente** entre lent (Huy Phong) et normal (Quang Anh) : vérifier que cela ne gêne pas | DEC-0067 point 2 | `voix.csv` | Moyenne | à vérifier |
| MOD-C07 | **Phrases lentes** à 0,75 : jugées bonnes, non appliquées (coût) ; à revoir | DEC-0067 point 7 | `comptage.csv`, audios | Moyenne | à décider |
| MOD-C08 | Silence de début des fichiers Ultra (plus de 200 ms) gardé brut : le raccourcir (`ROGNER_ULTRA = True`) s'il gêne à l'usage | DEC-0068 | `generer_audio_fpt.py` | Moyenne | à vérifier |
| MOD-C09 | **Deuxième voix de femme du Nord** (autre fournisseur ou enregistrement natif) | DEC-0066 « Conséquence » ; CTX-IA § 6 | `voix.csv` | Moyenne | à faire |
| MOD-C10 | **Enregistrement natif** au moins pour la page des tons et le modèle d'E4 (la synthèse FPT rend mal *hỏi* et *nặng*) | QUAL-AVANCEMENT, risques ; QUAL-CONTRASTE-TONS | audios | Moyenne | à décider |
| MOD-C11 | Huy Phong (H4) : son « numérique » par moments ; mots concernés et origine (synthèse ou traitement) à préciser. Concerne toujours le débit lent de H6 | QUAL-ESSAI-ULTRA | H4 lent | Moyenne | à vérifier |
| MOD-C12 | Diphtongues et triphtongues **seules** en E1 : à essayer d'abord | DEC-0070 point 2 | `essai_voyelles.py` | Basse | à faire |
| MOD-C13 | **Voix d'enfant** : source à trouver | DEC-0023 ; `voix.csv` (E1 `planned`) | `voix.csv` | Basse | à faire |
| MOD-C14 | Audios lents des mots qui ne servent qu'en leçons de tons : générés mais jamais joués (coût inutile, faible) | PROD-AF-LECT EC-03 | plan de génération | Basse | à faire |
| MOD-C15 | Réévaluer FPT.TTS-ultra plus tard pour les **phrases et dialogues** (A1–A2) | QUAL-ESSAI-ULTRA, résumé | audios A1 | Basse | plus tard |

### D. Lecteur d'activités

| N° | Besoin | Origine | Touche | Priorité | État |
|---|---|---|---|---|---|
| MOD-D01 | Regénérer le lecteur avec F4 / H6 et vérifier la page des tons, E1 (voyelle seule) et E4 (courbes F4) | DEC-0067, DEC-0070 | `generer_lecteur.py`, `courbes_modele.py` | **Haute** | à vérifier |
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
| MOD-D16 | **Rendre visible la position de l'apprenant dans la leçon.** À tout moment, l'apprenant doit voir où il en est : quels sons (ou tons) de la leçon il a **déjà étudiés**, lequel il **étudie en ce moment**, et lesquels **restent à étudier**. Exemple en L01, E1 : une frise des sons de la leçon (symbole ou lettres de chaque son), avec un état visible pour chacun (vu / en cours / à venir), et la partie A ou B. Même principe à étendre aux autres étapes (E2–E3 : séries réussies / à travailler ; E4) et à la leçon entière (étapes faites / ouvertes / fermées). **Fait** (lecteur 0.21) : l'écran E1 n'affiche qu'un compteur « Son 3 sur 12 », sans la liste des sons vus et à venir. À décider : contenu exact de la frise, possibilité de toucher un son déjà vu pour y revenir | proposition de Christophe, 2026-11-01 | `lecteur.js`, `lecteur.css` ; PROD-LECT ; PROD-AF-LECT (écrans) | Moyenne | à décider |
| MOD-D17 | **Développer le bloc « Écoute de la leçon »** (écran de la leçon, après « Fin d'E3 · L'écrit »). **Fait** (lecteur 0.21) : ce n'est pas une activité, seulement un **état** sans bouton : « Pas encore validée » ou « Validée le … », avec la phrase « Valider l'écoute ouvre la leçon suivante ». La validation se fait en réalité par le bouton « Valider l'écoute de la leçon » de l'écran de l'écrit, sans contrôle supplémentaire. **Choix de Christophe (2026-11-01) : les deux.** (1) Un **bilan d'écoute de fin de leçon** : toutes les séries de la leçon mêlées, débit normal, plusieurs voix, avec un seuil ; il couvrirait R-VOL-07 et MOD-D06 (pas de confusion majeure avec la leçon précédente). (2) Un **récapitulatif** : sons étudiés, scores par série, confusions fréquentes (lien avec MOD-D16 et « Mes progrès »). Restent à décider avant d'écrire la décision DEC : nombre de questions et seuil du bilan, part d'items de la leçon précédente, ordre (bilan puis récapitulatif), et si la validation de l'écoute passe désormais par le bilan plutôt que par l'écran de l'écrit | proposition de Christophe, 2026-11-01 | `lecteur.js` (écran de la leçon, `ecranEcrit`) ; R-VOL-07 ; PROD-LECT ; PROD-AF-LECT | Moyenne | à décider (contenu choisi, paramètres à fixer) |
| MOD-D18 | **Guider vers la prochaine étape.** Constat (lecteur du 31/10, téléphone) : l'écran de L01 aligne 12 cartes semblables, toutes avec le même bouton vert (environ 3,5 hauteurs d'écran), sans indication de l'étape à faire. Proposition : bouton « Continuer : L01 · E2 Distinguer » sur l'accueil ; une seule étape mise en avant dans la leçon ; étapes d'une partie en frise compacte (E1 → E2 → E3 → Combien → Écrit) avec leur état. Lié à MOD-D16 | relecture de l'interface, 2026-11-01 ; accord de Christophe | `lecteur.js` (accueil, écran de la leçon), `lecteur.css` | Moyenne | à faire |
| MOD-D19 | **Le bouton flottant « ⚑ Signaler un son » masque du contenu** : une tuile de mot en E1, la courbe en E4, un réglage, une case de l'écrit. Le placer dans la barre du haut, ou réserver une marge en bas de page | relecture de l'interface, 2026-11-01 | `lecteur.css`, `lecteur.js` | Moyenne | à faire |
| MOD-D20 | **Textes plus clairs.** « 0 justes sur les 0 dernières » et « — séries réussies 2 fois » sont peu compréhensibles ; remplacer par « Pas encore commencé » et une seule barre vers le verrou (« Encore 6 bonnes réponses pour valider ») au lieu des trois cases de chiffres. À vérifier : E3 affiche « Continuer » sans aucune réponse donnée (anomalie possible) | relecture de l'interface, 2026-11-01 | `lecteur.js` | Moyenne | à faire |
| MOD-D21 | **Accueil avec l'avancement réel** : pour chaque leçon, « en cours, 40 % » ou « validée le … » ; en tête, avancement global écoute et production (rend visible R-VOL-04) ; date de la dernière séance. Aujourd'hui, seulement « Ouverte » | relecture de l'interface, 2026-11-01 | `lecteur.js` (accueil) | Moyenne | à faire |
| MOD-D22 | **Écran de l'écrit** : grouper les termes par série (un cadre par série) ; réduire la place des cases « syllabe inventée (jamais écrite) » (3 sur 13 en L01, partie A) | relecture de l'interface, 2026-11-01 | `lecteur.js` (`ecranEcrit`), `lecteur.css` | Basse | à faire |
| MOD-D23 | **Détails** : en E1, une tuile de mot sans image (🔊 seul) ; « Mes progrès » vide avant E2 (y montrer les sons d'E1 découverts, lien MOD-D11) ; sur PC, écran de la leçon sur deux colonnes (secondaire, le téléphone passe d'abord) | relecture de l'interface, 2026-11-01 | `lecteur.js`, `images_provisoires.csv` | Basse | à faire |
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
| MOD-H01 | **E1 : étudier d'abord 1 ou 2 consonnes initiales**, pour que les mots d'exemple d'une voyelle soient de **simples syllabes consonne + voyelle**, faites seulement de sons déjà vus. Aujourd'hui, les mots d'exemple contiennent des consonnes initiales et finales pas encore étudiées. Constat chiffré (`exemples_e1.csv`, 2026-11-01) : en L01, 10 mots d'exemple de voyelles sur 13 ont une finale (*xem*, *em*, *nên*, *trên*, *lên*, *trong*, *con*, *môn*, *không*, *ông*…) ; *trong*, *không* et *nghe* utilisent tr-, kh-, ngh- et -ng, étudiés seulement en L10. Dans toutes les leçons : 73 mots d'exemple de voyelles, dont 66 avec une consonne initiale et 34 avec une finale. **Contredit l'ordre « voyelles → consonnes → finales » de L01** (DEC-0034, DEC-0037) : une nouvelle décision est nécessaire. À décider : quelles consonnes (de préférence proches du français et déjà dans L01) ; place dans L01 (avant la partie A ou au début de celle-ci) ; règle pour les leçons suivantes (mots d'exemple faits seulement de sons déjà ouverts). À trancher **avant de générer les audios Ultra des autres leçons** (MOD-C01), pour ne pas produire deux fois les mots d'exemple | proposition de Christophe, 2026-11-01 | DEC-0034, DEC-0037, DEC-0039 ; PROG-M0 (ordre de L01) ; FOND-04 ; `exemples_e1.csv`, `choisir_exemples_e1.py`, audios, lecteur | **Haute** | à décider |
| MOD-H02 | Même question pour les **tons** : plusieurs mots d'exemple de voyelles portent un ton pas encore étudié en L01 (*mẹ*, *bị*, *có*, *là*, *giờ*…, dans L04 à L12). À examiner avec MOD-H01 : faut-il des mots d'exemple au ton ngang seulement, tant que les autres tons ne sont pas ouverts ? | constat du 2026-11-01 (relevé de `exemples_e1.csv`, à confirmer leçon par leçon) | `exemples_e1.csv`, `choisir_exemples_e1.py` | Moyenne | à vérifier |

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

## Liens

- **Entrées** : [REG-DOC](../02_REGLES/REGLES_DOCUMENTAIRES.md),
  [REG-DEC](../02_REGLES/DECISIONS.md), [CTX-IA](../CONTEXTE_IA.md),
  [QUAL-AVANCEMENT-20261031](etat_avancement_2026-10-31.md)
- **Sorties** : aucune
