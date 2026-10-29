---
id: PROD-AUDIO
titre: Génération des audios avec FPT.AI
statut: BROUILLON
version: 0.1
date: 2026-10-28
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
  - https://docs.fpt.ai/docs/en/speech/documentation/voice-maker (consulté le 2026-10-28)
---

# Génération des audios avec FPT.AI

## Résumé

Le script `05_PRODUCTION/tools/generer_audio_fpt.py` lit `04_DONNEES` et
demande à FPT.AI chaque audio manquant. Les fichiers vont dans
`04_DONNEES/audio/` et sont inscrits dans `audios.csv` avec
`validated = false`. Le lecteur ne les utilise qu'une fois **écoutés et
validés** (R-AUD-01), sauf en mode d'essai (`--non-valides`).

## 1. Ce qui est généré

| Volet | Contenu | Voix | Débits | Fichiers |
|---|---|---|---|---|
| Écoute (E1–E3) | 237 termes distincts des séries minimales | F1 *banmai*, F2 *thuminh*, H1 *leminh* | lent (vitesse FPT −2), normal (0) | 1 422 |
| Production (E4–E5) | mots supports absents des séries (8) | F1 (voix modèle, R-AUD-03) | lent, normal | 16 |
| **Total** | | | | **1 438**, environ 4 600 caractères |

Le débit rapide (E5) sera ajouté avec le volet production.

> **Fait** : l'application Voice Maker de FPT.AI annonce 100 000 caractères
> gratuits par mois (site consulté le 2026-10-28). **Hypothèse** : la même
> limite s'applique à l'API ; les archives mentionnaient « 900 caractères
> par jour », sans source. Le script s'arrête de lui-même après 5 erreurs
> sans succès, et reprend là où il s'est arrêté.

## 2. Noms des fichiers

`audio/<référence>-<voix>-<débit>.mp3` : la référence est le code du mot
(`W0057`) ou, pour une syllabe hors corpus ou inventée, `S-` suivi de son
écriture « telex » en lettres simples (*xêm* → `S-xeem`, *chiện* →
`S-chieenj`).

## 3. Clé d'accès (DOC-04)

La clé est rangée dans une **variable d'environnement** de Windows,
`FPT_AI_API_KEY`, jamais dans un fichier du projet. La commande `setx`
l'enregistre pour votre compte Windows ; elle est lue par les programmes
lancés depuis une **nouvelle** fenêtre PowerShell. Elle se révoque depuis
la console FPT.AI.

## 4. Commandes

Depuis `C:\VIET_PROJECT` :

| But | Commande |
|---|---|
| Voir le plan, sans rien appeler | `python 05_PRODUCTION\tools\generer_audio_fpt.py .` |
| Essai : un mot, 3 voix, 2 débits | `python 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --lecon M0-L01 --limite 6` |
| Une leçon | `python 05_PRODUCTION\tools\generer_audio_fpt.py . --executer --lecon M0-L01` |
| Tout ce qui manque | `python 05_PRODUCTION\tools\generer_audio_fpt.py . --executer` |
| Lecteur d'essai avec ces audios | `python 05_PRODUCTION\tools\generer_lecteur.py . --non-valides` |

Arrêt possible à tout moment (Ctrl+C) ; relancer la même commande reprend
les fichiers manquants.

## 5. Validation (R-AUD-01)

Chaque audio est écouté avant de passer à `validated = true`. Outil de
validation : **à faire** (page d'écoute qui produit la liste des audios
acceptés).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
