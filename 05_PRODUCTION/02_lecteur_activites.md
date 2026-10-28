---
id: PROD-LECT
titre: Lecteur d'activités — version d'essai
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Décrit la première version du lecteur d'activités (volet écoute E1 → E3,
  toutes les leçons du Module 0) : fichiers, génération, règles appliquées,
  ce qui est provisoire, comment l'essayer et ce qui reste à faire.
entrees: []
sorties: []
sources:
  - 02_REGLES/DECISIONS.md (DEC-0026 à DEC-0030, DEC-0032, DEC-0033)
  - 03_PROGRAMME/01_types_activites.md (PROG-ACT)
  - 03_PROGRAMME/progression_M0.md (PROG-M0)
  - 05_PRODUCTION/01_architecture_outils.md (PROD-ARCH)
---

# Lecteur d'activités — version d'essai

## Résumé

Le lecteur est un **site statique** (DEC-0030) : une page, une feuille de
style, un programme JavaScript et un fichier de données **généré** depuis
`04_DONNEES`. Cette version 0.1 couvre le **volet écoute** (E1, E2, E3 et
la révélation de l'écrit) pour les 13 leçons qui ont des séries. Le son
vient, en attendant les enregistrements validés, de la **voix de synthèse**
de l'appareil.

## 1. Fichiers

| Fichier | Rôle | Suivi par Git |
|---|---|---|
| `05_PRODUCTION/lecteur/index.html` | page | oui |
| `05_PRODUCTION/lecteur/lecteur.css` | présentation (clair et sombre, téléphone d'abord) | oui |
| `05_PRODUCTION/lecteur/lecteur.js` | déroulement des étapes, scores, verrous, progression | oui |
| `05_PRODUCTION/lecteur/images_provisoires.csv` | une image (emoji) par mot imageable, **provisoire** en attendant `images.csv` | oui |
| `05_PRODUCTION/lecteur/indications_symboles.csv` | mise en garde affichée sous chaque symbole en E1 (DEC-0029 § 4), **à relire** | oui |
| `05_PRODUCTION/tools/generer_lecteur.py` | générateur : CSV → lecteur | oui |
| `06_LIVRABLES/lecteur/` | résultat, regénérable (DOC-03) ; `lecteur_autonome.html` = tout en un fichier | non |

## 2. Générer et ouvrir

Dans PowerShell, depuis `C:\VIET_PROJECT` :

```
python 05_PRODUCTION\tools\generer_lecteur.py .
```

Puis ouvrir `06_LIVRABLES\lecteur\index.html` (double-clic). Aucune
installation n'est nécessaire ; le générateur n'utilise que Python.

## 3. Règles appliquées

| Règle | Dans le lecteur |
|---|---|
| R-PARC-01, R-VOL-01 | E1 → E2 → E3 → écrit ; chaque étape s'ouvre quand la précédente est faite |
| E1 (PROG-ACT) | chaque série : tous les termes, chaque voix, débit lent ; symbole et mise en garde ; réécoute libre |
| R-PARC-04, DEC-0033 | E2 : positions 1 et 2 de la série |
| R-PARC-05 | E3 : série complète (2 à 4 choix) |
| DEC-0028, DEC-0029 | débit lent : image + symbole ; débit normal : symbole seul, image en petit |
| R-ECR-01/02, R-LEX-06 | aucun écrit avant la fin d'E3 ; syllabes inventées jamais écrites (🔊) |
| R-VOL-05 à 07, DEC-0032 | passage au débit normal quand le seuil est atteint au débit lent ; étape validée au débit normal : seuil sur les 20 dernières réponses, au moins 2 voix, chaque série réussie 2 fois |
| PROG-ACT § 4 | tirage au hasard ; pas plus de 3 fois de suite la bonne réponse à la même place ; voix alternées ; pas de chronomètre |
| R-VOL-02 | la leçon suivante s'ouvre quand l'écoute de la précédente est validée |

**Essai automatique du 2026-10-28** (navigateur sans son, voix simulée,
une erreur sur dix) : L01 parcourue en entier ; E2 validée en 81 réponses,
E3 en 63 ; trois voix utilisées ; chaque série réussie au moins 2 fois ;
syllabes inventées jamais affichées ; L02 ouverte ensuite.

## 4. Provisoire

| Élément | Provisoire | Définitif |
|---|---|---|
| Son | voix de synthèse de l'appareil ; les « voix » F1, F2, H1 sont simulées par la hauteur | audios FPT.AI validés (DEC-0023), lus automatiquement dès qu'ils figurent dans `audios.csv` avec `validated = true` |
| Images | emoji | images OpenMoji dans `images.csv` (DEC-0024) |
| Progression | dans le navigateur de l'appareil | WordPress ou Firebase (DEC-0030) : seul l'objet `Stockage` de `lecteur.js` change |

> **Hypothèse** : la qualité des tons de la voix de synthèse varie selon
> l'appareil. Elle suffit pour essayer le lecteur, pas pour apprendre les
> tons : ne pas valider de leçon de tons (L02, L03, L07, L11) avec elle.

## 5. Reste à faire

1. Volet production (E4–E5) : micro, comparaison au modèle, courbe mélodique.
2. Leçon L14 (recyclage) : construite à partir de toutes les séries.
3. Écart de 3 leçons entre écoute et production (R-VOL-04) : à contrôler
   quand le volet production existera.
4. Paquets Anki par leçon validée (DEC-0015).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création : volet écoute, voix de synthèse provisoire. |
