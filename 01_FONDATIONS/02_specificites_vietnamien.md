---
id: FOND-02
titre: Spécificités du vietnamien
statut: VALIDE
version: 1.0
date: 2026-10-28
resume: >
  Décrit les propriétés du vietnamien du Nord qui déterminent la conception
  de la formation : tons, structure de la syllabe, voyelles, consonnes,
  orthographe, rythme et grammaire. Fixe la notation phonétique de référence
  du projet. Les difficultés propres aux francophones sont traitées dans FOND-03.
entrees: [FOND-01]
sorties: [FOND-03, FOND-04, REG-REGLES, 04_DONNEES/tons.csv, 04_DONNEES/phonemes.csv]
sources:
  - _ARCHIVES/OLD/DOCS/00_CADRAGE/P0_CADR_GLOB_01_NORM_Specificites_Langue_Vietnamienne_v3.md
  - _ARCHIVES/OLD/DOCS/01_REFERENCES/Archives/01_synthese_specificites_langue_vietnamienne_.md
  - _ARCHIVES/Projet sous Anki/03_DATA_CSV/language/tones.csv et phonemes.csv
  - 02_REGLES/DECISIONS.md (DEC-0005, DEC-0008, DEC-0009)
  - Kirby, J. (2011). Vietnamese (Hanoi Vietnamese). Journal of the International Phonetic Association, 41(3).
  - Brunelle, M. (2009). Tone perception in Northern and Southern Vietnamese. Journal of Phonetics, 37(1).
---

# Spécificités du vietnamien

## Résumé

Le vietnamien est une langue **à tons** (6 tons), **monosyllabique** dans sa
structure (chaque syllabe a un sens ou une fonction) et **isolante** (les mots
ne changent jamais de forme). Sa syllabe suit un modèle fixe et fermé ; son
écriture utilise l'alphabet latin avec des correspondances lettre-son très
différentes du français. La formation vise la **variété du Nord (Hanoï)**.

