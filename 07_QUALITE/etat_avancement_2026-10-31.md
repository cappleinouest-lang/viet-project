---
id: QUAL-AVANCEMENT-20261031
titre: État d'avancement du projet au 31 octobre 2026
statut: VALIDE
version: 1.0
date: 2026-10-31
resume: >
  Point complet sur la formation au vietnamien du Nord (Module 0) : documents,
  décisions, données, audios, lecteur d'activités (volets écoute et production),
  outils, mesures de qualité, puis ce qui reste à faire, par priorité.
entrees: [CTX-IA, REG-DEC, PROD-LECT, PROD-AUDIO, QUAL-CONTRASTE-TONS-20261030]
sorties: []
sources:
  - Fichiers de C:\VIET_PROJECT relevés le 2026-10-31 (audios.csv, courbes_modele.csv, comptage.csv, voix.csv, donnees.js du lecteur généré le 2026-10-30 à 23 h 15)
---

# État d'avancement du projet au 31 octobre 2026

## Résumé

Le **Module 0** (sons et tons, 14 leçons) dispose d'un **lecteur d'activités
utilisable sur PC** : volet écoute complet (E1, échauffement, E2, E3,
« Combien de fois ? », écrit), volet production commencé (E4 avec micro et
courbe mélodique) et page de référence « Les 6 tons ». **4 491 audios** sont
produits, mais **aucun n'est encore validé** à l'écoute. Les fondations
pédagogiques sont validées ; **64 décisions** sont tracées. Restent surtout :
E5, la validation des audios, le verrou de production, la leçon de recyclage
L14, la relecture des contenus par un locuteur vietnamien et une sauvegarde
hors du PC.

| Domaine | Avancement | Commentaire |
|---|---|---|
| Fondations pédagogiques | ██████████ 100 % | FOND-01 à 04 validés |
| Règles et décisions | █████████░ 90 % | 64 décisions ; registre en brouillon |
| Données du Module 0 | ████████░░ 80 % | contenus complets ; relecture native à faire |
| Audios | ████████░░ 80 % | produits ; 0 validé |
| Lecteur — volet écoute | █████████░ 90 % | L14 manque ; verrous en mode essai |
| Lecteur — volet production | ████░░░░░░ 40 % | E4 fait ; E5 et verrou à faire |
| Révisions Anki | ░░░░░░░░░░ 0 % | non commencé |
| Mise en ligne (WordPress ou Firebase) | ░░░░░░░░░░ 0 % | choix après le lecteur |

> Les pourcentages sont une **estimation** de l'auteur, pas une mesure.

---

## 1. Documents et décisions

