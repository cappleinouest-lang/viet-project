---
id: PROD-AUDIO
titre: Génération des audios avec FPT.TTS-pro (FPT AI Marketplace)
statut: BROUILLON
version: 0.12
date: 2026-10-31
resume: >
  Explique comment générer, avec FPT.AI, les audios du Module 0 décrits par
  04_DONNEES : ce qui est produit, où va la clé d'accès, les commandes, la
  reprise après interruption et la validation par l'écoute.
entrees: []
sorties: []
sources:
  - 02_REGLES/DECISIONS.md (DEC-0023)
  - 02_REGLES/REGISTRE_REGLES.md (R-AUD-01 à R-AUD-06)
  - _ARCHIVES/Projet de Formation_Vietnamien_A0_to_A2/PROD/00_GLOBAL/01_DB/02_SCRIPTS/04_POPULATION/EXP_generate_audio_fptai_v01.py (appel de l'API, réglages de vitesse)
  - marketplace.fptcloud.com, Voice Studio, bouton View Code (relevé le 2026-10-29)
  - https://factory.fpt.ai/pricing?service=serverless-inference (consulté le 2026-10-29)
---

# Génération des audios avec FPT.TTS-pro (FPT AI Marketplace)

## Résumé

Le script `05_PRODUCTION/tools/generer_audio_fpt.py` lit `04_DONNEES` et
demande à FPT (FPT.TTS-pro ou FPT.AI-VITs selon la voix) chaque audio manquant
(`POST https://mkp-api.fptcloud.com/v1/audio/speech`, format proche d'OpenAI). Les fichiers vont dans
`04_DONNEES/audio/` et sont inscrits dans `audios.csv` avec
`validated = false`. Le lecteur ne les utilise qu'une fois **écoutés et
validés** (R-AUD-01), sauf en mode d'essai (`--non-valides`).

## 1. Ce qui est généré

| Volet | Contenu | Voix | Débits | Fichiers |
|---|---|---|---|---|
| Écoute (E1–E3) | 237 termes distincts des séries minimales | F1 Ban Mai (femme), H3 Le Minh, H4 Huy Phong (hommes) ; F3 Thu Minh écartée (DEC-0048), fichiers gardés | lent (`speed` propre à chaque voix), normal (1) | 1 896 |
| Production (E4–E5) | mots supports absents des séries (8) | F1 (voix modèle, R-AUD-03) | lent, normal | 16 |
| Découverte (E1) | mots d'exemple de `exemples_e1.csv` (DEC-0039) | voix de femme et voix d'homme prévues pour chaque mot | lent, normal | environ 326 de plus |
| **Total** | | | | **2 238** (2026-10-29), environ 6 000 caractères |

Débit lent choisi à l'écoute le 2026-10-29 (essais à 0,7, 0,6, 0,5) : F1 = 0,7 ; F3, H3, H4 = 0,6
(colonne `provider_speed_slow` de `voix.csv`). Le débit rapide (E5)
sera ajouté avec le volet production.

> **Fait** : la page de tarifs indique 16,50 $ par million de caractères
> pour FPT.TTS-pro comme pour FPT.AI-VITs (2026-10-29), soit moins de
> 0,10 $ pour l'ensemble. Service payant (portefeuille prépayé) ; erreur
> 402 = solde à zéro. Le script s'arrête de lui-même sur une erreur de clé
> (401) ou de solde (402), ou après 5 erreurs sans succès, et reprend là où
> il s'est arrêté.

## 1 bis. Choix des voix et des modèles (écoute du 2026-10-29)

| Code | Voix | Modèle | Décision |
|---|---|---|---|
| F1 | `std_banmai` | FPT.TTS-pro | gardée : claire en mot seul |
| H1 | `std_quanganh` | FPT.TTS-pro | écartée : consonne de départ avalée (syllabe d'environ 0,25 s, « x » absent) |
| H2 | `fci_vietkhoa` | FPT.TTS-pro | écartée : même défaut |
| H3 | `std_leminh` | FPT.AI-VITs | gardée : claire en mot seul (« x » d'environ 140 ms) |
| H4 | `std_huyphong` | FPT.AI-VITs | gardée |
| H5 | `std_minhquan` | FPT.AI-VITs | claire, non retenue (choix : 2 femmes et 2 hommes) |
| F3 | `std_thuminh` | FPT.AI-VITs | gardée le 2026-10-29, écartée (DEC-0048), puis **réintégrée le 2026-10-30 pour l'écoute des leçons de sons** : tons les plus nets à la mesure (DEC-0055) ; code F2 réservé à l'ancienne voix *thuminh* de l'API FPT.AI |

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

## 1 ter. Égalisation du volume

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
| 2. Écouter | ouvrir `06_LIVRABLES\validation\validation_audios.html` ; choisir la leçon ; pour chaque carte : `Espace` (tout écouter), puis `Entrée` (tout le reste est bon) ou « À refaire » + raison |
| 3. Exporter | bouton « Exporter mes décisions » : fichier `validations_audios_<date>.csv` dans Téléchargements |
| 4. Appliquer | `python 05_PRODUCTION\tools\valider_audios.py . --appliquer` (dernier export du dossier Téléchargements) |
| 5. Refaire les refusés | `.venv-asr\Scripts\python.exe 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --refaire --liste 07_QUALITE\audios_a_refaire.csv`, puis retour à l'étape 1 |
| 6. Lecteur avec les audios validés seulement | `python 05_PRODUCTION\tools\generer_lecteur.py .` (sans `--non-valides`) |

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
| 0.11 | 2026-10-30 | Débit lent de F3 : 0,8 (DEC-0059) ; options `--voix` et `--debit` du script. |
| 0.12 | 2026-10-31 | § 5 : outil de validation par l'écoute (`valider_audios.py`), option `--liste` (DEC-0065). |
| 0.10 | 2026-10-30 | Voix d'écoute par type de leçon : sons F3 + H4, tons F1 + H3 + H4 provisoirement (DEC-0055). |
