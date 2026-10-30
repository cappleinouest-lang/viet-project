---
id: PROG-ACT
titre: Types d'activités des étapes E1 à E5
statut: BROUILLON
version: 0.13
date: 2026-10-30
resume: >
  Catalogue des types d'activités, communs à toutes les leçons du Module 0 :
  pour chaque étape E1 à E5, ce que l'élève entend et voit, comment il
  répond, la correction, le score et la fin de l'étape. Le contenu de chaque
  leçon (mots, séries, nombre d'items) relève de PROG-M0.
entrees: [FOND-04, REG-REGLES, REG-DEC, DATA-MODELE]
sorties: [PROG-M0, PROD-ARCH, PROD-AF-LECT]
sources:
  - Uchihara, Karas et Thomson (2025), « High variability phonetic training (HVPT) - a meta-analysis of L2 perceptual training studies », Studies in Second Language Acquisition, 47, 794-827
  - _ARCHIVES/OLD/DOCS/00_CADRAGE/CADR_SPEC_STRUCTURE_MODULE_0_HYBRIDE_v02.md (§ 6, les 5 phases)
---

# Types d'activités des étapes E1 à E5

> Un **type d'activité** est une mécanique réutilisable (« Lequel ? »). Une
> **activité** est ce type appliqué à une leçon (« Lequel : *ma* ou *mạ* ? »).
> Aucun terme de support (carte, écran…) n'est employé ici (FOND-04 § 2).

## 1. Vue d'ensemble

| Étape | Code | Type d'activité | L'élève… | Noté ? |
|---|---|---|---|---|
| E1 Écouter | **ACT-E1-DECOUV** | Découverte | écoute chaque son (ou ton) seul, dans quelques mots | non |
| E2 Distinguer | **ACT-E2-PAREIL** | Pareil ou différent ? (échauffement) | entend deux mots, dit s'ils ont le même son | non |
| E2 Distinguer | **ACT-E2-LEQUEL** | Lequel ? (2 choix) | entend un terme, choisit A ou B | **oui** |
| E3 Opposer | **ACT-E3-LEQUEL** | Lequel ? (2 à 4 choix) | entend un terme, choisit dans la série | **oui** |
| E3 Opposer | **ACT-E3-COMBIEN** | Combien de fois ? | entend une suite de mots (puis une petite phrase), dit combien de fois il entend le son ou le ton | **oui** |
| E3 Opposer | **ACT-E3-ECRIT** | Révélation de l'écrit | voit l'écrit des termes réels, réécoute | non |
| E4 Répéter | **ACT-E4-REPETE** | Écoute et répète | imite le modèle, s'enregistre, compare | auto-évaluation |
| E5 Stabiliser | **ACT-E5-ENCHAINE** | Enchaînement | répète des séries mêlant leçons actuelle et précédentes | auto-évaluation |
| E5 Stabiliser | **ACT-E5-LIRE** | Lire puis vérifier | lit l'écrit à voix haute **avant** d'entendre le modèle | auto-évaluation |

## 2. Volet écoute

> **Place du son (DEC-0042)** : dans toutes les activités d'écoute, un
> symbole de consonne porte « début ▸ » ou « ◂ fin », et les consignes d'E2
> et E3 disent quoi écouter (consonne du début, de la fin, voyelle, ton).

> **Leçons de tons (DEC-0043, DEC-0045)** : jamais d'audio lent (E1,
> échauffement, E2, E3) ; en E2–E3, la première phase garde les images et
> **une seule voix** (F1, aussi dans l'échauffement), la seconde passe aux
> symboles seuls et à **plusieurs voix** ; toutes deux au débit normal.

### ACT-E1-DECOUV — Découverte

| Point | Règle |
|---|---|
| Entend | chaque son (ou ton) des séries de la leçon, **seul**, dans **3 mots au plus** (`exemples_e1.csv`, règle souple : ton déjà vu) ; chaque mot dit par **une voix de femme puis une voix d'homme**, deux boutons d'écoute : débit **normal** ou débit **lent**, et choix de la voix (femme et homme, femme, homme), au choix de l'élève (DEC-0039) |
| Voit | image du mot (ou 🔊) et son sens ; **symbole** de l'élément, avec sa **catégorie** (= ≈ ★), son **mot repère** et son **indice d'écoute** (DEC-0038) ; pictogramme du ton, ou `ipa_main` du son, présenté avec son audio (DEC-0029) ; **aucun écrit** (R-ECR-01) |
| Répond | rien ; peut **réécouter** autant qu'il veut, puis « suivant » |
| Fin | les mots de chaque son écoutés au moins une fois en entier |
| But | s'imprégner d'un modèle **juste** et varié, sans risque de confondre ; aucune opposition entre sons en E1, la première est la paire d'E2 (DEC-0039) |

> **ACT-E1-CONTRA (écoute contrastée) est supprimée** depuis DEC-0039.

### ACT-E2-PAREIL — Pareil ou différent ? (échauffement, DEC-0041)

| Point | Règle |
|---|---|
| Entend | deux termes de la paire d'E2, débit lent, **deux voix différentes** (même quand ils sont pareils) |
| Voit | deux réponses : **= Pareil**, **≠ Différent** ; après la réponse, les deux termes (image et symbole) |
| Répond | touche une réponse ; peut réécouter la paire ; puis réécouter chaque terme |
| Fin | 10 paires (moitié pareilles), puis passage au « Lequel ? » ; peut être refait |
| Note | **aucune** : hors score et hors verrou ; la validation d'E2 reste l'identification |

### ACT-E2-LEQUEL — Lequel ? (2 choix)

| Point | Règle |
|---|---|
| Entend | **un** terme de la paire minimale (DEC-0026), voix tirée au hasard parmi ≥ 2 |
| Voit | **deux** choix : au débit lent, **image + symbole**, avec catégorie et mot repère en petit (DEC-0038) ; au débit normal, **symbole seul**, l'image restant en petit (DEC-0028). Symbole : pictogramme et couleur du ton, ou `ipa_main` du son contrasté (ex. /ə/ – /o/) (DEC-0029). Sans image : symbole ou bouton sonore (syllabe inventée : DEC-0027) |
| Répond | touche un choix ; peut réécouter le terme avant de répondre |
| Correction | **immédiate** : juste → le terme est rejoué ; faux → la bonne réponse s'éclaire, puis les deux termes sont rejoués |
| Débit | **lent**, puis **normal** quand le seuil est atteint au débit lent |
| Score | part de réponses justes sur les **20 dernières** (paramètre) ; en plus, nombre de réussites **par série** au débit normal (DEC-0032) |

### ACT-E3-LEQUEL — Lequel ? (2 à 4 choix)

Même mécanique qu'E2, avec la **série complète** (2 à 4 termes, R-PARC-05).
Les séries de la leçon sont mêlées ; la position de la bonne réponse est
tirée au hasard.

### ACT-E3-COMBIEN — Combien de fois ? (DEC-0054)

| Point | Règle |
|---|---|
| Place | fin d'E3, après ACT-E3-LEQUEL, avant l'écrit |
| Entend | une **petite phrase** (DEC-0056 : ton de chaque mot déjà ouvert, autres sons libres) ou, à défaut, une **suite de 3 à 5 mots connus** ; une voix au hasard ; débit lent puis normal (normal seul dans les leçons de tons) |
| Voit | le son ou le ton à compter (symbole, place) ; **aucun écrit** avant la réponse |
| Répond | combien de fois il entend la cible : 0, 1, 2, 3, 4 ou 5 |
| Correction | juste / faux, puis **l'écrit est révélé**, syllabes cibles en évidence, avec la traduction de la phrase ; réécoute libre |
| Contenu | `04_DONNEES/comptage.csv` : nombre attendu **calculé** à partir de `syllabes.csv` ; mots dont tous les éléments sont ouverts (atomicité) ; autres mots pris de préférence parmi les éléments proches |
| Verrou | compte pour le verrou d'écoute, comme ACT-E3-LEQUEL : même seuil, 2 voix au moins |

### ACT-E3-ECRIT — Révélation de l'écrit

| Point | Règle |
|---|---|
| Quand | en fin d'E3, une fois le seuil atteint (R-ECR-02) |
| Voit | l'écrit de chaque terme **réel**, sous son image ; la syllabe inventée reste un bouton sonore (R-LEX-06) |
| Répond | rien ; réécoute libre. Pas de note : la lecture se travaille en E4–E5 |

### Verrou d'écoute (rappel R-VOL-05 à 07)

Seuil atteint en **E2 et E3**, au **débit normal**, sur **≥ 2 voix** :
85 %, 90 % pour les leçons de tons ; **et** chaque série de la leçon réussie
au moins **2 fois** au débit normal (paramètre, DEC-0032).

## 3. Volet production

### ACT-E4-REPETE — Écoute et répète

| Point | Règle |
|---|---|
| Entend | **un seul modèle** (même voix pour toute la leçon, R-AUD), lent puis normal |
| Voit | image + **écrit** (R-ECR-03) ; notation du son en option, jamais exigée (DEC-0021) ; pour un son absent ou proche du français, le **chemin de prononciation** (départ, un seul changement, vérification) de `reperes_sons.csv` (DEC-0038) |
| Répond | écoute, s'enregistre, puis réécoute son enregistrement **à côté** du modèle |
| Aide | **courbe mélodique** superposée au modèle (page de prononciation, PROD-ARCH) |
| Évaluation | l'élève se note : « proche » / « à reprendre » ; 3 essais au plus, puis item suivant |

### ACT-E5-ENCHAINE — Enchaînement

Séries de 4 à 6 items enchaînés sans pause, au rythme du modèle : lent,
normal, puis un peu plus rapide (FOND-04 § 3). Environ **1 item sur 3**
vient des leçons précédentes (paramètre).

### ACT-E5-LIRE — Lire puis vérifier

L'élève voit l'écrit (et l'image), **dit le mot avant d'entendre le modèle**,
puis écoute le modèle et se note. Reprend la « production semi-libre » des
archives : on vérifie qu'il produit sans imitation immédiate.

### Verrou de production

Production « intelligible » (R-VOL-08) : méthode **encore à définir**.
Proposition provisoire : « proche » sur 80 % des items d'E5, avec la courbe
mélodique dans la zone du modèle pour les tons, quand ses seuils seront
calibrés.

## 4. Règles communes

- **Une seule cible** par activité (FOND-04 § 6) ; atomicité par volet.
- **Tirage** : ordre aléatoire ; pas plus de **3 fois de suite** la même
  bonne réponse ; voix alternées.
- **Réécoute** toujours permise, jamais pénalisée.
- **Pas de chronomètre** dans le volet écoute.
- **Séance** : 20 à 30 min par jour (FOND-01) ; la répétition espacée des
  leçons validées se fait dans **Anki**, hors parcours (DEC-0015).

## 5. Ce que dit la recherche

**Faits** (Uchihara, Karas et Thomson, 2025, méta-analyse de 79 études) :

| Résultat | Effet sur ce document |
|---|---|
| L'entraînement par **identification** (g = 0,95) fait mieux que la **discrimination « même / différent »** (g = 0,57) | E2 et E3 sont des « Lequel ? » ; le « même / différent » ne sert plus que d'échauffement **non noté** en début d'E2 (DEC-0041) |
| Le **type de correction** ne change pas l'effet | correction simple : juste / faux, puis réécoute |
| Les progrès se **transfèrent** à de nouveaux mots et de nouvelles voix | les voix variées (DEC-0023) sont utiles |
| Les gains plafonnent après environ **400 minutes** d'entraînement au total | il est inutile d'allonger E2–E3 sans fin ; le verrou suffit |
| Les tons et les voyelles comptent parmi les cibles qui progressent le plus (g = 1,00) | cohérent avec le Module 0 |
| Des **images** comme étiquettes de réponse donnent un effet plus faible (g = 0,47) que des **mots écrits, l'orthographe ou des symboles** (0,90 à 1,03) | images, puis symboles (DEC-0028) |

## 6. Points à décider

1. ~~Étiquettes de réponse en E2–E3~~ → **décidé** : images, puis symboles
   (DEC-0028) ; symbole des sons = `ipa_main` du son contrasté (DEC-0029).
2. **Mesure du verrou de production** : proposition provisoire du § 3.
3. **Valeurs** : 20 dernières réponses, 3 essais en E4, 1 item sur 3
   d'anciennes leçons en E5.

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
| 0.2 | 2026-10-28 | Étiquettes E2–E3 : images, puis symboles (DEC-0028). |
| 0.3 | 2026-10-28 | Symbole des sons et symboles présentés dès E1 (DEC-0029). |
| 0.4 | 2026-10-28 | Verrou d'écoute : minimum de réussites par série (DEC-0032). |
| 0.5 | 2026-10-29 | Mots repères, catégories, indices d'écoute, chemins de prononciation (DEC-0038). |
| 0.6 | 2026-10-29 | E1 : découverte de chaque son seul dans 3 mots, voix de femme et d'homme ; ACT-E1-CONTRA supprimée (DEC-0039). |
| 0.7 | 2026-10-29 | ACT-E2-PAREIL : échauffement « Pareil ou différent ? » non noté (DEC-0041). |
| 0.8 | 2026-10-29 | Place du son indiquée partout (DEC-0042). |
| 0.9 | 2026-10-29 | Leçons de tons sans audio lent (DEC-0043). |
| 0.10 | 2026-10-29 | Tons : une seule voix en première phase (DEC-0045). |
| 0.11 | 2026-10-29 | Liens : ajout de PROD-AF-LECT en sorties (DOC-32). |
| 0.12 | 2026-10-30 | ACT-E3-COMBIEN « Combien de fois ? » (DEC-0054). |
| 0.13 | 2026-10-30 | Phrases plutôt que suites, règle souple (DEC-0056). |

## Liens

- **Entrées** : [FOND-04](../01_FONDATIONS/04_principes_pedagogiques.md),
  [REG-REGLES](../02_REGLES/REGISTRE_REGLES.md),
  [REG-DEC](../02_REGLES/DECISIONS.md),
  [DATA-MODELE](../04_DONNEES/00_modele_donnees.md)
- **Sorties** : PROG-M0 (à écrire),
  [PROD-ARCH](../05_PRODUCTION/01_architecture_outils.md)
