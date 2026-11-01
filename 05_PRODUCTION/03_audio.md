---
id: PROD-AUDIO
titre: Génération des audios avec FPT AI Marketplace (FPT.TTS-ultra, FPT.TTS-pro, FPT.AI-VITs)
statut: BROUILLON
version: 0.18
date: 2026-11-01
resume: >
  Explique comment générer, avec FPT.AI, les audios du Module 0 décrits par
  04_DONNEES : ce qui est produit, où va la clé d'accès, les commandes, la
  reprise après interruption et la validation par l'écoute.
entrees: [REG-DEC, REG-REGLES, DATA-MODELE]
sorties: [PROD-LECT, QUAL-CONTRASTE-TONS-20261030, QUAL-ESSAI-ULTRA-20261031, QUAL-AVANCEMENT-20261031]
sources:
  - 02_REGLES/DECISIONS.md (DEC-0023, DEC-0040, DEC-0065 à DEC-0070)
  - 04_DONNEES/audios.csv et voix.csv (comptage du 2026-11-01)
  - 02_REGLES/REGISTRE_REGLES.md (R-AUD-01 à R-AUD-06)
  - _ARCHIVES/Projet de Formation_Vietnamien_A0_to_A2/PROD/00_GLOBAL/01_DB/02_SCRIPTS/04_POPULATION/EXP_generate_audio_fptai_v01.py (appel de l'API, réglages de vitesse)
  - marketplace.fptcloud.com, Voice Studio, bouton View Code (relevé le 2026-10-29)
  - https://factory.fpt.ai/pricing?service=serverless-inference (consulté le 2026-10-29)
---

# Génération des audios avec FPT AI Marketplace (FPT.TTS-ultra, FPT.TTS-pro, FPT.AI-VITs)

## Résumé

Le script `05_PRODUCTION/tools/generer_audio_fpt.py` lit `04_DONNEES` et
demande à FPT (FPT.TTS-ultra, FPT.TTS-pro ou FPT.AI-VITs selon la voix)
chaque audio manquant
(`POST https://mkp-api.fptcloud.com/v1/audio/speech`, format proche d'OpenAI). Les fichiers vont dans
`04_DONNEES/audio/` et sont inscrits dans `audios.csv` avec
`validated = false`. Le lecteur ne les utilise qu'une fois **écoutés et
validés** (R-AUD-01), sauf en mode d'essai (`--non-valides`).

Depuis DEC-0067, **deux voix seulement** servent : **F4 Ban Mai** et
**H6 Quang Anh**, en FPT.TTS-ultra, au débit normal ; leur débit lent est
emprunté aux anciennes voix F1 et H4 (§ 1 bis).

## 1. Ce qui est généré

### 1.1 Plan actuel (DEC-0067)

| Volet | Contenu | Voix | Débits |
|---|---|---|---|
| Écoute (E1–E3), leçons de sons **et** de tons | termes des séries minimales, syllabes hors corpus et inventées, suites et phrases de « Combien de fois ? » | **F4** (femme) et **H6** (homme) | normal (Ultra) ; lent emprunté à F1 / H4 ; mots espacés (phrases) |
| Découverte (E1) | mots d'exemple de `exemples_e1.csv` (DEC-0039) ; voyelle seule (DEC-0070) | F4 et H6 | normal et lent ; voyelle seule : normal seulement |
| Page « Les 6 tons » | syllabes de `reference_tons.csv` | F4 et H6 | normal |
| Production (E4–E5) | mots supports ; classificateur + nom | **F4** (voix modèle, R-AUD-03) | lent (F1), normal |

> **Fait** (`audios.csv`, 2026-11-01) : F4 et H6 n'ont été générés que pour
> **L01** (essai demandé par DEC-0067, « Mise en œuvre ») : **227 fichiers**,
> aucun validé. Les autres leçons restent à générer après écoute de L01
> (environ 1 700 fichiers, 19 000 caractères).

### 1.2 Fichiers présents (`audios.csv`, 2026-11-01)

| Type (`item_type`) | F1 | F3 | H3 | H4 | **F4** | **H6** | H1, H2 | Total |
|---|---|---|---|---|---|---|---|---|
| mots (`word`) | 350 | 336 | 298 | 336 | 31 | 30 | 4 | 1 385 |
| syllabes hors corpus (`syllable`) | 280 | 200 | 280 | 200 | 9 | 9 | 0 | 978 |
| syllabes inventées (`invented`) | 70 | 70 | 70 | 70 | 4 | 4 | 1 | 289 |
| suites et phrases (`sequence`) | 898 | 826 | 82 | 908 | 65 | 65 | 0 | 2 844 |
| voyelle seule (`voyelle`) | 0 | 0 | 0 | 0 | 5 | 5 | 0 | 10 |
| **Total** | 1 598 | 1 432 | 730 | 1 514 | **114** | **113** | 5 | **5 506** |

Débits : normal 2 938, lent 2 499, mots espacés 69. **3 494 audios sont
validés**, tous des anciennes voix (F1, F3, H3, H4). F3, H3 et les essais
H1, H2 ne servent plus ; leurs fichiers sont gardés (on ne supprime rien).
F1 et H4 ne servent plus qu'au **débit lent** de F4 et H6.

Voyelle seule : DEC-0070 prévoit 22 fichiers (11 voyelles × 2 voix) ;
10 sont présents (hypothèse : les 5 voyelles de L01, à vérifier).

### 1.3 Débits lents des anciennes voix

Débit lent choisi à l'écoute le 2026-10-29 (essais à 0,7, 0,6, 0,5) :
F1 = 0,7 ; H3, H4 = 0,6 ; F3 = 0,8 depuis DEC-0059 (colonne
`provider_speed_slow` de `voix.csv`). FPT.TTS-ultra n'a pas de débit lent
(§ 1 bis). Le débit rapide (E5) sera ajouté avec le volet production.

> **Fait** : la page de tarifs indique 16,50 $ par million de caractères
> pour FPT.TTS-pro comme pour FPT.AI-VITs (2026-10-29), soit moins de
> 0,10 $ pour le plan du 29/10. Tarif de **FPT.TTS-ultra : non vérifié**
> (§ 1 bis). Service payant (portefeuille prépayé) ; erreur
> 402 = solde à zéro. Le script s'arrête de lui-même sur une erreur de clé
> (401) ou de solde (402), ou après 5 erreurs sans succès, et reprend là où
> il s'est arrêté.

## 1 bis. Voix actuelles (DEC-0067, 2026-10-31)

| Code | Voix | Débit normal et mots espacés | Débit lent (colonne `slow_from`) |
|---|---|---|---|
| F4 | Ban Mai (femme, voix modèle) | `std_banmai`, **FPT.TTS-ultra** | fichiers de **F1** (`std_banmai`, FPT.TTS-pro, 0,7) |
| H6 | Quang Anh (homme) | `std_quanganh`, **FPT.TTS-ultra** | fichiers de **H4** (`std_huyphong`, FPT.AI-VITs, 0,6) |

- FPT.TTS-ultra **ignore la vitesse** : le script ne lui demande jamais de
  débit lent ; le plan prévoit à la place `<référence>-F1-slow.mp3` ou
  `<référence>-H4-slow.mp3` (générés avec F1 ou H4 s'ils manquent), et le
  lecteur les joue pour F4 ou H6.
- Le texte est envoyé dans les champs `input` et `text` (exemple de la
  fiche FPT.TTS-ultra).
- Silence de début des fichiers Ultra (plus de 200 ms) : **gardé tel que
  FPT le livre** (DEC-0068). Le raccourcir reste possible
  (`ROGNER_ULTRA = True` dans `generer_audio_fpt.py`).
- Silence de fin des fichiers Ultra (environ 0,19 s) : **complété jusqu'à
  0,35 s**, sans rien couper ni fondre (DEC-0068).
- Mots espacés (phrases de « Combien de fois ? ») : **virgules** entre les
  mots (« Tôi, ăn, nem. »), à la place des points de suspension.
- Courbes d'E4 : `courbes_modele.py` prend par défaut F4 et F1.
- E1, voyelles simples (DEC-0070) : la voyelle **seule** (a, ă, â, e, ê, i,
  o, ô, ơ, u, ư), F4 et H6, débit normal seulement :
  `audio/V-<code du son>-<voix>-normal.mp3` (22 fichiers). Essai :
  `essai_voyelles.py`.
- Tarif de FPT.TTS-ultra : **à vérifier** sur la page du modèle avant une
  génération complète (environ 19 000 caractères).
- Essais : 07_QUALITE/essai_tts_ultra_2026-10-31.md (scripts
  `essai_ultra.py`, `essai_espacement.py`).

## 1 ter. Choix des voix et des modèles (écoute du 2026-10-29, historique)

| Code | Voix | Modèle | Décision |
|---|---|---|---|
| F1 | `std_banmai` | FPT.TTS-pro | gardée : claire en mot seul |
| H1 | `std_quanganh` | FPT.TTS-pro | écartée : consonne de départ avalée (syllabe d'environ 0,25 s, « x » absent) ; la même voix en FPT.TTS-ultra est **H6** (DEC-0067) |
| H2 | `fci_vietkhoa` | FPT.TTS-pro | écartée : même défaut |
| H3 | `std_leminh` | FPT.AI-VITs | gardée : claire en mot seul (« x » d'environ 140 ms) |
| H4 | `std_huyphong` | FPT.AI-VITs | gardée |
| H5 | `std_minhquan` | FPT.AI-VITs | claire, non retenue (choix : 2 femmes et 2 hommes) |
| F3 | `std_thuminh` | FPT.AI-VITs | gardée le 2026-10-29, écartée (DEC-0048), réintégrée le 2026-10-30 pour l'écoute des leçons de sons (DEC-0055), puis **écartée le 2026-10-31** : r- prononcé comme au Sud (DEC-0066) ; leçons de sons : F1 Ban Mai + H4 Huy Phong, remplacées le même jour par F4 + H6 (DEC-0067) ; code F2 réservé à l'ancienne voix *thuminh* de l'API FPT.AI |

> Ce tableau garde le choix du 29/10. Les voix actives sont celles du
> § 1 bis ; F1, F3, H3, H4 sont `inactive` dans `voix.csv` (DEC-0067).

Le modèle de chaque voix est dans la colonne `provider_model` de `voix.csv`.
Les mots sont envoyés **seuls**.

Pour H1 et H2, l'écriture « *mot*, *mot*. » suivie d'un découpage (2e
occurrence gardée) donnait un mot clair : cette méthode reste disponible
avec l'option `--doubler` (`decoupe_audio.py` : pause repérée sous
−50 dBFS, 0,06 s de marge, 0,1 s de silence avant et 0,35 s après ; brut
gardé dans `04_DONNEES/audio/_bruts/`). Elle nécessite `numpy` et
`soundfile`, présents dans `.venv-asr` : lancer alors le script avec
`.venv-asr\Scripts\python.exe`. Les essais sont dans
`04_DONNEES/audio/_essais/` (script `essai_variantes_fpt.py`).

## 1 quater. Égalisation du volume

Les voix n'ont pas le même niveau (mesure du 2026-10-29 : Huy Phong environ
5 dB plus faible que les autres). Chaque fichier est donc ramené à un
**niveau de parole de −20 dBFS** (moyenne des passages non silencieux),
sans que la crête dépasse **−1 dBFS** (pas de saturation). Le fichier reçu
de FPT, non retouché, reste dans `04_DONNEES/audio/_bruts/`.

Ce traitement utilise `numpy` et `soundfile`, présents dans
l'environnement Python du projet : le script se lance donc avec
`.venv-asr\Scripts\python.exe`.

## 2. Noms des fichiers

`audio/<référence>-<voix>-<débit>.mp3` : la référence est le code du mot
(`W0057`) ou, pour une syllabe hors corpus ou inventée, `S-` suivi de son
écriture « telex » en lettres simples (*xêm* → `S-xeem`, *chiện* →
`S-chieenj`).

## 3. Clé d'accès (DOC-04)

La clé (créée dans la marketplace : **Serverless Inference → API Keys**)
est rangée dans une **variable d'environnement** de Windows,
`FPT_MKP_API_KEY`, jamais dans un fichier du projet. La commande `setx`
l'enregistre pour votre compte Windows ; elle est lue par les programmes
lancés depuis une **nouvelle** fenêtre PowerShell. Elle se révoque depuis
la marketplace.

## 4. Commandes

Depuis `C:\VIET_PROJECT` :

| But | Commande |
|---|---|
| Voir le plan, sans rien appeler | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py .` |
| Essai : 4 fichiers | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --lecon M0-L01 --limite 4` |
| Une leçon | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --lecon M0-L01` |
| Refaire les audios déjà présents | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --refaire` |
| Tout ce qui manque | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer` |
| Lecteur d'essai avec ces audios | `python 05_PRODUCTION\tools\generer_lecteur.py . --non-valides` |

Arrêt possible à tout moment (Ctrl+C) ; relancer la même commande reprend
les fichiers manquants.

## 5. Validation (R-AUD-01)

Chaque audio est écouté avant de passer à `validated = true` (DEC-0065).

| Étape | Commande ou geste |
|---|---|
| 1. Fabriquer la page d'écoute | `python 05_PRODUCTION\tools\valider_audios.py .` |
| 2. Écouter | ouvrir `06_LIVRABLES\validation\validation_audios.html` ; choisir la leçon ; pour chaque carte : `Espace` (tout écouter), puis `Entrée` (tout le reste est bon) ou « À refaire » + une ou plusieurs raisons cochées (début tronqué, ton faux, son faux, trop numérique, trop lent, trop rapide, espace entre les mots trop faible, bruit, autre) |
| 3. Exporter | bouton « Exporter mes décisions » : fichier `validations_audios_<date>.csv` dans Téléchargements |
| 4. Appliquer | `python 05_PRODUCTION\tools\valider_audios.py . --appliquer` (dernier export du dossier Téléchargements) |
| 5. Refaire les refusés | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --refaire --liste 07_QUALITE\audios_a_refaire.csv`, puis retour à l'étape 1 |
| 6. Lecteur avec les audios validés seulement | `python 05_PRODUCTION\tools\generer_lecteur.py .` (sans `--non-valides`) |

**Pendant les exercices** (DEC-0069) : en mode test, le bouton
« ⚑ Signaler un son » du lecteur permet de cocher les défauts du son
entendu ; « Exporter les signalements » enregistre un fichier
`validations_audios_lecteur_<date>.csv` dans Téléchargements, que l'étape 4
(`--appliquer`) traite comme un export de la page de validation.

Seuls les audios du plan actuel sont proposés. Une décision ne vaut que
pour la version écoutée du fichier : un audio refait redevient « à écouter ».
Les décisions restent dans le navigateur tant qu'elles ne sont pas exportées :
exporter à la fin de chaque séance.

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
| 0.2 | 2026-10-29 | Passage à FPT.TTS-pro (marketplace.fptcloud.com), voix `std_banmai`, `std_quanganh` et `fci_vietkhoa`, clé `FPT_MKP_API_KEY`. |
| 0.3 | 2026-10-29 | Mots doublés puis découpés (2e occurrence) ; lancement avec `.venv-asr` ; option `--refaire`. |
| 0.4 | 2026-10-29 | Voix d'homme en FPT.AI-VITs (H3, H4, H5) ; H1 et H2 écartées ; mot seul, doublement en option (`--doubler`). |
| 0.5 | 2026-10-29 | Égalisation du volume (−20 dBFS, crête ≤ −1 dBFS) ; lancement avec `.venv-asr`. |
| 0.6 | 2026-10-29 | Voix retenues : 2 femmes (F1 Ban Mai, F3 Thu Minh) et 2 hommes (H3 Le Minh, H4 Huy Phong). |
| 0.7 | 2026-10-29 | Débit lent propre à chaque voix (F1 0,7 ; F3, H3, H4 0,6). |
| 0.8 | 2026-10-29 | Mots d'exemple d'E1 ajoutés au plan (DEC-0039) ; décisions des voix : DEC-0040. |
| 0.9 | 2026-10-30 | F3 Thu Minh écartée (DEC-0048). |
| 0.10 | 2026-10-30 | Voix d'écoute par type de leçon : sons F3 + H4, tons F1 + H3 + H4 provisoirement (DEC-0055). |
| 0.11 | 2026-10-30 | Débit lent de F3 : 0,8 (DEC-0059) ; options `--voix` et `--debit` du script. |
| 0.12 | 2026-10-31 | § 5 : outil de validation par l'écoute (`valider_audios.py`), option `--liste` (DEC-0065). |
| 0.13 | 2026-10-31 | F3 Thu Minh écartée ; leçons de sons : F1 + H4 (DEC-0066). |
| 0.14 | 2026-10-31 | § 1 bis : F4 Ban Mai et H6 Quang Anh en FPT.TTS-ultra, débit lent emprunté à F1 et H4, silences raccourcis, mots espacés par virgules (DEC-0067). |
| 0.15 | 2026-10-31 | Fichiers Ultra : début gardé brut, silence final complété à 0,35 s (DEC-0068). |
| 0.16 | 2026-10-31 | § 5 : signaler un son défectueux depuis le lecteur (DEC-0069). |
| 0.17 | 2026-10-31 | Voyelle seule en E1 (DEC-0070). |
| 0.18 | 2026-11-01 | MOD-B02 : titre et résumé (FPT.TTS-ultra) ; § 1 refait : plan actuel F4 / H6 (DEC-0067), fichiers présents comptés dans `audios.csv`, débits lents ; § 1 ter replacé dans l'histoire ; ligne 0.10 remise à sa place ; champs `entrees` et `sorties` remplis (DOC-30, DOC-32). |

## Liens

- **Entrées** : [REG-DEC](../02_REGLES/DECISIONS.md),
  [REG-REGLES](../02_REGLES/REGISTRE_REGLES.md),
  [DATA-MODELE](../04_DONNEES/00_modele_donnees.md)
- **Sorties** : [PROD-LECT](02_lecteur_activites.md),
  [QUAL-CONTRASTE-TONS-20261030](../07_QUALITE/contraste_tons_voix_2026-10-30.md),
  [QUAL-ESSAI-ULTRA-20261031](../07_QUALITE/essai_tts_ultra_2026-10-31.md),
  [QUAL-AVANCEMENT-20261031](../07_QUALITE/etat_avancement_2026-10-31.md)
