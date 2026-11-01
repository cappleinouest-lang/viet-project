---
id: QUAL-ESSAI-ULTRA-20261031
titre: Essai de FPT.TTS-ultra avec les voix du Nord
statut: VALIDE
version: 1.5
date: 2026-10-31
resume: >
  Compare les 4 voix « Nord » de FPT.TTS-ultra (Ban Mai, Viet Khoa, Minh Quang,
  Quang Anh) aux voix actuelles du projet (Ban Mai en FPT.TTS-pro, Huy Phong en
  FPT.AI-VITs), sur le contraste des tons (même méthode que
  QUAL-CONTRASTE-TONS-20261030) et sur l'accent, à l'écoute.
entrees: [REG-DEC, PROD-AUDIO, QUAL-CONTRASTE-TONS-20261030]
sorties: []
sources:
  - 04_DONNEES/audio/_essais/ultra/*-U1..U4-normal.mp3, script 05_PRODUCTION/tools/essai_ultra.py
  - 04_DONNEES/audio/*-F1-normal.mp3, *-H4-normal.mp3 (références)
  - écoute de Christophe (page 04_DONNEES/audio/_essais/ultra/ecoute.html), 2026-10-31
---

# Essai de FPT.TTS-ultra avec les voix du Nord

## Résumé

Sur le contraste des tons, **les 4 voix Ultra font nettement moins bien** que
les voix actuelles (contraste 1,70 à 2,34, contre environ 4). À l'écoute,
**Minh Quang (Ultra) n'a pas vraiment l'accent du Nord**, bien que la
marketplace l'annonce « Nord » ; Ban Mai, Viet Khoa et Quang Anh (Ultra) ont
bien l'accent du Nord. Les 3 autres voix de l'API (Xuan Toan, Phuong An,
Kim Ngan) n'ont **pas** l'accent du Nord. Recommandation : garder Ban Mai (FPT.TTS-pro) et
Huy Phong (FPT.AI-VITs) pour les leçons de sons et de tons ; réévaluer Ultra
plus tard pour des phrases et dialogues.

## Le modèle FPT.TTS-ultra (fiche de la marketplace)

- Synthèse « basée sur LLM », 24 kHz ; trois modes : *auto* (voix par défaut),
  *clone* (imitation d'un échantillon audio), *design* (voix décrite par des
  attributs : genre, âge, hauteur, accent étranger, chuchotement).
- Aucun attribut d'accent vietnamien (Nord / Sud) en mode *design*.
- L'interface propose 4 voix « Nord » : Ban Mai, Viet Khoa, Minh Quang, Quang Anh.
- Identifiants API acceptés (sonde du 2026-10-31) : `std_banmai`,
  `std_vietkhoa`, `std_minhquang`, `std_quanganh`. L'API connaît d'autres voix
  : `fci_xuantoan`, `fci_phuongan`, `std_kimngan` (7 voix en tout), pas
  l'accent du Nord à l'écoute (test d'accent ci-dessous).
- Huy Phong n'existe pas en Ultra.

## Méthode

- Mêmes 36 mots que QUAL-CONTRASTE-TONS-20261030 (6 par ton), débit normal,
  plus 10 syllabes d'accent (*ra, rau, da, dê, gia, gì, sa, xa, tra, cha*).
- Mot seul (pas de doublement), volume égalisé par `decoupe_audio.py`.
- Mesure de `tester_voix_tons.py` (reconnus, contraste, paires difficiles,
  silence avant le mot, durée de la consonne de début).
- Accent jugé à l'écoute par Christophe.

## Résultats

| Voix | Reconnus | Contraste | sắc / ngã | hỏi / nặng | huyền / nặng | huyền / hỏi | Silence | Consonne |
|---|---|---|---|---|---|---|---|---|
| Huy Phong (H4, VITs, actuel) | **81 %** | **4,07** | 2,11 | 2,06 | 1,70 | 0,95 | 40 ms | 32 ms |
| Ban Mai (F1, TTS-pro, actuelle) | 78 % | 4,00 | **3,23** | **2,55** | **1,99** | 1,08 | 88 ms | 79 ms |
| Ban Mai (Ultra) | 64 % | 2,34 | 2,02 | 1,93 | 0,61 | 1,90 | 216 ms | 141 ms |
| Quang Anh (Ultra) | 74 % | 2,22 | 1,02 | 2,06 | 0,98 | 1,46 | 237 ms | 75 ms |
| Viet Khoa (Ultra) | 46 % | 1,98 | 2,52 | 2,15 | 1,17 | 1,27 | 236 ms | 387 ms |
| Minh Quang (Ultra) | 50 % | 1,70 | 1,34 | 1,98 | 0,66 | **1,99** | 268 ms | 258 ms |

Accent à l'écoute (Christophe) :

| Voix Ultra | Accent du Nord |
|---|---|
| Ban Mai | oui ; **début des mots plus précis** qu'en FPT.TTS-pro (écoute de Christophe) |
| Viet Khoa | oui ; **parle trop vite** (écoute de Christophe) |
| Quang Anh | oui |
| Minh Quang | **non, pas vraiment** (malgré l'étiquette « Nord » de la marketplace) |

Test d'accent Nord / Sud (`essai_ultra.py --accent`, 15 mots et phrases
choisis pour séparer les accents : r-/d-/gi-, v-, s-/x-, tr-/ch-, finales
-n/-t, hỏi/ngã ; page `04_DONNEES/audio/_essais/ultra/accent/accent.html`) :

| Voix Ultra | Identifiant | Accent du Nord |
|---|---|---|
| Ban Mai (référence) | `std_banmai` | oui |
| Xuan Toan | `fci_xuantoan` | **non** |
| Phuong An | `fci_phuongan` | **non** |
| Kim Ngan | `std_kimngan` | **non** |

## Lecture

- **Fait mesuré** : contraste des tons environ deux fois plus faible en Ultra.
  *huyền / nặng* très proche chez Ban Mai Ultra (0,61) et Minh Quang Ultra (0,66).
- **Fait mesuré** : en Ultra, le début de mot n'est pas tronqué, mais le
  silence avant le mot est long (plus de 200 ms) ; facile à raccourcir.
  Consonne de Viet Khoa anormalement longue (387 ms) : souffle ou bruit
  possible, à vérifier à l'écoute.
- **Fait constaté (écoute)** : Ban Mai (Ultra) attaque le début des mots avec
  plus de précision que Ban Mai (FPT.TTS-pro) ; cohérent avec la mesure
  (consonne de début 141 ms contre 79 ms). Contrepartie : tons moins
  contrastés (2,34 contre 4,00 ; *huyền / nặng* 0,61).
- **Fait constaté (écoute)** : Viet Khoa (Ultra) parle trop vite au débit
  normal (vitesse 1,0 envoyée).
- **Fait constaté (essai_espacement.py, 2026-10-31)** : **FPT.TTS-ultra ignore
  le paramètre de vitesse** : à 0,75, les phrases ne sont pas ralenties. Ultra
  ne peut donc pas fournir de version lente sans traitement après coup.
- **Fait constaté (écoute)** : pour des phrases, les versions « mots
  espacés » obtenues par la ponctuation (virgules, points de suspension,
  points) sonnent hachées, toutes voix confondues ; essai non concluant.
- **Fait constaté** : l'étiquette de région de la marketplace ne suffit pas
  (Minh Quang Ultra ; déjà Thu Minh, DEC-0066). Chaque voix est à vérifier à l'écoute.
- **Fait constaté (écoute)** : Huy Phong (H4, FPT.AI-VITs) a quelquefois un
  son « numérique » (artefact de synthèse). Mots concernés et origine
  (synthèse FPT ou traitement du projet) à préciser.
- **Hypothèse** : Ultra, conçu pour des phrases expressives, est moins adapté
  aux mots isolés ; un autre tirage pourrait donner des chiffres un peu différents.
- **Limite** : 6 mots par ton, une seule génération par voix.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026-10-31 | Création. |
| 1.1 | 2026-10-31 | Viet Khoa (Ultra) : débit trop rapide à l'écoute. |
| 1.2 | 2026-10-31 | Ban Mai (Ultra) : début des mots plus précis à l'écoute. |
| 1.3 | 2026-10-31 | Huy Phong (H4) : son numérique par moments. |
| 1.4 | 2026-10-31 | Test d'accent : Xuan Toan, Phuong An, Kim Ngan pas du Nord. |
| 1.5 | 2026-10-31 | Ultra ignore la vitesse ; phrases espacées par ponctuation hachées. |