> **Règle** : la notation phonétique du projet est celle de la base
> (`04_DONNEES/phonemes.csv`) : notamment **ư = /ɨ/** et **ơ = /ə/** (DEC-0008).

## 1. Les tons

Chaque syllabe porte **obligatoirement** un ton, qui fait partie du mot au
même titre que ses voyelles et ses consonnes. Changer de ton, c'est changer
de mot.

| Ton | Signe | Mélodie (Hanoï) | Chiffres Chao* | Qualité de la voix | Exemple |
|---|---|---|---|---|---|
| **ngang** | aucun | moyen, plat | 33 | normale | *ma* (fantôme) |
| **huyền** | ` | bas, descendant | 21 | parfois soufflée | *mà* (mais) |
| **sắc** | ´ | montant | 35 | tendue | *má* (joue, maman au Sud) |
| **hỏi** | ̉ | descend, puis remonte un peu ou pas | 313 ou 31 | devient tendue | *mả* (tombe) |
| **ngã** | ~ | montant, **cassé au milieu** | 3ˀ5 | grinçante ou coup de glotte **au milieu** | *mã* (cheval) |
| **nặng** | ̣ | bas, descendant, **court** | 21ʔ | se ferme par un coup de glotte **à la fin** | *mạ* (plant de riz) |

\* Échelle de 1 (grave) à 5 (aigu) : « 35 » = part du niveau 3 et monte au
niveau 5. « ˀ » ou « ʔ » = glottalisation (fermeture des cordes vocales).

**Points essentiels :**
- En vietnamien du Nord, les tons se reconnaissent à leur **mélodie** et à la
  **qualité de la voix** : voix grinçante, coup de glotte (Brunelle, 2009).
  C'est le cas en particulier pour hỏi, ngã et nặng.
- À Hanoï, **hỏi** est souvent réalisé sans remontée finale (31). Cela le
  rapproche de huyền : c'est alors la qualité de la voix qui les distingue
  (Kirby, 2011).
- Les tons ne sont pas des intonations : l'intonation de la phrase (question,
  exclamation) se superpose aux tons **sans les modifier**. La question
  passe souvent par des **particules finales** (*không ?*, *à ?*, *nhé*).

> **Correction** : `tones.csv` note ngã « 35ʔ » (coup de glotte à la fin).
> La description de référence le place **au milieu** de la syllabe : « 3ˀ5 »
> (Kirby, 2011). À corriger lors de la reprise des données.

## 2. La syllabe

Modèle unique : **[consonne initiale] + noyau vocalique + [consonne finale] + ton**

| Élément | Présence | Contenu |
|---|---|---|
| Consonne initiale | facultative | simple (b, m, t…) ou écrite en deux ou trois lettres (ng, nh, ngh, tr, kh, th, ph, gi…) |
| Noyau vocalique | **obligatoire** | voyelle simple, diphtongue ou triphtongue, éventuellement précédée d'un son « w » (*oa*, *uê*…) |
| Consonne finale | facultative | **-m, -n, -ng, -nh** (nasales) ou **-p, -t, -c, -ch** (occlusives) ; ou semi-voyelles -i/-y, -o/-u |
| Ton | **obligatoire** | l'un des 6 tons |

- Pas d'enchaînement de consonnes (*str-*, *-pl*…) comme en français.
- L'inventaire des syllabes possibles est **fermé** : environ quelques
  milliers de combinaisons (ordre de grandeur à vérifier sur la base).
- La syllabe est l'**unité de base de la perception** et de la formation.

## 3. Les voyelles

**11 voyelles écrites** : a, ă, â, e, ê, i (y), o, ô, ơ, u, ư.

| Groupe | Voyelles | Notation | Remarque |
|---|---|---|---|
| Avant | i/y, ê, e | /i/, /e/, /ɛ/ | proches du français |
| Arrière arrondies | u, ô, o | /u/, /o/, /ɔ/ | proches du français |
| **Centrales** | **ư, ơ** | **/ɨ/, /ə/** | absentes du français (autre notation courante : /ɯ/, /ɤ/) |
| **Brèves** | **ă, â** | **/ă/, /ə̆/** | ă = *a* bref ; â = *ơ* bref ; la **durée** distingue les mots |
| Basse | a | /a/ | proche du français |

- **Diphtongues** (ai, ao, au, ay, ây, âu, êu, oi, ôi, ơi, ui, ưi, ưu…) et
  **noyaux à glissement** (iê/ia, uô/ua, ươ/ưa) : la qualité de chaque
  partie doit être tenue.
- **Triphtongues** (iêu, oai, oay, uây, uôi, ươi, ươu, uyu…) : séquences
  longues, inventaire de 84 unités dans `phonemes.csv`.

> **Correction** : la table `pedagogical_groups.csv` des archives qualifie
> ă et â de « voyelles longues ». Ce sont au contraire les deux voyelles
> **brèves** du vietnamien (DEC-0005).

## 4. Les consonnes

### 4.1 Consonnes initiales (prononciation de Hanoï)

| Lettre(s) | Son | Remarque |
|---|---|---|
| b, đ | /ɓ/, /ɗ/ | précédées d'une légère fermeture de la gorge (« implosives ») ; **đ** est le *d* du français |
| d, gi, r | /z/ | les trois se prononcent **pareil** à Hanoï (voir 4.3) |
| ph | /f/ | |
| th | /tʰ/ | *t* suivi d'un souffle ; distinct de **t** /t/ |
| kh | /x/ | comme la *jota* espagnole |
| c, k, q(u) | /k/ (/kw/ pour qu) | trois écritures pour le même son |
| g, gh | /ɣ/ | son « r grasseyé doux » ; *gh* devant i, e, ê |
| ng, ngh | /ŋ/ | comme *-ng* de *parking*, **aussi en début de mot** |
| nh | /ɲ/ | comme *gn* de *agneau* |
| ch, tr | /c/ ~ /tɕ/ | proche de *tch* ; voir 4.3 |
| x, s | /s/ | voir 4.3 |
| h, l, m, n, p, t, v | comme en français (p rare en début de mot) | |

### 4.2 Consonnes finales

- **-p, -t, -c, -ch** sont **non relâchées** : la bouche se ferme et **s'arrête**,
  sans bruit d'explosion (*một* [mot̚], *học* [hɔk̚]).
- **-ng** et **-nh** s'opposent à **-n** : *bản* ≠ *bảng*.
- Après o, ô, u, la finale **-ng** s'accompagne d'une fermeture des lèvres
  (*ông* [ʔəwŋ͡m]) — à vérifier dans la description de référence.

### 4.3 Sons confondus dans la prononciation de Hanoï

| Écriture | Prononciation courante à Hanoï | Prononciation distinguée |
|---|---|---|
| **tr / ch** | même son, ou très proches | tr rétroflexe /ʈ/ (Centre, Sud, prononciation soignée) |
| **s / x** | même son /s/ | s rétroflexe /ʂ/ (Centre, Sud, prononciation soignée) |
| **d / gi / r** | même son /z/ | r roulé ou /ʐ/ (Centre, Sud, prononciation soignée) |

> **Fait** : ces fusions sont décrites pour Hanoï, mais pas de façon uniforme
> selon les locuteurs et les sources (Kirby, 2011 ; synthèse Wikipédia,
> « Vietnamese phonology », dont les tableaux se contredisent en partie).

> **Règle** (DEC-0009) : la formation suit l'**accent courant de Hanoï**.
> tr/ch, s/x et d/gi/r se prononcent pareil ; leur distinction est un point
> d'**orthographe** à mémoriser, pas un exercice d'écoute. L'audio
> (voix natives ou de synthèse) suit cet accent.

## 5. L'écriture (chữ Quốc ngữ)

- Alphabet latin, mais **correspondances lettre-son propres** (tableau 4.1) :
  l'écrit induit le francophone en erreur.
- **Deux couches de signes** sur les voyelles :
  1. signes de **qualité** : ă, â, ê, ô, ơ, ư (et đ pour la consonne) ;
  2. signes de **ton** : ` ´ ̉ ~ ̣ (aucun signe = ngang).
  Une voyelle peut porter les deux : *ướ* = ư + ơ + ton sắc.
- Conséquence : l'écrit n'est **pas un point d'entrée fiable** ; sa place
  dans le Module 0 est à fixer dans FOND-04.

## 6. Rythme et prosodie

- **Vietnamien** : chaque syllabe est une unité pleine, avec son ton ; pas
  d'accent de mot ; les syllabes sont de durée comparable.
- **Français** : c'est la **prosodie** qui prime (DEC-0008). Le rythme est lui
  aussi régulier syllabe par syllabe, mais la **dernière syllabe de chaque
  groupe** est allongée, et la **mélodie de phrase** porte le sens (question,
  insistance). La hauteur de la voix ne change jamais le sens d'un mot.

> **Correction** : la synthèse des archives classe le français parmi les
> langues « à rythme accentuel » (*stress-timed*). Il est habituellement
> classé parmi les langues **à rythme syllabique**, comme le vietnamien ; la
> différence tient à l'allongement de fin de groupe et à la mélodie de phrase.

## 7. Grammaire : une langue isolante

| Propriété | Conséquence |
|---|---|
| Aucune conjugaison, déclinaison ni accord | les mots ne changent jamais de forme |
| **Ordre des mots** fixe (sujet – verbe – objet ; le qualifiant suit le nom) | l'ordre porte le sens |
| **Marqueurs** de temps et d'aspect : *đã* (accompli), *đang* (en cours), *sẽ* (futur), *rồi* (déjà) | ils remplacent la conjugaison |
| **Classificateurs** obligatoires avec les nombres et démonstratifs : *con*, *cái*, *chiếc*, *quả*, *người*… | *hai con mèo* = deux chats |
| **Particules finales** : *không ?*, *à*, *nhé*, *ạ*… | question, politesse, nuance |
| **Pronoms de parenté** : *anh, chị, em, ông, bà, cô, chú, bác*… | le pronom dépend de l'âge et de la relation ; pas d'équivalent neutre de « je / tu » |

## 8. Variétés régionales

La formation enseigne la **variété du Nord**. Principales différences avec
le Sud, à connaître pour comprendre :
- **5 tons** au Sud (hỏi et ngã confondus), 6 au Nord ;
- pas de glottalisation forte de nặng au Sud ;
- consonnes (tableau 4.3) et vocabulaire (*bát / chén* « bol »,
  *quả / trái* « fruit »…).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Fusion de la v3 et de la synthèse archivées ; corrections DEC-0005 et DEC-0008 ; vérifications sur Kirby (2011) et Brunelle (2009) : notation de ngã, hỏi à Hanoï, fusions de consonnes, rythme du français ; ajout des pronoms de parenté et des variétés régionales. |
| 0.2 | 2026-10-28 | § 4.3 : norme de l'accent courant de Hanoï (DEC-0009). |
| 1.0 | 2026-10-28 | Validé par Christophe (DEC-0014). |

## Liens

- **Entrées** : [01 — Intention et objectifs](01_intention_et_objectifs.md)
- **Sorties** :
  [03 — Difficultés des francophones](03_difficultes_francophones.md) ·
  [04 — Principes pédagogiques](04_principes_pedagogiques.md) ·
  [Registre des règles](../02_REGLES/REGISTRE_REGLES.md) ·
  `04_DONNEES/tons.csv` · `04_DONNEES/phonemes.csv`
