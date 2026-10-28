---
id: QUAL-PROP-MOTS-M0
titre: Proposition de mots supports du Module 0
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Proposition de 91 mots supports pour les 13 leçons d'apprentissage du
  Module 0, choisis automatiquement dans mots.csv selon les critères de
  R-LEX-03 et R-ATOM-05, avec les sons non couverts et des ajouts proposés
  hors corpus (à vérifier).
entrees: [DATA-MODELE, REG-REGLES]
sorties: [04_DONNEES/mots_lecons.csv (après validation)]
sources:
  - 04_DONNEES/mots.csv, syllabes.csv, ouvertures.csv, lecons.csv
---

# Proposition de mots supports du Module 0

## Méthode

Pour chaque leçon N, un mot est **candidat** s'il :
1. ne contient que des sons et tons ouverts en N ou avant (R-ATOM-03) ;
2. contient **au moins un** élément de la leçon N (R-ATOM-05) ;
3. n'en contient **qu'un seul** (R-LEX-03, critère 5 ; sauf L01) ;
4. a **1 ou 2 syllabes** (R-LEX-04).

Parmi les candidats, le choix privilégie : (a) les mots qui couvrent un
élément nouveau pas encore couvert ; (b) les mots déjà marqués supports dans
les archives ; (c) les mots d'une syllabe ; (d) les plus fréquents.
Quotas : 10 mots en L01 (21 nouveautés), 7 ailleurs → **91 mots** (≤ 100,
R-LEX-02). L14 (recyclage) n'a pas de mots propres.

## Proposition

| Leçon | Famille | Nb | Mots proposés | Éléments non couverts | Ajouts proposés hors corpus (à vérifier) |
|---|---|---|---|---|---|
| L01 | Sons proches du français + ton ngang | 10 | *va li* (valise), *nên* (donc), *xem* (regarder), *to* (grand), *môn* (matière (scolaire)), *ra* (sortir), *đi* (aller), *ba* (trois), *ho* (tousser), *pin* (pile (batterie)) | u | tu (pratiquer une religion) — à défaut |
| L02 | Tons sắc et huyền | 7 | *là* (être), *nó* (il/elle), *về* (rentrer), *bé* (petit(e)), *bán* (vendre), *bàn* (table), *à* (préposition (à, vers, pour)) | — | — |
| L03 | Ton nặng (opposé à huyền) | 4 | *bạn* (ami(e)), *họ* (ils/elles), *mẹ* (mère), *hẹn* (rendez-vous) | — | dạ (oui, poli), bị (marque du passif), lạ (étrange) |
| L04 | Diphtongues | 7 | *tôi* (je), *nói* (parler), *hai* (deux), *sao* (étoile), *tuy* (bien que, quoique), *vui* (joyeux), *mèo* (chat) | iu, eo couvert ; iu (dịu disponible en remplacement) | — |
| L05 | Consonnes complexes (c, ph, th, qu) | 7 | *có* (avoir), *quá* (trop), *thôi* (c'est tout), *con* (enfant), *cá* (poisson), *cái* (classificateur (objets)), *quý* (précieux) | ph | pha (mélanger, préparer : *pha cà phê*) |
| L06 | Voyelles centrales (ơ, ư) et leurs diphtongues | 7 | *mới* (nouveau/nouvelle), *lưu* (conserver, circuler), *cơm* (riz cuit), *nếu* (si), *với* (avec), *giờ* (heure), *vợ* (femme (épouse)) | ư (seule), ơu, ưi | thư (lettre), tư (quatre, privé) |
| L07 | Ton hỏi (opposé à huyền, puis à nặng) | 7 | *phở* (pho (soupe de nouilles)), *ở* (habiter), *phải* (devoir), *hỏi* (poser une question), *mở* (ouvrir), *giỏi* (habile), *rẻ* (pas cher) | — | — |
| L08 | Finales non relâchées (-p, -t, -c, -ch) | 7 | *học* (étudier), *tốt* (bien), *thích* (aimer), *giúp* (aider), *ít* (peu), *phút* (minute), *tết* (Têt (Nouvel An vietnamien)) | — | — |
| L09 | Voyelles brèves (ă, â) et leurs diphtongues | 7 | *năm* (cinq), *rất* (très), *đây* (ici), *tay* (main), *đâu* (où), *đau* (avoir mal), *thấy* (voir) | — | — |
| L10 | Consonnes difficiles (ng, nh, ch, kh, g) et finales -ng, -nh | 7 | *ông* (grand-père), *nhà* (maison), *trên* (sur), *anh* (grand frère / homme adulte (pronom)), *nghe* (écouter), *gà* (poulet), *khi* (quand) | — | — |
| L11 | Ton ngã (opposé à sắc) et contraste hỏi / ngã | 7 | *cũng* (aussi), *nghĩ* (penser), *mỗi* (chaque), *dễ* (facile), *lẽ* (raison), *cũ* (vieux), *mũi* (nez) | — | — |
| L12 | Noyaux à glissement (iê, uô, ươ, oa…) | 7 | *nước* (eau), *biết* (savoir), *muốn* (vouloir), *hoa* (fleur), *chuyên* (spécialisé, expert), *khỏe* (en bonne santé), *hoặc* (ou) | uơ, uê, uâ | — |
| L13 | Triphtongues | 7 | *người* (personne), *ngoài* (en dehors de), *yêu* (aimer), *rượu* (alcool), *muối* (sel), *tiêu* (poivre), *mười* (dix) | oeo, uyu, oao, uây, oay | — |

## Remarques

- Les éléments non couverts de L12 et L13 (*uơ, uê, uâ, oeo, uyu, oao,
  uây, oay*) sont **rares** : à couvrir par des syllabes d'exercice ou des
  mots ajoutés plus tard.
- Les ajouts hors corpus sont des mots courants selon mes connaissances ;
  ils sont **à vérifier** (sens, fréquence) avant d'entrer dans `mots.csv`.
- *à* (L02) est surtout une particule à l'oral (voir le rapport de reprise).

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |
