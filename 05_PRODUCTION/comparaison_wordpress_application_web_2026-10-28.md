---
id: PROD-COMP-SUPPORT-20261028
titre: Comparaison WordPress / application web sur mesure
statut: BROUILLON
version: 0.1
date: 2026-10-28
resume: >
  Compare l'enveloppe retenue par DEC-0015 et DEC-0016 (WordPress) à une
  application web sur mesure sans WordPress, sur les exigences du dossier de
  choix du support. Conclut que le lecteur d'activités et la page de
  prononciation sont identiques dans toutes les options, et propose une
  décision DEC-0030 à valider.
entrees: []
sorties: []
sources:
  - 05_PRODUCTION/dossier_choix_support_2026-10-28.md (exigences EX-01 à EX-28)
  - 02_REGLES/DECISIONS.md (DEC-0015, DEC-0016, DEC-0017)
  - 05_PRODUCTION/01_architecture_outils.md (PROD-ARCH)
  - Recherches web du 2026-10-28 (liste en fin de document)
---

# Comparaison WordPress / application web sur mesure

## Résumé

**Constat principal** : dans toutes les options, l'essentiel du travail est
le même, à savoir le **lecteur d'activités** (E1 → E5, scores, verrous) et
la **page de prononciation** (micro, courbe mélodique). Ce sont des
programmes qui tournent **dans le navigateur** (JavaScript), quel que soit
l'hébergement. Le choix ne porte donc que sur l'**enveloppe** : où le site
est hébergé, comment l'élève a un compte, où sa progression est enregistrée.

**Recommandation** : une **application web statique** (fichiers générés
depuis `04_DONNEES`, suivis par Git, hébergés gratuitement), avec la
progression **synchronisée par un service de comptes gratuit** (Firebase).
WordPress reste possible plus tard, car le lecteur est écrit indépendamment
de l'enveloppe. Décision proposée : DEC-0030 (§ 6), **à valider par
Christophe**.

## 1. Les options comparées

| Code | Option | Où est la progression |
|---|---|---|
| **W** | WordPress + lecteur + petite extension de progression (**décision actuelle**, DEC-0016) | Base de données WordPress, sur le compte de l'élève |
| **S1** | Application web **statique**, sans compte | Dans le navigateur de chaque appareil ; transfert par fichier d'export / import |
| **S2** | Application web **statique** + service de comptes **Firebase** (Google) | Base Firebase, sur le compte de l'élève |

> **Application web statique** : un ensemble de fichiers (pages, JavaScript,
> audio, images) que le serveur se contente d'envoyer, sans programme côté
> serveur. Elle peut être installée sur l'écran d'accueil du téléphone comme
> une application (« PWA ») et fonctionner sans réseau.

Option écartée d'emblée : **Supabase** (équivalent de Firebase). Son offre
gratuite **met le projet en pause après une semaine d'inactivité** (fait,
source 1). Une pause de l'élève (vacances, maladie) bloquerait alors l'accès
à sa progression.

## 2. Ce qui est identique dans toutes les options

| Élément | Commentaire |
|---|---|
| Lecteur d'activités E1 → E5, scores, verrous, volets | Même code JavaScript |
| Page de prononciation (micro, courbe mélodique) | Même code. Exige **https** (EX-23) : fourni dans les trois options |
| Anki pour les révisions (DEC-0015) | Paquet proposé au téléchargement quand la leçon est validée, dans les trois options |
| Génération depuis `04_DONNEES` (DEC-0017) | Même générateur ; seule la sortie diffère (voir § 3, EX-26) |

## 3. Comparaison sur les critères qui les départagent

✔ = répond bien · ~ = répond avec une contrainte · ✘ = ne répond pas