| Élément | État |
|---|---|
| Structure : 7 dossiers + `_ARCHIVES`, Markdown + CSV, Git | en place (DEC-0001 à 0003) ; `.gitignore` complété le 2026-10-30 (audios bruts, essais, anciens, fichiers de clé) |
| Fondations FOND-01 à 04 | **VALIDE** |
| `02_REGLES/DECISIONS.md` | **64 décisions** (DEC-0001 à DEC-0064), dont 30 prises les 29 et 30 octobre |
| `02_REGLES/REGISTRE_REGLES.md` | brouillon v0.18 ; R-ECR-01 assoupli (lettres du son, DEC-0063) |
| `CONTEXTE_IA.md` | à jour (v1.12, décisions jusqu'à DEC-0064) |
| `CARTE_DOCUMENTAIRE.md` | **ancienne** (29/10) : à regénérer (`build_doc_map.py`) |

### Décisions des 30 et 31 octobre, par thème

| Thème | Décisions |
|---|---|
| Voix | F3 Thu Minh écartée (0048) puis réintégrée : **leçons de sons = Thu Minh + Huy Phong** ; leçons de tons provisoirement Ban Mai, Le Minh, Huy Phong (0055) ; débit lent de Thu Minh 0,8 (0059) |
| Volet production | E4 d'abord, sur PC (0049) ; modèle lent puis normal, courbe partout (0050) |
| Lecteur | mode essai « tout ouvert » (0051) ; page « Les 6 tons » avec schémas et 10 séries (0052, 0053, 0064) |
| Écoute | exercice « Combien de fois ? » en fin d'E3, compté dans le verrou (0054) ; phrases en règle souple (0056) ; trois écoutes : normale, lente, mots espacés (0057, 0058) |
| Classificateurs | colonne `classifier` dans `mots.csv` (0060) ; **E1 et E4 seulement**, pas en E2–E3 (0061, 0062) |
| Écrit | lettres vietnamiennes du son dès E1 et en phase 1 (0063) |

---

## 2. Données (`04_DONNEES`)

| Fichier | Contenu | État |
|---|---|---|
| `lecons.csv` | 14 leçons (4 de tons, L14 recyclage) | complet |
| `mots.csv` | 332 mots, dont 120 noms ; **colonne `classifier`** (62 noms) | complet ; 24 classificateurs « à vérifier » |
| `paires_minimales.csv` | 95 séries minimales | complet ; termes hors corpus à confirmer |
| `sons.csv`, `tons.csv`, `syllabes.csv`, `ouvertures.csv`, `reperes_sons.csv` | sons, tons, décomposition, ouvertures, repères | complets |
| `exemples_e1.csv` | 302 mots d'exemple d'E1 (voix par type de leçon) | complet |
| `mots_lecons.csv` | 100 mots supports (E4) | complet |
| `comptage.csv` | **436 suites + 19 phrases** de « Combien de fois ? » | phrases seulement pour L01, L02, L04 ; à relire |
| `reference_tons.csv` | **10 séries** (a, i, u, o, ơ, ai, ao, uôi, -t, -c), 52 syllabes, 3 inventées | sens à relire |
| `voix.csv` | voix actives F1, F3, H3, H4 ; colonnes `listen_sounds` / `listen_tones` | à jour |
| `courbes_modele.csv` | **754 courbes** mélodiques (Ban Mai + série des tons) | à jour |
| `audios.csv` | **4 491 audios** | **0 validé** |
| `appuis_series.csv` | vide (essai abandonné, DEC-0061) | — |

---

## 3. Audios (FPT AI Marketplace)

| Usage | Nombre |
|---|---|
| Mots (séries, supports, exemples E1) | 1 324 |
| Syllabes hors corpus | 960 |
| Syllabes inventées | 281 |
| « Combien de fois ? » : suites | 1 676 |
| « Combien de fois ? » : phrases (normal, lent, espacé) | 114 |
| Classificateur + nom (E1, E4) | 100 |
| Essai abandonné « hai con… » en E2–E3 (inutilisés) | 36 |
| **Total** | **4 491** |

| Voix | Rôle | Débit lent | Audios |
|---|---|---|---|
| F1 Ban Mai | modèle d'E4 ; leçons de tons (provisoire) ; page des tons | 0,7 | 810 |
| F3 Thu Minh | leçons de sons | **0,8** (606 lents refaits le 30/10) | 1 432 |
| H3 Le Minh | leçons de tons (provisoire) ; page des tons | 0,6 | 730 |
| H4 Huy Phong | leçons de sons et de tons | 0,6 | 1 514 |

- Volume égalisé (−20 dBFS) ; fichiers bruts gardés dans `audio/_bruts/`.
- Coût FPT de l'ensemble : de l'ordre de **1 à 2 $**.
- **Aucun audio validé** (R-AUD-01) : le lecteur ne les joue qu'en mode
  d'essai (`--non-valides`).

---

## 4. Lecteur d'activités (`05_PRODUCTION/lecteur`, version 0.21)

Site statique ouvert par double-clic (`06_LIVRABLES/lecteur/index.html`) ou en
un seul fichier (`lecteur_autonome.html`). Testé sur PC (Chrome / Edge).
Progression enregistrée dans le navigateur.

### Volet écoute

| Étape | Fonctionnalités | État |
|---|---|---|
| E1 Découvrir | chaque son seul, 3 mots, femme / homme, normal / lent ; symbole, catégorie, repère, **lettres du son** ; noms avec **classificateur** | fait |
| Échauffement | « Pareil ou différent ? », non noté | fait |
| E2, E3 | « Lequel ? » ; phase 1 (images + symboles + lettres, lent), phase 2 (symboles seuls, normal) ; place du son ; tons : une voix puis plusieurs | fait |
| **Combien de fois ?** | phrases ou suites ; 3 écoutes ; écrit révélé après la réponse ; compte pour le verrou | fait |
| Écrit (fin d'E3) | écrit des termes réels | fait |
| L14 recyclage | — | **à faire** |

### Volet production

| Étape | Fonctionnalités | État |
|---|---|---|
| E4 Répéter | modèle Ban Mai lent puis normal, enregistrement, « Moi », « Moi puis le modèle », **courbes mélodiques**, chemin de prononciation, note proche / à reprendre, nom puis **classificateur + nom** | fait (sans verrou) |
| E5 Stabiliser | enchaînements, lecture avant écoute | **à faire** |
| Verrou de production (R-VOL-08) | — | **non décidé** |

### Autres écrans

- **Les 6 tons** : 10 séries, schémas, règle des syllabes fermées (sắc ou nặng
  seulement), deux voix.
- **Réglages** : vitesse de synthèse, question suivante automatique, aides,
  grand texte, **lettres du son**, **mode essai tout ouvert**, **infos de test
  sur le son**.
- **Mes progrès** par leçon.

---

## 5. Outils (`05_PRODUCTION/tools`)

| Script | Rôle |
|---|---|
| `generer_audio_fpt.py` | génère les audios (options `--lecon`, `--voix`, `--debit`, `--refaire`) |
| `courbes_modele.py` | calcule les courbes mélodiques du modèle |
| `generer_lecteur.py` | fabrique le lecteur à partir des données |
| `choisir_exemples_e1.py`, `choisir_suites_comptage.py` | composent les mots d'E1 et les suites / vérifient les phrases |
| `regle_classificateurs.py` | règle commune des classificateurs |
| `tester_voix_tons.py`, `tester_appui.py`, `essai_variantes_fpt.py` | essais et mesures de voix |
| `choisir_appuis.py` | abandonné (DEC-0061) |
| page `essai_micro.html` | essai du micro et des courbes |

---

## 6. Qualité et mesures

| Mesure | Résultat (2026-10-30) |
|---|---|
| Contraste des tons par voix (36 mots) | Thu Minh 94 %, Huy Phong 81 %, Ban Mai 78 %, Le Minh 81 % (contraste plus faible), Quang Anh 61 %, Minh Quan 58 % |
| Faiblesses communes de la synthèse FPT | *huyền* ≈ *hỏi* par la mélodie ; *nặng* pas assez bas |
| Début de mot tronqué | Thu Minh et Huy Phong : consonnes brèves ; « hai + classificateur » les allonge |
| Saturation de Thu Minh au ralenti | due à la synthèse à 0,6 → passée à 0,8 |
| Courbes Python / navigateur | identiques (écart < 0,01 demi-ton) |

Rapports : `07_QUALITE/contraste_tons_voix_2026-10-30.md`,
`07_QUALITE/proposition_classificateurs_2026-10-30.csv`.

---

## 7. Ce qui reste à faire

### Priorité haute

1. **Valider les audios** (R-AUD-01) : outil d'écoute qui marque
   `validated = true` ; sans lui, le lecteur reste en mode d'essai.
2. **Sauvegarde hors du PC** : dépôt privé GitHub (l'historique n'existe que
   sur le PC).
3. **Relecture par un locuteur vietnamien** : 19 phrases, 24 classificateurs
   « à vérifier », sens des mots de la page des tons, 74 termes hors corpus.
4. **Voix des leçons de tons** : choisir le « locuteur le plus adapté »
   (aujourd'hui provisoire).

### Priorité moyenne

5. **E5 Stabiliser** : enchaînements, lecture avant écoute, classificateurs.
6. **Verrou de production** (R-VOL-08) : méthode à décider.
7. **Phrases de « Combien de fois ? »** pour toutes les leçons.
8. **L14** : leçon de recyclage.
9. **Présentation de chaque classificateur** à sa première apparition.
10. **Images définitives** (OpenMoji) à la place des emoji.

### Plus tard

11. Contrôle de l'écart de 3 leçons entre écoute et production (R-VOL-04).
12. Paquets **Anki** par leçon validée.
13. Choix de l'enveloppe (WordPress ou Firebase), mise en ligne en https
    (nécessaire pour le micro sur téléphone).
14. Couper le **mode test** et le **mode essai** avant d'ouvrir à d'autres
    apprenants.
15. Regénérer `CARTE_DOCUMENTAIRE.md`.

## Risques

| Risque | Effet | Parade |
|---|---|---|
| Synthèse vocale imparfaite sur les tons (*hỏi*, *nặng*) | l'oreille apprend un modèle approximatif | enregistrement natif au moins pour la page des tons et E4 |
| Contenus non relus par un natif | erreurs de sens ou phrases peu naturelles | relecture avant ouverture à d'autres apprenants |
| Historique seulement sur le PC | perte totale en cas de panne | dépôt GitHub privé |
| Mode essai actif | verrous non éprouvés en conditions réelles | tester un parcours complet avec les verrous |

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-31 | Création. |
