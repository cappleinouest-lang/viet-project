---
id: PROD-LECT
titre: Lecteur d'activités — version d'essai
statut: BROUILLON
version: 0.21
date: 2026-11-01
resume: >
  Décrit la version d'essai du lecteur d'activités (volet écoute E1 → E3 et
  « Combien de fois ? », E4 du volet production, page « Les 6 tons ») :
  fichiers, génération, règles appliquées, ce qui est provisoire, comment
  l'essayer et ce qui reste à faire.
entrees: [PROD-AF-LECT, PROD-AUDIO]
sorties: [QUAL-AVANCEMENT-20261031]
sources:
  - 02_REGLES/DECISIONS.md (DEC-0026 à DEC-0030, DEC-0032, DEC-0033, DEC-0037 à DEC-0070)
  - 05_PRODUCTION/tools/generer_lecteur.py et lecteur/lecteur.js (relus le 2026-11-01)
  - 03_PROGRAMME/01_types_activites.md (PROG-ACT)
  - 03_PROGRAMME/progression_M0.md (PROG-M0)
  - 05_PRODUCTION/01_architecture_outils.md (PROD-ARCH)
---

# Lecteur d'activités — version d'essai

## Résumé

Le lecteur est un **site statique** (DEC-0030) : une page, une feuille de
style, un programme JavaScript et un fichier de données **généré** depuis
`04_DONNEES`. La version 0.1 couvrait le **volet écoute** (E1, E2, E3 et
la révélation de l'écrit) pour les 13 leçons qui ont des séries ; s'y sont
ajoutés l'échauffement, « Combien de fois ? », E4 (volet production), la
page « Les 6 tons » et les audios FPT. Les audios sont joués quand ils sont
**validés** (ou tous en mode d'essai, `--non-valides`) ; sinon, la **voix de
synthèse** de l'appareil.

Depuis DEC-0067, deux voix : **F4 Ban Mai** (femme, voix modèle) et
**H6 Quang Anh** (homme), en FPT.TTS-ultra ; au débit lent, le lecteur joue
les fichiers de F1 et H4 (colonne `slow_from` de `voix.csv`).

## 1. Fichiers

| Fichier | Rôle | Suivi par Git |
|---|---|---|
| `05_PRODUCTION/lecteur/index.html` | page | oui |
| `05_PRODUCTION/lecteur/lecteur.css` | présentation (clair et sombre, téléphone d'abord) | oui |
| `05_PRODUCTION/lecteur/lecteur.js` | déroulement des étapes, scores, verrous, progression | oui |
| `05_PRODUCTION/lecteur/images_provisoires.csv` | une image (emoji) par mot imageable, **provisoire** en attendant `images.csv` | oui |
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
| E1 (PROG-ACT, DEC-0039) | un écran par son (ou ton) : symbole, catégorie, repère, indice ; 3 mots au plus (`exemples_e1.csv`), chacun dit par une voix de femme puis d'homme ; deux boutons « ▶ Écouter » (débit normal) et « 🐢 Écouter lentement » (débit lent), choix de la voix « Femme et homme » (par défaut), « Femme » ou « Homme » ; toucher un mot le redit avec la voix et la dernière vitesse choisies ; pour une voyelle simple (leçons de sons), tuile « 🔈 Le son seul » jouée avant les mots, au débit normal seulement, si son audio est validé ou en mode d'essai (DEC-0070) ; aucun mot écrit (lettres du son : DEC-0063) ; aucune opposition ; « suivant » après une écoute complète. Progression antérieure : une E2 commencée vaut E1 faite |
| R-PARC-04, DEC-0033 | E2 : positions 1 et 2 de la série |
| DEC-0042 | place du son : marque « début ▸ » / « ◂ fin » sur chaque symbole de consonne ; en E1, en-tête « consonne en début / fin de mot » ou « voyelle » ; en E2 et E3, consigne « Écoutez la consonne du début du mot », etc. |
| DEC-0047 | mode test : dans la case du mot joué, une ligne par voix : fichier (ou « synthèse de l'appareil »), personnage · F/H · code, modèle · débit · `speed` ; en E2, E3 et à l'échauffement, seulement après la réponse ; réglage « Infos de test sur le son ». Au débit lent, la voix qui fournit le fichier est indiquée (DEC-0067) |
| DEC-0069 | en mode test, bouton « ⚑ Signaler un son » dans tous les exercices : 8 derniers sons joués, défauts à cocher, remarque ; export `validations_audios_lecteur_<date>.csv` (traitement : PROD-AUDIO § 5) |
| DEC-0067 | voix d'écoute de toutes les leçons (sons et tons) : F4 et H6 (colonnes `listen_sounds` et `listen_tones` de `voix.csv`) ; débit lent pris à la voix `slow_from` (F4 ← F1, H6 ← H4) |
| DEC-0045 | leçons de tons : échauffement avec la même voix, la voix modèle (F4 depuis DEC-0067), pour les deux mots ; E2–E3 phase « avec images » avec la voix modèle seule, phase « symboles seuls » avec les voix d'écoute de la leçon (F4 et H6) |
| DEC-0043 | leçons de tons : audio toujours au débit normal (E1 sans « Écouter lentement », échauffement, E2, E3) ; phases d'E2–E3 nommées « avec images » puis « symboles seuls » |
| DEC-0041 | E2 commence par 10 paires « Pareil ou différent ? » non notées (deux voix différentes par paire, termes montrés après la réponse) ; bouton « Pareil ou différent ? » sur l'étape E2 pour le refaire ; une E2 déjà commencée le saute |
| R-PARC-05 | E3 : série complète (2 à 4 choix) |
| DEC-0028, DEC-0029 | débit lent : image + symbole ; débit normal : symbole seul, image en petit |
| R-ECR-01/02, R-LEX-06 | aucun écrit avant la fin d'E3 ; syllabes inventées jamais écrites (🔊) |
| R-VOL-05 à 07, DEC-0032 | passage au débit normal quand le seuil est atteint au débit lent ; étape validée au débit normal : seuil sur les 20 dernières réponses, au moins 2 voix, chaque série réussie 2 fois |
| PROG-ACT § 4 | tirage au hasard ; pas plus de 3 fois de suite la bonne réponse à la même place ; voix alternées ; pas de chronomètre |
| R-VOL-02 | la leçon suivante s'ouvre quand l'écoute de la précédente est validée |
| DEC-0038 | symbole de son avec sa catégorie (= ≈ ★, couleur et marque), son mot repère (🇫🇷 mot écrit, 🇻🇳 image seule) et son indice d'écoute en E1 ; catégorie et repère en petit au débit lent ; symbole seul au débit normal. Données : `04_DONNEES/reperes_sons.csv` |
| DEC-0054, DEC-0056 à DEC-0058 | « Combien de fois ? » en fin d'E3 : suites ou phrases, deux phases, trois écoutes des phrases (normale, lente, mots espacés par virgules depuis DEC-0067), écrit révélé après la réponse, verrou comme E2–E3 |
| DEC-0052, DEC-0053, DEC-0064 | page « Les 6 tons » : 10 séries, schéma de chaque ton, voix F4 ou H6 (`voix_reference_tons`), débit normal ou lent |
| DEC-0037 | leçon marquée `split_parts` (L01) : partie A voyelles, puis partie B consonnes et finales, chacune avec E1 → E3, son verrou et l'écrit ; l'écoute de la leçon est validée après la dernière partie |

**Essai automatique du 2026-10-28** (navigateur sans son, voix simulée,
une erreur sur dix) : L01 parcourue en entier ; E2 validée en 81 réponses,
E3 en 63 ; trois voix utilisées ; chaque série réussie au moins 2 fois ;
syllabes inventées jamais affichées ; L02 ouverte ensuite.

**Essai du 2026-10-29** (L01 en deux parties) : partie A, E2 en 40 réponses
et E3 en 42 ; partie B, E2 en 41 et E3 en 44 ; la progression enregistrée
avec l'ancienne version est reprise et répartie entre les deux parties.

## 3 bis. Réglages et suivi

| Écran | Contenu |
|---|---|
| **Réglages** (accueil) | vitesse de la voix de synthèse (plus lente, normale, plus rapide) ; question suivante automatique après une bonne réponse ; aides sous les symboles (repère, indice) ; grand texte. Enregistrés sur l'appareil |
| **Mes progrès** (leçon) | par jour : réponses, temps (écarts de moins de 2 min entre deux réponses), réussite ; par série : réussite au débit normal, les plus difficiles en premier ; confusions fréquentes (« /o/ entendu, /ɔ/ choisi ») |
| **Partie terminée** | réduite à une ligne « Validée », avec « Afficher » |

Chaque réponse enregistre désormais l'heure, le terme attendu et le terme
choisi ; les réponses données avant cette version n'ont pas ces détails.

## 4. Provisoire

| Élément | Provisoire | Définitif |
|---|---|---|
| Son | voix de synthèse de l'appareil pour les mots sans fichier ; les voix F4 et H6 y sont simulées par la hauteur. Essai avec les audios FPT non encore validés : `generer_lecteur.py . --non-valides`. Au 2026-11-01, les audios F4 / H6 n'existent que pour L01 (PROD-AUDIO § 1) : les autres leçons jouent la voix de synthèse | audios FPT validés (DEC-0023, DEC-0067), lus automatiquement dès qu'ils figurent dans `audios.csv` avec `validated = true` |
| Images | emoji | images OpenMoji dans `images.csv` (DEC-0024) |
| Progression | dans le navigateur de l'appareil | WordPress ou Firebase (DEC-0030) : seul l'objet `Stockage` de `lecteur.js` change |

> **Hypothèse** : la qualité des tons de la voix de synthèse varie selon
> l'appareil. Elle suffit pour essayer le lecteur, pas pour apprendre les
> tons : ne pas valider de leçon de tons (L02, L03, L07, L11) avec elle.

## 5. Reste à faire

1. Volet production (E4–E5) : micro, comparaison au modèle, courbe mélodique.
   **En cours** (DEC-0049) : E4 d'abord, sur PC. Étape 1 faite : page d'essai
   `05_PRODUCTION/lecteur/essai_micro.html` (double-clic ; code commun
   `prononciation.js` : micro, courbe mélodique par l'algorithme YIN, demi-tons
   autour de la hauteur médiane, temps ramené de 0 à 1). Limite connue : chaque
   courbe est rapportée à SA propre médiane, elle montre la forme du ton, pas
   son registre (haut / bas). Étape 2 (DEC-0050) : courbes du modèle (F4
   depuis DEC-0067, lent F1) calculées à l'avance par `tools/courbes_modele.py` (même calcul que
   `prononciation.js`) dans `04_DONNEES/courbes_modele.csv`. Étape 3 : **E4 intégré
   au lecteur** (version 0.15) : mots supports de la leçon (`mots_lecons.csv`),
   ouverts quand l'écoute de la leçon est validée ; passage 1 avec le modèle lent
   (fichiers de F1), passage 2 avec le modèle normal (F4) ; pour chaque mot : écrit, image, son ou
   ton visé avec son chemin de prononciation, modèle, enregistrement, « Moi »,
   « Moi puis le modèle », courbes, note « proche » / « à reprendre » (3 essais
   au plus, paramètre `essais_max_e4`). E4 est marquée « parcourue », sans verrou
   (R-VOL-08 non décidé). Les enregistrements ne sont ni gardés ni envoyés.
   Non contrôlé : l'écart de 3 leçons entre écoute et production (R-VOL-04).
   Avant de générer : lancer `courbes_modele.py` (voir PROD-AUDIO).
2. Leçon L14 (recyclage) : construite à partir de toutes les séries.
3. Écart de 3 leçons entre écoute et production (R-VOL-04) : à contrôler
   quand le volet production existera.
4. Paquets Anki par leçon validée (DEC-0015).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création : volet écoute, voix de synthèse provisoire. |
| 0.2 | 2026-10-29 | Leçons en deux parties (DEC-0037) ; reprise de l'ancienne progression. |
| 0.3 | 2026-10-29 | Mots repères et catégories de sons (DEC-0038) ; `indications_symboles.csv` remplacé par `04_DONNEES/reperes_sons.csv`. |
| 0.4 | 2026-10-29 | Réglages, suivi des progrès, parties terminées réduites. |
| 0.5 | 2026-10-29 | E1 = découverte de chaque son seul (DEC-0039) ; voix F3, H3, H4 en synthèse provisoire. |
| 0.6 | 2026-10-29 | Échauffement « Pareil ou différent ? » en début d'E2 (DEC-0041). |
| 0.7 | 2026-10-29 | Place du son indiquée (DEC-0042). |
| 0.8 | 2026-10-29 | Leçons de tons sans audio lent (DEC-0043). |
| 0.9 | 2026-10-29 | Tons : une voix puis plusieurs (DEC-0045). |
| 0.10 | 2026-10-29 | Liens : ajout de PROD-AF-LECT en entrees (DOC-32). |
| 0.11 | 2026-10-29 | Code du lecteur commenté (index.html, lecteur.css, lecteur.js) : guide en tête de chaque fichier, sections numérotées, rôle de chaque fonction. Aucune instruction modifiée (vérifié par comparaison du code sans commentaires). |
| 0.12 | 2026-10-30 | Mode test : informations sur le son joué (DEC-0047). |
| 0.13 | 2026-10-30 | Voix F3 écartée : 3 voix actives (DEC-0048). |
| 0.14 | 2026-10-30 | Volet production, étape 1 : page d'essai du micro et de la courbe (DEC-0049). |
| 0.15 | 2026-10-30 | E4 « Écoute et répète » intégré au lecteur (DEC-0050) ; courbes du modèle dans donnees.js ; prononciation.js chargé par index.html et inclus dans lecteur_autonome.html. |
| 0.16 | 2026-10-30 | Réglage « Mode essai : tout ouvert », activé par défaut (DEC-0051). |
| 0.17 | 2026-10-30 | Écran « Les 6 tons » : série ma… mạ, courbes sur une même échelle (DEC-0052). |
| 0.18 | 2026-10-30 | « Les 6 tons » : schéma de chaque ton à la place des courbes mesurées (DEC-0053). |
| 0.19 | 2026-10-30 | Voix d'écoute propres à chaque leçon (`l.voix`, DEC-0055). |
| 0.20 | 2026-10-30 | Écran « Combien de fois ? » en fin d'E3 (DEC-0054) : deux phases, verrou comme E2/E3, écrit de la suite révélé après la réponse ; l'écrit d'E3 s'ouvre après sa validation. |
| 0.21 | 2026-11-01 | MOD-B03 : changements du lecteur des 30 et 31/10 décrits : voix F4 / H6 et débit lent emprunté (DEC-0067), signalement d'un son (DEC-0069), voyelle seule en E1 (DEC-0070), « Combien de fois ? » et page « Les 6 tons » au § 3 ; § 4 et § 5 sans F1, H3, H4 ; résumé ; liens (DOC-32). |

## Liens

- **Entrées** : [PROD-AF-LECT](04_analyse_fonctionnelle_lecteur.md),
  [PROD-AUDIO](03_audio.md)
- **Sorties** : [QUAL-AVANCEMENT-20261031](../07_QUALITE/etat_avancement_2026-10-31.md)