| Critère | W — WordPress | S1 — Statique sans compte | S2 — Statique + Firebase |
|---|---|---|---|
| **EX-01** Partage avec d'autres apprenants | ✔ inscriptions intégrées | ~ chacun garde sa progression sur son appareil | ✔ comptes (e-mail ou Google) |
| **EX-02** PC, Android, iPhone, navigateur | ✔ | ✔ | ✔ |
| **EX-03** Même progression sur tous les appareils | ✔ | ✘ export / import manuel | ✔ |
| **EX-04** Coût annuel | ~ hébergement mutualisé : environ **2 à 7 € par mois** selon l'offre (source 2), plus un nom de domaine | ✔ **0 €** (hébergeur gratuit, adresse fournie) | ✔ **0 €** dans les quotas gratuits (source 3), largement suffisants ici |
| **EX-26** Contenus regénérables, suivis par Git | ~ les pages vivent dans la base WordPress, **hors Git** ; il faut un script qui les pousse dans WordPress | ✔ tout est fichier, regénéré et versionné | ✔ idem ; seule la progression des élèves est hors Git, ce qui est normal |
| **EX-27** Neutralité (couche d'adaptation seule) | ✔ | ✔ | ✔ |
| **Entretien** | ✘ mises à jour régulières de WordPress, de PHP et des extensions ; cible fréquente d'attaques | ✔ rien à mettre à jour côté serveur | ✔ presque rien ; règles d'accès Firebase à écrire une fois |
| **Hors connexion** (non exigé, mais utile au téléphone) | ✘ difficile | ✔ | ✔ (Firestore garde une copie locale et synchronise ensuite) |
| **Dépendance** | Hébergeur (remplaçable) | Aucune | **Google** ; changement de service possible si la progression est isolée derrière une interface |
| **Données personnelles** (au moment du partage) | Chez votre hébergeur | Chez l'élève | Chez Google ; à mentionner aux élèves |
| **Travail de développement en plus du lecteur** | Extension en PHP + script de publication des pages | Export / import | Connexion et enregistrement Firebase (JavaScript) |

## 4. Points de vigilance communs

- **iPhone** : Safari sait enregistrer le micro depuis iOS 14.3 (format AAC
  dans un conteneur MP4, différent d'Android et du PC) (fait, source 4). La
  courbe mélodique peut être calculée directement sur le son du micro, sans
  passer par un fichier : le format ne devrait donc pas gêner
  (**hypothèse**, à tester sur un iPhone).
- **Anki sur iPhone** : AnkiMobile coûte environ **25 $** (achat unique,
  jusqu'à 5 appareils) ; Anki est gratuit sur PC, Android et AnkiWeb (fait,
  source 5). À signaler aux futurs élèves sur iPhone.
- **Quotas Firebase** : si un quota gratuit est dépassé, le service s'arrête
  jusqu'au lendemain (ou au mois suivant), il n'est pas facturé (source 3).
  Ordre de grandeur pour ce projet : quelques centaines d'écritures par jour
  et par élève, pour 20 000 permises (**estimation**).

## 5. Raisonnement

1. **W** apporte surtout des comptes et des pages « toutes faites ». Or les
   pages de la formation sont **générées** depuis les données (DOC-03,
   DEC-0017) : les ranger dans une base WordPress les sort de Git et ajoute
   une étape de publication. WordPress demande aussi un entretien continu,
   pour un gain limité tant que l'élève est seul.
2. **S1** est la plus simple, mais échoue sur **EX-03** : vous pratiquerez
   sur PC et sur téléphone.
3. **S2** remplit toutes les exigences, sans coût ni serveur à entretenir.
   Son seul défaut est la dépendance à Google. On la limite en isolant
   l'enregistrement de la progression dans une **seule partie du code**
   (une « interface »), qu'on peut rebrancher sur WordPress ou un autre
   service si besoin.
4. **Ordre de développement sans regret** : le lecteur d'activités peut être
   construit et testé **d'abord en S1** (progression locale), puis relié à
   Firebase. Rien n'est perdu si l'on revient à WordPress.

## 6. Décision proposée (à valider)

> **DEC-0030 — Enveloppe de la formation : application web statique et
> Firebase** (remplace DEC-0016 ; précise DEC-0015 pour l'apprentissage ;
> Anki inchangé pour les révisions)
>
> - Site **statique** généré depuis `04_DONNEES`, suivi par Git, hébergé
>   gratuitement en https ; installable sur téléphone (PWA).
> - **Lecteur d'activités** et **page de prononciation** écrits
>   indépendamment de l'hébergement.
> - **Progression** : d'abord dans l'appareil (développement et essais),
>   puis synchronisée par **Firebase** (comptes, une seule progression sur
>   tous les appareils), derrière une interface remplaçable.
> - **WordPress** : abandonné pour l'instant ; réexamen si le partage exige
>   des fonctions qu'il apporte (paiement, forum, gestion de groupes).

## 7. Questions à trancher par Christophe

1. Valider, modifier ou refuser DEC-0030.
2. Avez-vous une raison de tenir à WordPress qui n'apparaît pas dans les
   documents (habitude, site existant, projet de vente de la formation) ?
3. Acceptez-vous que la progression des élèves soit enregistrée chez Google
   (Firebase) ?

## Sources

1. Supabase, limites de l'offre gratuite (pause après une semaine
   d'inactivité) : https://automationatlas.io/answers/supabase-free-tier-limits-2026/
2. Comparatif d'hébergements WordPress, prix d'entrée (codeur.com, mai
   2026) : https://www.codeur.com/comparatif/hebergement-wordpress
3. Firebase, offre gratuite Spark (quotas, pas de mise en pause) :
   https://omidsaffari.com/blog/firebase-pricing ; page officielle :
   https://firebase.google.com/pricing
4. WebKit, MediaRecorder dans Safari : https://webkit.org/blog/11353/mediarecorder-api/
5. Anki, prix d'AnkiMobile : https://docs.ankiweb.net/faqs/why-does-ankimobile-cost-more-than-a-typical-mobile-app

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1 | 2026-10-28 | Création. |

## Liens

- **Entrées** : [Dossier de choix du support](dossier_choix_support_2026-10-28.md) ·
  [Journal des décisions](../02_REGLES/DECISIONS.md) ·
  [Architecture des outils](01_architecture_outils.md)
- **Sorties** : DEC-0030 si elle est validée
