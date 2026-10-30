/*
 * ============================================================================
 * LECTEUR D'ACTIVITÉS — PROGRAMME (lecteur.js)
 * Vietnamien, Module 0, volet écoute : E1 Découvrir → échauffement → E2 → E3 → écrit
 * Volet production : E4 Répéter (micro, courbe mélodique : prononciation.js)
 * ============================================================================
 *
 * À QUOI SERT CE FICHIER
 *   Il fabrique tous les écrans dans la zone <main id="app"> de index.html,
 *   joue les sons, note les réponses, calcule les scores et ouvre les étapes
 *   (verrous). Il ne contient AUCUN contenu pédagogique : leçons, séries,
 *   sons, mots et audios arrivent tout faits dans window.DONNEES_LECTEUR,
 *   produit par 05_PRODUCTION/tools/generer_lecteur.py à partir de 04_DONNEES.
 *   → Pour changer un mot, une série, un seuil de leçon : modifier 04_DONNEES
 *     puis regénérer, jamais ce fichier.
 *
 * PLAN DU FICHIER (chercher le titre « ---------- … ---------- »)
 *    1. Enregistrement de la progression (Stockage, migration, réglages)
 *    2. Outils (fabriquer un élément, tirer au hasard…)
 *    3. Audio (fichier ou voix de synthèse)
 *    4. Affichage d'un terme (symbole, image, repère, place dans le mot)
 *    5. Calcul des scores et des verrous
 *    6. Écran : accueil (liste des leçons)
 *    7. Écran : une leçon (parties, étapes, boutons)
 *    8. Écran : E1 Découvrir
 *    9. Écran : échauffement « Pareil ou différent ? »
 *   10. Écran : E2 et E3 « Lequel ? »
 *   10 bis. Écran : « Combien de fois ? » (fin d'E3)
 *   11. Écran : l'écrit (fin d'E3)
 *   11 bis. Écran : E4 Répéter (volet production)
 *   11 ter. Écran : Les 6 tons (référence, schéma de chaque ton)
 *   12. Écran : réglages
 *   13. Écran : mes progrès
 *   14. Démarrage
 *
 * VOCABULAIRE UTILISÉ DANS LE CODE
 *   leçon (l)    : { code 'M0-L01', numero, titre, seuil (0.85), tons (vrai/faux),
 *                    series [...], parties [...], decouverte {...} }
 *   partie (pa)  : { code 'A' | 'B' | 'U' (unique), titre, series [codes], elements [codes] }
 *   série (s)    : { code 'S0001', place 'debut'|'fin'|'voyelle'|'ton', termes [...] }
 *   terme (t)    : un mot ou une syllabe : { ecrit, sens, invente, image, symbole, audio }
 *   symbole      : { texte '/ɛ/', categorie 'identique'|'proche'|'nouveau', place, repere, indication }
 *   debit        : 'slow' (lent) ou 'normal' ; dans l'état d'une étape, c'est la PHASE
 *                  (phase 1 = 'slow' = images + symboles ; phase 2 = 'normal' = symboles seuls)
 *   voix         : code 'F1', 'F3', 'H3', 'H4' (voix actives de voix.csv) ; l.voix = voix d'écoute de la leçon (DEC-0055)
 *   cle          : 'e2' ou 'e3' (quelle étape « Lequel ? »)
 *   pc           : code de la partie ('A', 'B' ou 'U')
 *
 * MODIFICATIONS COURANTES : OÙ REGARDER
 *   - un texte affiché (consigne, bouton)      → chercher le texte entre apostrophes ;
 *   - le nombre de paires de l'échauffement    → NB_PAIRES_ECHAUFFEMENT ;
 *   - les seuils, 20 réponses, 2 voix…         → PARAMETRES dans generer_lecteur.py ;
 *   - ce qu'il faut écouter (début/fin…)       → PLACES ;
 *   - la couleur, la taille                    → lecteur.css ;
 *   - passer à WordPress ou Firebase           → l'objet Stockage, et lui seul.
 *
 * PRÉCAUTIONS
 *   - Ne pas écrire de balise fermante de script dans ce fichier, même en
 *     commentaire : le générateur l'insère dans lecteur_autonome.html.
 *   - nomAccessible() sert aux essais automatiques : ne pas changer son texte.
 *   - Après une modification : regénérer, ouvrir 06_LIVRABLES/lecteur/index.html,
 *     et parcourir au moins une leçon de sons (L01) et une leçon de tons (L02).
 *
 * Règles appliquées : PROG-ACT, R-PARC-01 à 05, R-ECR-01/02, R-LEX-06, R-VOL-02/05 à 07,
 * DEC-0028/0029 (étiquettes), DEC-0032 (minimum par série), DEC-0033 (positions 1 et 2 en E2),
 * DEC-0037 (leçon en deux parties), DEC-0039 (E1 un son à la fois), DEC-0041 (échauffement),
 * DEC-0042 (place du son), DEC-0043 et DEC-0045 (leçons de tons), DEC-0049 et DEC-0050 (E4),
 * DEC-0051 (mode essai : tout ouvert), DEC-0052 et DEC-0053 (page « Les 6 tons », schémas),
 * DEC-0054 (« Combien de fois ? »), DEC-0055 (voix d'écoute par leçon).
 * Description complète : 05_PRODUCTION/04_analyse_fonctionnelle_lecteur.md (PROD-AF-LECT).
 */
// Tout le programme est enfermé dans une fonction qui s'exécute aussitôt :
// ses variables ne se mélangent pas avec celles de la page.
(function () {
  // Mode strict : le navigateur signale plus d'erreurs (variable mal orthographiée…).
  'use strict';

  // Raccourcis : D = toutes les données générées ; P = paramètres des verrous ;
  // puis les zones de la page (voir les id dans index.html).
  var D = window.DONNEES_LECTEUR;
  var P = D.parametres;
  var app = document.getElementById('app');
  var titreBarre = document.getElementById('barre-titre');
  var btnRetour = document.getElementById('btn-retour');
  var bandeau = document.getElementById('bandeau-voix');
  var pied = document.getElementById('pied');

  /* ---------- 1. Enregistrement de la progression (seul endroit à remplacer
     pour passer à WordPress ou Firebase : DEC-0030) ---------- */
  // Nom sous lequel la progression est rangée dans le navigateur (localStorage).
  // Le changer revient à repartir de zéro pour tout le monde.
  var CLE = 'viet-lecteur-progression-v1';
  var memoire = null;
  var Stockage = {
    // charger() : lit la progression enregistrée (texte JSON) ; si rien ou si le
    // navigateur refuse (navigation privée…), repart d'une progression vide.
    charger: function () {
      try {
        var t = window.localStorage.getItem(CLE);
        if (t) return JSON.parse(t);
      } catch (e) { /* stockage indisponible : on garde la progression en mémoire */ }
      return memoire || { version: 2, lecons: {} };
    },
    // enregistrer(p) : garde p en mémoire et l'écrit dans le navigateur.
    // Pour WordPress ou Firebase : remplacer le corps de ces deux fonctions par
    // un envoi / une lecture sur le compte de l'apprenant (DEC-0030).
    enregistrer: function (p) {
      memoire = p;
      try { window.localStorage.setItem(CLE, JSON.stringify(p)); } catch (e) { /* idem */ }
    }
  // (Fin de l'objet Stockage.)
  };

  // Retrouve une leçon par son code ('M0-L01').
  function trouverLecon(code) { return D.lecons.filter(function (l) { return l.code === code; })[0]; }
  // Séries d'une leçon qui appartiennent à une partie (A, B ou U).
  function seriesDe(l, partie) {
    return l.series.filter(function (s) { return partie.series.indexOf(s.code) >= 0; });
  }
  // État vide d'une étape E2 ou E3 :
  //   debit    : phase en cours, 'slow' (phase 1) puis 'normal' (phase 2)
  //   hist     : toutes les réponses { s: série, ok: juste ?, v: voix, d: phase, t: heure,
  //              c: n° du terme attendu, r: n° du terme choisi }
  //   reussites: nombre de bonnes réponses par série, en phase 2 (DEC-0032)
  //   validee  : étape validée ; echauffe (ajouté plus tard) : échauffement fait
  // État vide d'une partie : sons vus en E1, E2, E3, écrit vu.
  function etatEtape() { return { debit: 'slow', hist: [], reussites: {}, validee: false }; }
  function etatPartieNeuf() { return { e1: { vues: [] }, e2: etatEtape(), e3: etatEtape(), ecrit: false }; }

  // MIGRATION : convertit une progression enregistrée avec une ancienne version
  // du lecteur. À compléter (et à monter le numéro de version) si la forme de
  // l'état change un jour.
  // Version 1 (une leçon = un seul bloc) -> version 2 (une leçon = une ou plusieurs parties).
  function migrer(p) {
    if (p.version === 2) return p;
    Object.keys(p.lecons || {}).forEach(function (code) {
      var ancien = p.lecons[code];
      var l = trouverLecon(code);
      if (!l || ancien.parties) return;
      var neuf = { parties: {}, ecouteValideeLe: ancien.ecouteValideeLe || null };
      l.parties.forEach(function (pa) {
        var dans = function (s) { return pa.series.indexOf(s) >= 0; };
        var copie = function (e) {
          var r = {};
          Object.keys(e.reussites || {}).forEach(function (s) { if (dans(s)) r[s] = e.reussites[s]; });
          return { debit: e.debit, hist: (e.hist || []).filter(function (h) { return dans(h.s); }), reussites: r, validee: !!e.validee };
        };
        neuf.parties[pa.code] = {
          e1: { vues: (ancien.e1 && ancien.e1.vues || []).filter(dans) },
          e2: copie(ancien.e2 || etatEtape()), e3: copie(ancien.e3 || etatEtape()),
          ecrit: !!ancien.ecrit
        };
      });
      p.lecons[code] = neuf;
    });
    p.version = 2;
    return p;
  }
  // prog = TOUTE la progression de l'apprenant, chargée au démarrage :
  //   { version: 2, lecons: { 'M0-L01': { parties: { A: {...}, B: {...} }, ecouteValideeLe: '2026-10-29' } },
  //     reglages: {...} }
  // On la modifie en mémoire puis on appelle sauver().
  var prog = migrer(Stockage.charger());
  // Réglages par défaut (écran Réglages). Ajouter un réglage : l'ajouter ici,
  // puis une ligne dans ecranReglages().
  var REGLAGES_DEFAUT = { vitesse: 1, suivantAuto: false, aides: true, grandTexte: false, infoTest: true, toutOuvert: true };
  function reglages() {
    prog.reglages = prog.reglages || {};
    Object.keys(REGLAGES_DEFAUT).forEach(function (k) { if (prog.reglages[k] === undefined) prog.reglages[k] = REGLAGES_DEFAUT[k]; });
    return prog.reglages;
  }
  // Applique le réglage « Grand texte » (classe sur la balise html, voir lecteur.css).
  // MODE ESSAI (DEC-0051) : toutes les leçons et toutes les étapes ouvertes, sans verrou.
  // Activé par défaut pendant la phase de test ; à couper dans Réglages pour retrouver les verrous.
  // Les scores et validations restent calculés normalement.
  function toutOuvert() { return !!reglages().toutOuvert; }
  function appliquerReglages() { document.documentElement.classList.toggle('grand-texte', !!reglages().grandTexte); }
  appliquerReglages();

  // Accès à l'état d'une leçon ou d'une partie ; le crée vide s'il n'existe pas encore.
  function etatLecon(code) {
    if (!prog.lecons[code]) prog.lecons[code] = { parties: {}, ecouteValideeLe: null };
    return prog.lecons[code];
  }
  function etatPartie(code, pc) {
    var e = etatLecon(code);
    if (!e.parties[pc]) e.parties[pc] = etatPartieNeuf();
    return e.parties[pc];
  }
  // Enregistre toute la progression. À appeler après chaque changement d'état.
  function sauver() { Stockage.enregistrer(prog); }

  /* ---------- 2. Outils ---------- */
  // Fabrique un élément de la page. Exemple :
  //   el('button', { class: 'bouton', text: 'OK', onclick: f })  →  <button class="bouton">OK</button>
  // attrs : 'class', 'text' (texte affiché), 'onclick'… (actions), sinon attributs HTML
  //         (une valeur false ou null n'est pas posée ; true pose l'attribut vide, ex. hidden).
  // enfants : liste d'éléments ou de textes à placer dedans (les null sont ignorés).
  function el(tag, attrs, enfants) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') n.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== false && attrs[k] != null) n.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
    });
    (enfants || []).forEach(function (c) { if (c) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return n;
  }
  // Efface l'écran courant et remonte en haut de la page (avant d'afficher un nouvel écran).
  function vider() { app.innerHTML = ''; window.scrollTo(0, 0); }
  // hasard(n) : entier au hasard de 0 à n-1. melanger(t) : copie de t dans un ordre au hasard.
  function hasard(n) { return Math.floor(Math.random() * n); }
  function melanger(t) { t = t.slice(); for (var i = t.length - 1; i > 0; i--) { var j = hasard(i + 1); var x = t[i]; t[i] = t[j]; t[j] = x; } return t; }
  function pourcent(x) { return Math.round(x * 100) + ' %'; }
  // Textes de titres : « Partie A · Voyelles » et « Leçon 1A · E1 Découvrir ».
  function nomPartie(l, pa) { return l.parties.length > 1 ? 'Partie ' + pa.code + ' · ' + pa.titre : ''; }
  function titreEcran(l, pa, etape) {
    return 'Leçon ' + l.numero + (l.parties.length > 1 ? pa.code : '') + ' · ' + etape;
  }

  /* ---------- 3. Audio : fichier validé si présent, sinon voix de synthèse (provisoire) ----------
     Le générateur met dans chaque terme : audio[voix][débit] = chemin du fichier mp3,
     seulement pour les fichiers validés (ou tous avec --non-valides). S'il manque,
     la voix de synthèse de l'appareil lit l'écrit du terme ; les « voix » F1, H3…
     sont alors simulées par la hauteur (VOIX_PROVISOIRES dans generer_lecteur.py). */
  var voixVi = null;
  // Cherche une voix de synthèse vietnamienne sur l'appareil (la liste arrive parfois en retard).
  function chercherVoix() {
    if (!('speechSynthesis' in window)) return;
    var v = window.speechSynthesis.getVoices().filter(function (x) { return /^vi/i.test(x.lang); });
    voixVi = v.length ? v[0] : null;
    afficherBandeau();
  }
  // Bandeau jaune en haut : caché dès qu'il existe au moins un fichier audio ;
  // sinon il explique la voix provisoire, ou comment installer une voix vietnamienne.
  function afficherBandeau() {
    var aDesFichiers = D.lecons.some(function (l) { return l.series.some(function (s) { return s.termes.some(function (t) { return Object.keys(t.audio).length; }); }); });
    if (aDesFichiers) { bandeau.hidden = true; return; }
    bandeau.hidden = false;
    if (!('speechSynthesis' in window)) {
      bandeau.textContent = 'Ce navigateur ne sait pas lire de voix de synthèse. Essayez Chrome, Edge ou Safari.';
    } else if (!voixVi) {
      bandeau.textContent = 'Aucune voix vietnamienne trouvée sur cet appareil. Sur Windows : Paramètres › Heure et langue › Langue et région › Ajouter une langue › Tiếng Việt (cochez « Synthèse vocale »). Sur Android et iPhone, elle est en général déjà présente.';
    } else {
      bandeau.textContent = 'Version d’essai : voix de synthèse de l’appareil (' + voixVi.name + '), en attendant les enregistrements validés. Les trois « voix » sont simulées.';
    }
  }
  if ('speechSynthesis' in window) {
    chercherVoix();
    window.speechSynthesis.onvoiceschanged = chercherVoix;
  }

  // JOUER UN TERME : jouer(terme, 'F1', 'slow') renvoie une « promesse » qui se termine
  // quand le son est fini. On enchaîne avec .then(...) : jouer(a).then(function () { return jouer(b); }).
  // Sécurité : la promesse se termine de toute façon après 5 à 6 s (son bloqué).
  var lectureEnCours = null;

  // MODE TEST (DEC-0047) : dans la case du mot qui vient d'être joué, une petite note dit
  // ce qui a été entendu : fichier, personnage, F (femme) ou H (homme), modèle FPT, débit et
  // valeur « speed ». Une ligne par voix (en E1, la femme puis l'homme).
  // Se désactive dans Réglages (« Infos de test sur le son »).
  // En E2, E3 et à l'échauffement, les notes n'apparaissent qu'APRÈS la réponse (sinon le
  // nom du fichier trahirait la bonne réponse) : on n'indique alors pas de case à jouer().
  function texteInfoSon(terme, codeVoix, debit, fichier) {
    var v = D.voix.filter(function (x) { return x.code === codeVoix; })[0] || {};
    var genre = v.genre === 'female' ? 'F' : v.genre === 'male' ? 'H' : '?';
    var qui = (v.nom || codeVoix) + ' · ' + genre + ' · ' + codeVoix;
    var nomDebit = { slow: 'lent', normal: 'normal', spaced: 'mots espacés' }[debit] || debit;
    var vitesse = nomDebit + (v.vitesse_fpt && v.vitesse_fpt[debit] != null ? ' · speed ' + String(v.vitesse_fpt[debit]).replace('.', ',') : '');
    if (!fichier) return ['synthèse de l’appareil (aucun fichier)', qui, nomDebit];
    return [fichier.split('/').pop(), qui, (v.modele ? v.modele + ' · ' : '') + vitesse];
  }
  function noterInfoSon(caseMot, terme, codeVoix, debit) {
    if (!caseMot || !reglages().infoTest) return;
    var f = terme.audio && terme.audio[codeVoix] && terme.audio[codeVoix][debit];
    var bloc = caseMot.querySelector('.info-son');
    if (!bloc) { bloc = el('span', { class: 'info-son', 'aria-hidden': 'true' }); caseMot.appendChild(bloc); }
    var ligne = bloc.querySelector('[data-voix="' + codeVoix + '"]');
    if (!ligne) { ligne = el('span', { class: 'info-son-voix' }); ligne.dataset.voix = codeVoix; bloc.appendChild(ligne); }
    ligne.innerHTML = '';
    texteInfoSon(terme, codeVoix, debit, f).forEach(function (x) { ligne.appendChild(el('span', { text: x })); });
  }

  // jouer(terme, voix, débit, caseMot) : caseMot (facultatif) = case où noter l'info de test.
  function jouer(terme, codeVoix, debit, caseMot) {
    return new Promise(function (resolve) {
      var fini = false;
      function fin() { if (!fini) { fini = true; resolve(); } }
      // 1) Un fichier existe pour cette voix et ce débit : on le joue.
      var f = terme.audio[codeVoix] && terme.audio[codeVoix][debit];
      noterInfoSon(caseMot, terme, codeVoix, debit);   // mode test (DEC-0047)
      if (f) {
        if (lectureEnCours) lectureEnCours.pause();
        var a = new Audio(f);
        lectureEnCours = a;
        a.onended = fin; a.onerror = fin;
        a.play().catch(fin);
        setTimeout(fin, 6000);
        return;
      }
      // 2) Sinon, voix de synthèse : elle lit l'écrit du terme, avec la hauteur de la « voix »
      //    simulée et une vitesse = débit × vitesse de la voix × réglage de l'apprenant.
      if (!('speechSynthesis' in window)) { fin(); return; }
      var v = D.voix.filter(function (x) { return x.code === codeVoix; })[0] || D.voix[0];
      var u = new SpeechSynthesisUtterance((terme.appui ? terme.appui + ' ' : '') + terme.ecrit);
      u.lang = 'vi-VN';
      if (voixVi) u.voice = voixVi;
      u.pitch = v.hauteur || 1;
      u.rate = (D.debits[debit] || 0.9) * (v.vitesse || 1) * (reglages().vitesse || 1);
      u.onend = fin; u.onerror = fin;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
      setTimeout(fin, 5000);
    });
  }
  // Coupe le son en cours (appelé à chaque changement d'écran).
  function arreterSon() {
    if (lectureEnCours) lectureEnCours.pause();
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  }
  // pause(700) : attendre 700 millisecondes dans un enchaînement de sons.
  function pause(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  // Une voix au hasard, différente de « sauf » (pour ne pas répéter la même voix).
  // Voix d'écoute de la leçon (l.voix, DEC-0055 : leçons de sons et leçons de tons n'ont pas les mêmes).
  function voixAuHasard(l, sauf) {
    var toutes = (l && l.voix && l.voix.length) ? l.voix : D.voix.map(function (v) { return v.code; });
    var c = toutes.filter(function (x) { return x !== sauf; });
    return c.length ? c[hasard(c.length)] : toutes[0];
  }

  /* ---------- 4. Affichage d'un terme ---------- */
  // Contenu d'une tuile ou d'une carte pour un terme, selon le mode :
  //   'decouverte' (E1) : symbole + catégorie + repère + indice + sens
  //   'lent'   (phase 1) : image + symbole + repère en petit
  //   'normal' (phase 2) : symbole seul (l'image passe en petit, voir .symbole-seul en CSS)
  //   'ecrit'  (fin d'E3) : image + écrit + sens (syllabe inventée : 🔊, jamais écrite)
  // Renvoie une liste d'éléments à placer dans la tuile.
  function contenuTerme(t, mode) {
    // mode : 'decouverte' (E1), 'lent' (image + symbole), 'normal' (symbole seul), 'ecrit'
    var morceaux = [];
    var cat = t.symbole.categorie;
    // Catégorie du son (DEC-0038) : indice affiché en E1 et au débit lent, retiré au débit normal.
    var avecIndices = mode === 'decouverte' || mode === 'lent';
    var sym = el('span', { class: 'symbole' + (cat && avecIndices ? ' cat-' + cat : '') }, [
      cat && avecIndices ? el('span', { class: 'marque', text: MARQUES[cat], 'aria-hidden': 'true' }) : null,
      t.symbole.texte
    ]);
    if (t.symbole.couleur) sym.style.color = t.symbole.couleur;
    var pl = placeDe(t.symbole);
    if (pl && pl.court && mode !== 'ecrit') sym.appendChild(el('span', { class: 'place place-' + t.symbole.place, text: pl.court }));
    var img = t.image ? el('span', { class: 'image', text: t.image, 'aria-hidden': 'true' }) : null;
    if (mode === 'ecrit') {
      if (img) morceaux.push(img);
      if (t.appui) morceaux.push(el('span', { class: 'appui', text: t.appui }));   // mot d'appui (DEC-0060)
      morceaux.push(t.invente ? el('span', { class: 'ecrit', text: '🔊' }) : el('span', { class: 'ecrit', text: t.ecrit }));
      morceaux.push(el('span', { class: 'sens', text: t.invente ? 'syllabe inventée (jamais écrite)' : t.sens }));
      return morceaux;
    }
    if (img) morceaux.push(img);
    morceaux.push(sym);
    var r = t.symbole.repere;
    if (r && r.image && avecIndices && reglages().aides) {
      // Mot repère (DEC-0038) : français écrit ; vietnamien en image seulement (pas d'écrit en E1–E2).
      morceaux.push(el('span', { class: 'repere' + (mode === 'lent' ? ' petit-repere' : ''), title: 'mot repère' }, [
        el('span', { 'aria-hidden': 'true', text: r.langue === 'fr' ? '🇫🇷 ' : '🇻🇳 ' }),
        el('span', { text: r.image + (r.mot && mode === 'decouverte' ? ' ' + r.mot : '') })
      ]));
    }
    if (mode === 'decouverte') {
      if (t.symbole.indication && reglages().aides) morceaux.push(el('span', { class: 'indication', text: t.symbole.indication }));
      if (t.sens) morceaux.push(el('span', { class: 'sens', text: 'mot entendu : ' + t.sens }));
    }
    return morceaux;
  }
  // Marque de catégorie d'un son (DEC-0038), toujours affichée avec la couleur.
  var MARQUES = { identique: '=', proche: '≈', nouveau: '★' };
  // PLACES : pour chaque place, le texte court de la pastille (dans le symbole),
  // le texte long (en-tête d'E1) et la consigne d'E2–E3. Modifier ces textes ici.
  // Place du son dans le mot (DEC-0042) : une même consonne peut être au début ou à la fin.
  var PLACES = {
    debut: { court: 'début ▸', long: 'consonne en début de mot', consigne: 'Écoutez la consonne du début du mot.' },
    fin: { court: '◂ fin', long: 'consonne en fin de mot', consigne: 'Écoutez la consonne de la fin du mot.' },
    voyelle: { court: '', long: 'voyelle', consigne: 'Écoutez la voyelle (le milieu du mot).' },
    ton: { court: '', long: 'ton', consigne: 'Écoutez le ton (la mélodie du mot).' }
  };
  function placeDe(sym) { return PLACES[sym && sym.place] || null; }
  // RÈGLES PROPRES AUX LEÇONS DE TONS (l.tons vrai)
  //   debitSon   : débit du SON joué ; toujours normal pour les tons (le ralenti déforme la mélodie)
  //   voixUnique : vrai quand il faut une seule voix (tons, phase 1) ; voixModele : F1
  //   nomPhase   : nom affiché de la phase (« débit lent » ou, pour les tons, « avec images »)
  // Leçons de tons (DEC-0043) : jamais d'audio lent, le ralenti déforme la mélodie.
  // Les deux phases d'E2–E3 restent (images + symboles, puis symboles seuls), au débit normal.
  function debitSon(l, debit) { return l.tons ? 'normal' : debit; }
  // Leçons de tons (DEC-0045) : on compare des mélodies, donc d'abord avec UNE voix (la voix modèle) ;
  // plusieurs voix ensuite seulement, en phase « symboles seuls », pour rendre l'exercice plus difficile.
  function voixUnique(l, debit) { return l.tons && debit === 'slow'; }
  function voixModele() { return D.voix.some(function (v) { return v.code === 'F1'; }) ? 'F1' : D.voix[0].code; }   // R-AUD-03
  function nomPhase(l, debit) {
    if (l.tons) return debit === 'slow' ? 'avec images' : 'symboles seuls';
    return debit === 'slow' ? 'débit lent' : 'débit normal';
  }
  // Légende des catégories affichée sous les tuiles.
  var LIBELLES = { identique: 'son du français', proche: 'son proche du français', nouveau: 'son nouveau' };
  function legende(series) {
    var vues = {};
    series.forEach(function (s) { s.termes.forEach(function (t) { if (t.symbole.categorie) vues[t.symbole.categorie] = true; }); });
    var cats = ['identique', 'proche', 'nouveau'].filter(function (c) { return vues[c]; });
    if (!cats.length) return null;
    return el('div', { class: 'legende' }, cats.map(function (c) {
      return el('span', { class: 'symbole-legende cat-' + c }, [el('span', { class: 'marque', text: MARQUES[c] }), LIBELLES[c]]);
    }));
  }
  // Nom lu par les lecteurs d'écran pour une tuile. NE PAS MODIFIER : les essais automatiques
  // s'en servent pour trouver les tuiles.
  function nomAccessible(t) {
    return (t.sens ? t.sens + ', ' : '') + 'symbole ' + t.symbole.texte;  // ne pas modifier : utilisé par les essais automatiques
  }
  // Classe de la grille selon le nombre de tuiles (3 ou 4 : colonnes en plus sur grand écran).
  function classeTuiles(n) { return 'tuiles' + (n === 3 ? ' trois' : n === 4 ? ' quatre' : ''); }

  /* ---------- 5. Calcul des scores et des verrous (R-VOL-05 à 07, DEC-0032) ----------
     Une étape E2 ou E3 a deux phases :
       phase 1 ('slow')   → passe en phase 2 quand : 20 réponses au moins (P.fenetre_score)
                            et taux de réussite ≥ seuil de la leçon sur les 20 dernières ;
       phase 2 ('normal') → étape VALIDÉE quand : même condition, + au moins 2 voix
                            différentes (P.min_voix) dans ces 20 réponses, + chaque série
                            réussie au moins 2 fois en phase 2 (P.min_reussites_par_serie). */
  // Mesure sur les 20 dernières réponses d'une phase : nombre, justes, taux, nombre de voix.
  function mesure(etat, debit) {
    var h = etat.hist.filter(function (x) { return x.d === debit; }).slice(-P.fenetre_score);
    var justes = h.filter(function (x) { return x.ok; }).length;
    var voix = {};
    h.forEach(function (x) { voix[x.v] = true; });
    return { n: h.length, justes: justes, taux: h.length ? justes / h.length : 0, voix: Object.keys(voix).length };
  }
  // Nombre de séries réussies au moins 2 fois en phase 2.
  function seriesCouvertes(series, etat) {
    return series.filter(function (s) { return (etat.reussites[s.code] || 0) >= P.min_reussites_par_serie; }).length;
  }
  // Appelée après CHAQUE réponse. Renvoie 'normal' (passage en phase 2), 'validee'
  // (étape validée) ou null (rien ne change). Modifie l'état de l'étape en conséquence.
  function verifierPassages(seuil, series, etat) {
    var m = mesure(etat, etat.debit);
    var seuilAtteint = m.n >= P.fenetre_score && m.taux >= seuil;
    if (etat.debit === 'slow' && seuilAtteint) { etat.debit = 'normal'; return 'normal'; }
    if (etat.debit === 'normal' && seuilAtteint && m.voix >= P.min_voix && seriesCouvertes(series, etat) === series.length && !etat.validee) {
      etat.validee = true; return 'validee';
    }
    return null;
  }

  /* ---------- 6. Écran : accueil (liste des leçons) ---------- */
  // La 1re leçon est toujours ouverte ; la suivante quand l'écoute de la précédente est validée (R-VOL-02).
  function leconOuverte(i) {
    if (i === 0 || toutOuvert()) return true;
    var prec = prog.lecons[D.lecons[i - 1].code];
    return !!(prec && prec.ecouteValideeLe);
  }
  // Affiche la liste des leçons avec leur état (pastille) ; une leçon sans série est « À venir ».
  function ecranAccueil() {
    arreterSon();
    vider();
    btnRetour.hidden = true;
    titreBarre.textContent = 'Vietnamien · Module 0';
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Volet écoute' }),
      el('h1', { text: 'Les sons et les tons' }),
      el('p', { class: 'petit', text: 'Chaque leçon s’ouvre quand l’écoute de la précédente est validée. 20 à 30 minutes par jour suffisent.' }),
      toutOuvert() ? el('p', { class: 'mode-essai', text: 'Mode essai : toutes les leçons et étapes sont ouvertes (Réglages pour retrouver les verrous).' }) : null
    ]));
    var liste = el('div', { class: 'lecons' });
    D.lecons.forEach(function (l, i) {
      var etat = prog.lecons[l.code];
      var ouverte = leconOuverte(i) && l.series.length > 0;
      var pastille;
      if (etat && etat.ecouteValideeLe) pastille = el('span', { class: 'pastille ok', text: 'Écoute validée' });
      else if (!l.series.length) pastille = el('span', { class: 'pastille ferme', text: 'À venir' });
      else if (!ouverte) pastille = el('span', { class: 'pastille ferme', text: 'Fermée' });
      else pastille = el('span', { class: 'pastille', text: etat ? 'En cours' : 'Ouverte' });
      var detail = l.series.length + ' séries' + (l.parties.length > 1 ? ' en ' + l.parties.length + ' parties' : '') + ' · seuil ' + pourcent(l.seuil);
      liste.appendChild(el('button', {
        class: 'lecon', type: 'button', disabled: !ouverte,
        onclick: function () { ecranLecon(l.code); }
      }, [
        el('span', { class: 'num', text: 'L' + String(l.numero).padStart(2, '0') }),
        el('span', { class: 'titre' }, [el('span', { text: l.titre }), el('br'), el('span', { class: 'petit', text: detail })]),
        pastille
      ]));
    });
    app.appendChild(liste);
    app.appendChild(el('div', { class: 'actions' }, [
      el('button', { class: 'bouton second', type: 'button', text: '🎵 Les 6 tons', onclick: function () { ecranTons(ecranAccueil); } }),
      el('button', { class: 'bouton second', type: 'button', text: '⚙ Réglages', onclick: ecranReglages })]));
    pied.textContent = 'Données générées le ' + D.genere_le + '. Progression enregistrée dans ce navigateur, sur cet appareil.';
  }

  /* ---------- 7. Écran : une leçon ---------- */
  var deplies = {};   // parties terminées affichées en entier (pour cette visite seulement)
  // Une partie est terminée quand son écrit a été vu et validé (bouton en fin d'E3).
  function partieTerminee(code, pa) { var e = etatLecon(code).parties[pa.code]; return !!(e && e.ecrit); }

  // Écran d'une leçon : pour chaque partie, les blocs E1, E2, E3 et l'écrit, chacun
  // ouvert ou fermé selon les verrous ; puis « Mes progrès » et « Recommencer ».
  function ecranLecon(code) {
    arreterSon();
    var l = trouverLecon(code);
    var etatL = etatLecon(code);
    sauver();
    vider();
    btnRetour.hidden = false;
    btnRetour.onclick = ecranAccueil;
    titreBarre.textContent = 'Leçon ' + l.numero;
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Leçon ' + l.numero + (l.tons ? ' · tons' : ' · sons') }),
      el('h1', { text: l.titre }),
      l.parties.length > 1 ? el('p', { class: 'petit', text: 'Cette leçon se fait en ' + l.parties.length + ' parties, l’une après l’autre. Elle est validée quand toutes le sont.' }) : null
    ]));

    // Pour chaque partie (A puis B, ou U) : la partie B n'est ouverte que si A est terminée.
    l.parties.forEach(function (pa, k) {
      var series = seriesDe(l, pa);
      var etat = etatPartie(code, pa.code);
      var partieOuverte = k === 0 || toutOuvert() || partieTerminee(code, l.parties[k - 1]);
      var etapes = el('div', { class: 'etapes' });
      // Une partie terminée est réduite à une ligne « Validée » (bouton Afficher / Réduire).
      var reduite = l.parties.length > 1 && etat.ecrit && !deplies[code + pa.code];
      if (l.parties.length > 1) {
        etapes.appendChild(el('div', { class: 'partie-tete' }, [
          el('h2', { text: nomPartie(l, pa) }),
          el('span', { class: 'pastille' + (etat.ecrit ? ' ok' : partieOuverte ? '' : ' ferme'),
            text: etat.ecrit ? 'Validée' : partieOuverte ? series.length + ' séries' : 'Après la partie ' + l.parties[k - 1].code }),
          etat.ecrit ? el('button', { class: 'bouton discret', type: 'button', text: reduite ? 'Afficher' : 'Réduire',
            'aria-expanded': reduite ? 'false' : 'true',
            onclick: function () { deplies[code + pa.code] = reduite; ecranLecon(code); } }) : null
        ]));
      }
      if (reduite) { app.appendChild(etapes); return; }
      // Bloc E1 : jauge = sons vus / sons de la partie.
      var e1Fait = e1Termine(etat, pa);
      var nbEl = elementsDe(pa).length || 1;
      etapes.appendChild(blocEtape('E1 · Découvrir', 'Écoutez chaque ' + (l.tons ? 'ton' : 'son') + ' dans plusieurs mots, sans répondre.',
        e1Vus(etat, pa) + ' / ' + elementsDe(pa).length + (l.tons ? ' tons' : ' sons'), e1Fait ? 1 : e1Vus(etat, pa) / nbEl,
        e1Fait ? 'Réécouter' : 'Commencer', partieOuverte, function () { ecranE1(code, pa.code, 0); }));

      // Blocs E2 et E3 : E2 s'ouvre quand E1 est faite, E3 quand E2 est validée.
      // La jauge approche 1 quand le taux s'approche du seuil sur 20 réponses.
      [['e2', 'E2 · Distinguer', 'Lequel avez-vous entendu ? Deux choix.'], ['e3', 'E3 · Opposer', 'Lequel avez-vous entendu ? Toute la série.']].forEach(function (x, j) {
        var e = etat[x[0]];
        var m = mesure(e, e.debit);
        var ouvert = partieOuverte && (toutOuvert() || (j === 0 ? e1Fait : etat.e2.validee));
        var texte = e.validee ? 'Validée' :
          nomPhase(l, e.debit).replace(/^./, function (c) { return c.toUpperCase(); }) + ' · ' + m.justes + ' justes sur les ' + m.n + ' dernières' +
          (e.debit === 'normal' ? ' · séries réussies 2 fois : ' + seriesCouvertes(series, e) + ' / ' + series.length : '');
        // E2 : échauffement « Pareil ou différent ? » non noté avant le premier « Lequel ? » (DEC-0041)
        var echauffer = j === 0 && !e.echauffe && !e.hist.length;
        var bloc = blocEtape(x[1], x[2], texte, e.validee ? 1 : Math.min(1, m.taux * Math.min(1, m.n / P.fenetre_score) / l.seuil),
          e.validee ? 'Refaire' : echauffer ? 'Commencer' : 'Continuer', ouvert,
          function () { if (echauffer) ecranPareil(code, pa.code); else ecranQuiz(code, pa.code, x[0]); });
        if (j === 0 && ouvert && !echauffer) {
          bloc.querySelector('.actions').appendChild(el('button', { class: 'bouton second', type: 'button', text: 'Pareil ou différent ?',
            onclick: function () { ecranPareil(code, pa.code); } }));
        }
        etapes.appendChild(bloc);
      });

      // Bloc « Combien de fois ? » (DEC-0054) : ouvert quand E3 est validée ; compte pour le verrou.
      var aCombien = itemsCombien(l, pa.code).length > 0;
      var combienFait = !aCombien || (etat.combien && etat.combien.validee);
      if (aCombien) {
        var ec = etatCombien(code, pa.code), cc = ciblesCombien(l, pa.code), mc = mesure(ec, ec.debit);
        etapes.appendChild(blocEtape('Fin d’E3 · Combien de fois ?', 'Une suite de mots : combien de fois entendez-vous le son ou le ton ?',
          ec.validee ? 'Validée' : nomPhase(l, ec.debit).replace(/^./, function (c) { return c.toUpperCase(); }) + ' · ' + mc.justes + ' justes sur les ' + mc.n + ' dernières' +
            (ec.debit === 'normal' ? ' · sons réussis 2 fois : ' + seriesCouvertes(cc, ec) + ' / ' + cc.length : ''),
          ec.validee ? 1 : Math.min(1, mc.taux * Math.min(1, mc.n / P.fenetre_score) / l.seuil),
          ec.validee ? 'Refaire' : ec.hist.length ? 'Continuer' : 'Commencer',
          partieOuverte && (toutOuvert() || etat.e3.validee), function () { ecranCombien(code, pa.code); }));
      }
      // Bloc de l'écrit : ouvert quand E3 et « Combien de fois ? » sont validés.
      etapes.appendChild(blocEtape('Fin d’E3 · L’écrit', 'Découvrez comment s’écrivent les mots entendus.',
        etat.ecrit ? 'Vu' : aCombien ? 'Après « Combien de fois ? »' : 'Après la validation d’E3', etat.ecrit ? 1 : 0,
        'Voir l’écrit', partieOuverte && (toutOuvert() || (etat.e3.validee && combienFait)), function () { ecranEcrit(code, pa.code); }));
      app.appendChild(etapes);
    });

    var resume = el('div', { class: 'etapes' });
    resume.appendChild(el('div', { class: 'etape' }, [
      el('div', { class: 'etape-tete' }, [el('h2', { text: 'Écoute de la leçon' }),
        el('span', { class: 'pastille' + (etatL.ecouteValideeLe ? ' ok' : ' ferme'), text: etatL.ecouteValideeLe ? 'Validée le ' + etatL.ecouteValideeLe : 'Pas encore validée' })]),
      el('p', { class: 'petit', text: 'Valider l’écoute ouvre la leçon suivante.' })
    ]));
    // Bloc E4 (volet production, DEC-0049) : ouvert quand l'écoute de la leçon est validée (R-VOL-03).
    if (l.production && l.production.length) {
      var e4 = etatE4(code);
      var b4 = bilanE4(l, e4, e4.debit);
      // termine : les deux passages faits ; « Refaire » efface les notes (l'historique est gardé).
      var termine = e4.debit === 'normal' && b4.notes === b4.total;
      var texte4 = termine ? 'Parcourue le ' + e4.faiteLe + ' · ' + b4.proches + ' / ' + b4.total + ' proches au débit normal' :
        (e4.debit === 'slow' ? 'Passage 1 (modèle lent)' : 'Passage 2 (modèle normal)') + ' · ' + b4.notes + ' / ' + b4.total + ' mots' +
        (e4.faiteLe ? ' · déjà parcourue le ' + e4.faiteLe : '');
      resume.appendChild(blocEtape('E4 · Répéter', 'Écoutez le modèle, enregistrez-vous, comparez les courbes, notez-vous.',
        texte4, termine ? 1 : (e4.debit === 'normal' ? 0.5 : 0) + b4.notes / b4.total / 2,
        termine ? 'Refaire' : b4.notes || e4.debit === 'normal' ? 'Continuer' : 'Commencer', ouvertureE4(code),
        function () {
          if (termine) { e4.debit = 'slow'; e4.notes = {}; sauver(); }
          ecranE4(code, premierE4(l, e4));
        }));
      if (!ouvertureE4(code)) resume.lastChild.appendChild(el('p', { class: 'petit', text: 'S’ouvre quand l’écoute de la leçon est validée.' }));
    }
    resume.appendChild(el('div', { class: 'etape' }, [
      el('div', { class: 'etape-tete' }, [el('h2', { text: 'E5 · Stabiliser' }), el('span', { class: 'pastille ferme', text: 'À venir' })]),
      el('p', { class: 'petit', text: 'Enchaînements et lecture avant écoute : après E4.' })
    ]));
    app.appendChild(resume);

    app.appendChild(el('div', { class: 'actions' }, [
      el('button', { class: 'bouton second', type: 'button', text: '📈 Mes progrès dans cette leçon', onclick: function () { ecranProgres(code); } }),
      l.tons ? el('button', { class: 'bouton second', type: 'button', text: '🎵 Les 6 tons', onclick: function () { ecranTons(function () { ecranLecon(code); }); } }) : null]));

    // « Recommencer cette leçon » : demande confirmation, puis efface la leçon de la progression.
    var zone = el('div', { class: 'actions' });
    zone.appendChild(el('button', { class: 'bouton discret', type: 'button', text: 'Recommencer cette leçon', onclick: function () {
      zone.innerHTML = '';
      zone.appendChild(el('div', { class: 'confirmation' }, [
        el('p', { text: 'Toute la progression de la leçon ' + l.numero + ' sera effacée.' }),
        el('div', { class: 'actions' }, [
          el('button', { class: 'bouton', type: 'button', text: 'Effacer', onclick: function () { delete prog.lecons[code]; sauver(); ecranLecon(code); } }),
          el('button', { class: 'bouton second', type: 'button', text: 'Annuler', onclick: function () { ecranLecon(code); } })
        ])
      ]));
    } }));
    app.appendChild(zone);
  }
  // Fabrique le bloc d'une étape : titre, état (texte), consigne, jauge (part de 0 à 1),
  // bouton (libellé, ouvert ou « Fermée », action au clic).
  function blocEtape(titre, consigne, etat, part, libelle, ouvert, action) {
    var j = el('div', { class: 'jauge' }, [el('span')]);
    j.firstChild.style.width = Math.round(Math.max(0, Math.min(1, part)) * 100) + '%';
    return el('div', { class: 'etape' }, [
      el('div', { class: 'etape-tete' }, [el('h2', { text: titre }), el('span', { class: 'petit', text: etat })]),
      el('p', { class: 'petit', text: consigne }),
      j,
      el('div', { class: 'actions' }, [el('button', { class: 'bouton', type: 'button', text: ouvert ? libelle : 'Fermée', disabled: !ouvert, onclick: action })])
    ]);
  }
  // Retrouve une partie de leçon par son code.
  function partieDe(l, pc) { return l.parties.filter(function (p) { return p.code === pc; })[0]; }

  /* ---------- 8. Écran : E1 Découvrir, un son à la fois (DEC-0039) ---------- */
  // Chaque son (ou ton) de la partie, seul, dans quelques mots ; chaque mot dit par une voix
  // de femme puis une voix d'homme ; deux boutons : écoute au débit normal ou au débit lent ;
  // choix de la voix : femme et homme (par défaut), femme seule, homme seul.
  // Aucune opposition entre sons en E1 : les différences commencent en E2.
  function elementsDe(pa) { return pa.elements || []; }
  function e1Vus(etat, pa) {
    var els = elementsDe(pa);
    return etat.e1.vues.filter(function (x) { return els.indexOf(x) >= 0; }).length;
  }
  function e1Termine(etat, pa) {
    // Progression antérieure à DEC-0039 (E1 par séries) : une E2 déjà commencée vaut E1 faite.
    return e1Vus(etat, pa) >= elementsDe(pa).length || etat.e2.hist.length > 0 || etat.e2.validee;
  }
  // Affiche le son n° index de la partie : sa carte, le choix des voix, les boutons
  // d'écoute et ses mots d'exemple (l.decouverte[son].mots, venus de exemples_e1.csv).
  // Le son est noté « vu » (etat.e1.vues) après une écoute complète.
  function ecranE1(code, pc, index) {
    arreterSon();
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var els = elementsDe(pa);
    var etat = etatPartie(code, pc);
    // d = le son présenté : { element, symbole, mots: [{ ecrit, sens, image, voix: [femme, homme], audio }] }
    var d = l.decouverte[els[index]];
    // lent : vitesse choisie en dernier (bouton « Écouter lentement ») ; choixVoix : femme, homme ou les deux.
    var lent = false;
    var choixVoix = 'fh';   // 'fh' : femme puis homme ; 'f' : femme ; 'h' : homme
    vider();
    btnRetour.onclick = function () { ecranLecon(code); };
    titreBarre.textContent = titreEcran(l, pa, 'E1 Découvrir');
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: (l.tons ? 'Ton ' : 'Son ') + (index + 1) + ' sur ' + els.length +
        (placeDe(d.symbole) && !l.tons ? ' · ' + placeDe(d.symbole).long : '') }),
      el('h1', { text: 'Écoutez, sans répondre' }),
      el('p', { class: 'petit', text: l.tons ? 'Le même ton dans plusieurs mots, à vitesse normale (le ralenti déforme la mélodie). Choisissez la voix ; touchez un mot pour le réentendre.'
        : 'Le même son dans plusieurs mots. Choisissez la voix et la vitesse ; touchez un mot pour le réentendre.' })
    ]));
    // Le son présenté : symbole, catégorie, mot repère, indice d'écoute (DEC-0038)
    var carte = el('div', { class: 'carte-son' }, contenuTerme({ symbole: d.symbole, image: '', sens: '' }, 'decouverte'));
    app.appendChild(carte);

    // dire(m) : prononce un mot avec la voix choisie (ou femme puis homme), à la vitesse choisie.
    function dire(m, caseMot) {
      var v = m.voix;
      var debit = debitSon(l, lent ? 'slow' : 'normal');
      if (choixVoix === 'f') return jouer(m, v[0], debit, caseMot);
      if (choixVoix === 'h') return jouer(m, v[1], debit, caseMot);
      return jouer(m, v[0], debit, caseMot).then(function () { return pause(450); }).then(function () { return jouer(m, v[1], debit, caseMot); });
    }
    var boutonsVoix = [['fh', '👩 👨 Femme et homme'], ['f', '👩 Femme'], ['h', '👨 Homme']].map(function (x) {
      var b = el('button', { class: 'choix-voix' + (x[0] === choixVoix ? ' choisi' : ''), type: 'button',
        'aria-pressed': x[0] === choixVoix ? 'true' : 'false', text: x[1], onclick: function () {
          choixVoix = x[0];
          boutonsVoix.forEach(function (o) { var oui = o.dataset.v === choixVoix; o.classList.toggle('choisi', oui); o.setAttribute('aria-pressed', oui ? 'true' : 'false'); });
        } });
      b.dataset.v = x[0];
      return b;
    });
    // Tuiles des mots : image (ou 🔊) et sens ; aucun écrit vietnamien en E1 (R-ECR-01).
    var grille = el('div', { class: classeTuiles(d.mots.length) });
    var tuiles = d.mots.map(function (m, i) {
      var b = el('button', { class: 'tuile', type: 'button', 'aria-label': 'mot ' + (i + 1) + (m.sens ? ', ' + m.sens : ''),
        onclick: function () { surligner(i); dire(m, tuiles[i]).then(function () { surligner(-1); }); } }, [
        el('span', { class: 'image', text: m.image || '🔊', 'aria-hidden': 'true' }),
        m.sens ? el('span', { class: 'sens', text: m.sens + (m.appui ? ' · avec son classificateur' : '') }) : null   // DEC-0062
      ]);
      grille.appendChild(b);
      return b;
    });
    function surligner(k) { tuiles.forEach(function (b, i) { b.classList.toggle('joue', i === k); }); }
    var suivant = el('button', { class: 'bouton', type: 'button', disabled: etat.e1.vues.indexOf(d.element) < 0,
      text: index + 1 < els.length ? (l.tons ? 'Ton suivant' : 'Son suivant') : 'Terminer E1',
      onclick: function () { if (index + 1 < els.length) ecranE1(code, pc, index + 1); else ecranLecon(code); } });
    // Deux boutons : vitesse normale ou lente. Toucher un mot le redit à la vitesse choisie en dernier.
    // ecouterTout : dit tous les mots l'un après l'autre ; à la fin, le son est noté « vu »
    // et « Son suivant » s'active.
    function ecouterTout(avecLenteur) {
      lent = avecLenteur;
      ecoute.disabled = true; ecouteLente.disabled = true;
      ecoute.classList.toggle('choisi', !lent); ecouteLente.classList.toggle('choisi', lent);
      var seq = Promise.resolve();
      d.mots.forEach(function (m, i) {
        seq = seq.then(function () { surligner(i); return dire(m, tuiles[i]); }).then(function () { return pause(700); });
      });
      seq.then(function () {
        surligner(-1); ecoute.disabled = false; ecouteLente.disabled = false;
        if (etat.e1.vues.indexOf(d.element) < 0) { etat.e1.vues.push(d.element); sauver(); }
        suivant.disabled = false;
      });
    }
    var ecoute = el('button', { class: 'ecoute choisi', type: 'button', text: '▶ Écouter', onclick: function () { ecouterTout(false); } });
    var ecouteLente = el('button', { class: 'ecoute', type: 'button', text: '🐢 Écouter lentement', onclick: function () { ecouterTout(true); } });
    app.appendChild(el('div', { class: 'choix-voix-groupe', role: 'group', 'aria-label': 'Voix' }, boutonsVoix));
    // Leçon de tons : pas d'écoute lente (DEC-0043)
    // Leçon de tons : un seul bouton (pas d'écoute lente, DEC-0043).
    app.appendChild(l.tons ? el('div', { class: 'actions centre' }, [ecoute]) : el('div', { class: 'deux-ecoutes' }, [ecoute, ecouteLente]));
    app.appendChild(grille);
    var lg = legende([{ termes: [{ symbole: d.symbole }] }]); if (lg) app.appendChild(lg);
    app.appendChild(el('div', { class: 'actions' }, [suivant]));
    if (!d.mots.length) { suivant.disabled = false; ecoute.disabled = true; ecouteLente.disabled = true; }
  }

  /* ---------- 9. Écran : échauffement « Pareil ou différent ? » (DEC-0041) ---------- */
  // Non noté, hors verrou. Deux termes de la paire d'E2, débit lent, deux voix différentes
  // (même quand les termes sont pareils : on juge le son, pas l'enregistrement).
  var NB_PAIRES_ECHAUFFEMENT = 10;
  function ecranPareil(code, pc) {
    arreterSon();
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var series = seriesDe(l, pa);
    var e2 = etatPartie(code, pc).e2;
    // reponses : 10 cases vrai/faux (vrai = paire pareille), moitié-moitié, mélangées.
    var reponses = melanger(Array.apply(null, Array(NB_PAIRES_ECHAUFFEMENT)).map(function (_, i) { return i % 2 === 0; }));
    var k = 0, justes = 0;

    // item() : affiche la paire n° k. fin() : écran de résultat.
    function item() {
      if (k >= reponses.length) return fin();
      var s = series[hasard(series.length)];
      // La paire d'E2 de la série (positions 1 et 2) ; t2 = t1 si la paire doit être pareille.
      var paire = s.termes.slice(0, 2);
      var t1 = paire[hasard(2)];
      var pareil = reponses[k];
      var t2 = pareil ? t1 : paire[1 - paire.indexOf(t1)];
      // Sons : deux voix différentes (DEC-0041). Tons : la même voix modèle pour les deux mots (DEC-0045).
      var v1 = l.tons ? voixModele() : voixAuHasard(l, null), v2 = l.tons ? v1 : voixAuHasard(l, v1);
      vider();
      btnRetour.onclick = function () { ecranLecon(code); };
      titreBarre.textContent = titreEcran(l, pa, 'E2 Pareil ou différent ?');
      app.appendChild(el('div', { class: 'consigne' }, [
        el('span', { class: 'etiquette', text: 'Échauffement · paire ' + (k + 1) + ' sur ' + reponses.length + ' · non noté' }),
        el('h1', { text: 'Pareil ou différent ?' }),
        el('p', { class: 'consigne-place', text: (placeDe(s.termes[0].symbole) || PLACES.voyelle).consigne }),
        el('p', { class: 'petit', text: l.tons ? 'Deux mots, la même voix. La mélodie est-elle la même ?' : 'Deux mots, deux voix. Ce son est-il le même dans les deux mots ?' })
      ]));
      var ds = debitSon(l, 'slow');
      function ecouterPaire() { return jouer(t1, v1, ds).then(function () { return pause(700); }).then(function () { return jouer(t2, v2, ds); }); }
      app.appendChild(el('button', { class: 'ecoute', type: 'button', text: '▶ Réécouter', onclick: ecouterPaire }));
      var retour = el('p', { class: 'retour-reponse', role: 'status' });
      var revelation = el('div', { class: 'tuiles' });
      var suivant = el('button', { class: 'bouton', type: 'button', text: 'Suivant', hidden: true, onclick: function () { k++; item(); } });
      var repondu = false;
      // repondre(vrai = « Pareil ») : corrige, puis montre les deux termes (réécoutables).
      // Rien n'est enregistré dans le score : l'échauffement est hors verrou.
      function repondre(dit) {
        if (repondu) return;
        repondu = true;
        var ok = dit === pareil;
        if (ok) justes++;
        boutons.forEach(function (b) { b.disabled = true; });
        boutons[pareil ? 0 : 1].classList.add('juste');
        if (!ok) boutons[pareil ? 1 : 0].classList.add('faux');
        retour.className = 'retour-reponse ' + (ok ? 'juste' : 'faux');
        retour.textContent = ok ? 'Juste.' : (pareil ? 'C’était le même son.' : 'Les deux sons étaient différents.');
        // On montre les deux termes (image et symbole) ; toucher pour réentendre.
        [[t1, v1], [t2, v2]].forEach(function (x, i) {
          var c = el('button', { class: 'tuile', type: 'button', 'aria-label': 'mot ' + (i + 1) + ', ' + nomAccessible(x[0]),
            onclick: function () { jouer(x[0], x[1], ds, c); } }, [el('span', { class: 'etiquette', text: 'Mot ' + (i + 1) })].concat(contenuTerme(x[0], 'lent')));
          revelation.appendChild(c);
          noterInfoSon(c, x[0], x[1], ds);   // mode test : ce qui a été entendu, une fois la réponse donnée
        });
        suivant.hidden = false;
        sauver();
      }
      var boutons = [
        el('button', { class: 'tuile reponse-pd', type: 'button', onclick: function () { repondre(true); } }, [el('span', { class: 'symbole', text: '=' }), el('span', { text: 'Pareil' })]),
        el('button', { class: 'tuile reponse-pd', type: 'button', onclick: function () { repondre(false); } }, [el('span', { class: 'symbole', text: '≠' }), el('span', { text: 'Différent' })])
      ];
      app.appendChild(el('div', { class: 'tuiles' }, boutons));
      app.appendChild(retour);
      app.appendChild(revelation);
      app.appendChild(el('div', { class: 'actions' }, [suivant]));
      setTimeout(ecouterPaire, 250);
    }
    // Fin : l'échauffement est noté fait (le bouton E2 affichera « Continuer »).
    function fin() {
      e2.echauffe = true; sauver();
      vider();
      titreBarre.textContent = titreEcran(l, pa, 'E2 Pareil ou différent ?');
      app.appendChild(el('div', { class: 'consigne' }, [
        el('span', { class: 'etiquette', text: 'Échauffement terminé · non noté' }),
        el('h1', { text: justes + ' juste' + (justes > 1 ? 's' : '') + ' sur ' + reponses.length }),
        el('p', { class: 'petit', text: 'Maintenant, il faudra dire lequel des deux sons vous entendez. C’est cette étape qui compte pour valider.' })
      ]));
      app.appendChild(el('div', { class: 'actions' }, [
        el('button', { class: 'bouton', type: 'button', text: 'Commencer « Lequel ? »', onclick: function () { ecranQuiz(code, pc, 'e2'); } }),
        el('button', { class: 'bouton second', type: 'button', text: 'Encore ' + NB_PAIRES_ECHAUFFEMENT + ' paires', onclick: function () { ecranPareil(code, pc); } })
      ]));
    }
    item();
  }

  /* ---------- 10. Écran : E2 et E3 « Lequel ? » ----------
     ecranQuiz(code, partie, 'e2' ou 'e3'). Une question = une série tirée au sort,
     un terme cible joué, des tuiles de choix (2 en E2, toute la série en E3).
     Chaque réponse est enregistrée puis verifierPassages() décide du passage de phase. */
  function ecranQuiz(code, pc, cle) {
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var series = seriesDe(l, pa);
    // e = état de l'étape (e2 ou e3) : phase, historique, réussites, validée.
    var e = etatPartie(code, pc)[cle];
    var derniereVoix = null;
    var positionsJustes = [];

    // Tirage d'une série, pondéré : en phase 2, une série pas encore réussie 2 fois
    // a plus de chances de sortir (poids 1 + 2 par réussite manquante).
    function choisirSerie() {
      // Les séries pas encore réussies 2 fois au débit normal sont tirées plus souvent (DEC-0032).
      var poids = series.map(function (s) {
        var manque = Math.max(0, P.min_reussites_par_serie - (e.reussites[s.code] || 0));
        return 1 + (e.debit === 'normal' ? manque * 2 : 0);
      });
      var total = poids.reduce(function (a, b) { return a + b; }, 0);
      var r = Math.random() * total;
      for (var i = 0; i < poids.length; i++) { r -= poids[i]; if (r < 0) return series[i]; }
      return series[series.length - 1];
    }

    // nouvelItem() : prépare une question : choix (2 en E2, toute la série en E3),
    // terme cible, ordre des tuiles (règle des 3 fois de suite), voix.
    function nouvelItem() {
      var s = choisirSerie();
      var choix = cle === 'e2' ? s.termes.slice(0, 2) : s.termes.slice();   // DEC-0026, DEC-0033
      var cible = choix[hasard(choix.length)];
      var ordre;
      // Pas plus de 3 fois de suite la bonne réponse à la même place (PROG-ACT § 4).
      for (var essai = 0; essai < 20; essai++) {
        ordre = melanger(choix);
        var pos = ordre.indexOf(cible);
        var n = P.max_meme_position;
        var memes = positionsJustes.length >= n && positionsJustes.slice(-n).every(function (p) { return p === pos; });
        if (!memes) break;
      }
      positionsJustes.push(ordre.indexOf(cible));
      var voix = voixUnique(l, e.debit) ? voixModele() : voixAuHasard(l, derniereVoix);
      derniereVoix = voix;
      afficherItem(s, ordre, cible, voix);
    }

    // afficherItem() : construit l'écran de la question et gère la réponse.
    function afficherItem(s, ordre, cible, voix) {
      vider();
      btnRetour.onclick = function () { ecranLecon(code); };
      titreBarre.textContent = titreEcran(l, pa, cle === 'e2' ? 'E2 Distinguer' : 'E3 Opposer');
      var debit = e.debit;            // phase du verrou (lent puis normal)
      var son = debitSon(l, debit);   // débit de l'audio : toujours normal pour les tons (DEC-0043)
      var m = mesure(e, debit);
      app.appendChild(el('div', { class: 'mesures' }, [
        el('div', { class: 'mesure' }, [el('b', { text: l.tons ? (debit === 'slow' ? 'Images' : 'Symboles') : (debit === 'slow' ? 'Lent' : 'Normal') }), el('span', { text: l.tons ? 'phase' : 'débit' })]),
        el('div', { class: 'mesure' }, [el('b', { text: m.justes + ' / ' + m.n }), el('span', { text: 'justes · objectif ' + pourcent(l.seuil) + ' sur ' + P.fenetre_score })]),
        el('div', { class: 'mesure' }, [el('b', { text: debit === 'normal' ? seriesCouvertes(series, e) + ' / ' + series.length : '—' }), el('span', { text: 'séries réussies 2 fois' })])
      ]));
      var ecoute = el('button', { class: 'ecoute', type: 'button', text: '▶ Réécouter', onclick: function () { jouer(cible, voix, son); } });
      app.appendChild(el('div', { class: 'consigne' }, [el('h1', { text: 'Lequel avez-vous entendu ?' }),
        el('p', { class: 'consigne-place', text: (placeDe(s.termes[0].symbole) || PLACES.voyelle).consigne })]));
      app.appendChild(ecoute);
      var mode = debit === 'slow' ? 'lent' : 'normal';
      var grille = el('div', { class: classeTuiles(ordre.length) });
      var retour = el('p', { class: 'retour-reponse', role: 'status' });
      var repondu = false;
      var suivant = el('button', { class: 'bouton', type: 'button', text: 'Suivant', hidden: true, onclick: nouvelItem });
      var tuiles = ordre.map(function (t) {
        var cls = 'tuile' + (mode === 'normal' ? ' symbole-seul' : '');
        var b = el('button', { class: cls, type: 'button', 'aria-label': nomAccessible(t), onclick: function () {
          if (repondu) { jouer(t, voix, son, b); return; }
          // Première touche = réponse : on l'enregistre dans l'historique, on compte la
          // réussite de la série (phase 2), puis on vérifie les passages de phase.
          repondu = true;
          var ok = t === cible;
          e.hist.push({ s: s.code, ok: ok, v: voix, d: debit, t: Date.now(), c: s.termes.indexOf(cible), r: s.termes.indexOf(t) });
          if (e.hist.length > 3000) e.hist = e.hist.slice(-3000);
          if (ok && debit === 'normal') e.reussites[s.code] = (e.reussites[s.code] || 0) + 1;
          var passage = verifierPassages(l.seuil, series, e);
          sauver();
          var caseCible = tuiles[ordre.indexOf(cible)];
          caseCible.classList.add('juste');
          // Retour : « Juste » et on réentend le terme ; sinon on réentend le bon, puis celui choisi.
          if (ok) {
            retour.className = 'retour-reponse juste'; retour.textContent = 'Juste.';
            jouer(cible, voix, son, caseCible).then(function () {
              if (reglages().suivantAuto && !passage && app.contains(suivant)) setTimeout(function () { if (app.contains(suivant)) nouvelItem(); }, 600);
            });
          } else {
            b.classList.add('faux');
            retour.className = 'retour-reponse faux'; retour.textContent = 'C’était l’autre. Écoutez les deux.';
            jouer(cible, voix, son, caseCible).then(function () { return pause(400); }).then(function () { return jouer(t, voix, son, b); });
          }
          suivant.hidden = false;
          // Messages de passage en phase 2 ou de validation de l'étape.
          if (passage === 'normal') retour.textContent += l.tons ? ' Seuil atteint avec les images : on passe aux symboles seuls, avec plusieurs voix.' : ' Seuil atteint au débit lent : on passe au débit normal, avec les symboles seuls.';
          if (passage === 'validee') {
            retour.textContent += ' Étape validée !';
            suivant.textContent = cle === 'e2' ? 'Revenir à la leçon (E3 ouverte)' : 'Revenir à la leçon (voir l’écrit)';
            suivant.onclick = function () { ecranLecon(code); };
          }
          suivant.focus();
        } }, contenuTerme(t, mode));
        grille.appendChild(b);
        return b;
      });
      app.appendChild(grille);
      if (mode === 'lent') { var lg = legende([s]); if (lg) app.appendChild(lg); }
      app.appendChild(retour);
      app.appendChild(el('div', { class: 'actions' }, [suivant]));
      app.appendChild(el('p', { class: 'petit', text: 'Réécouter ne coûte rien. Après votre réponse, touchez une case pour l’entendre.' }));
      // Le terme est joué automatiquement peu après l'affichage.
      setTimeout(function () { jouer(cible, voix, son); }, 250);
    }

    nouvelItem();
  }

  /* ---------- 10 bis. Écran : « Combien de fois ? » (fin d'E3, DEC-0054) ----------
     L'apprenant entend une suite de mots connus (plus tard une petite phrase) et dit combien de
     fois il entend le son ou le ton de la leçon. Mêmes phases et même verrou que E2/E3 :
     phase 1 'slow' (symbole + repère, débit lent ; tons : débit normal, une voix), puis phase 2
     'normal' (symbole seul, plusieurs voix) ; étape validée quand le seuil de la leçon est atteint
     sur les 20 dernières réponses, avec au moins 2 voix, et chaque son réussi 2 fois en phase 2.
     Aucun écrit avant la réponse ; ensuite la suite écrite est montrée, cibles en évidence.
     État : etatPartie(code, pc).combien = { debit, hist, reussites (par élément), validee }. */
  var NOMBRES_COMBIEN = [0, 1, 2, 3, 4, 5];
  function itemsCombien(l, pc) { return (l.combien || []).filter(function (x) { return x.partie === pc; }); }
  // Les « séries » du verrou sont ici les éléments (sons ou tons) à compter.
  function ciblesCombien(l, pc) {
    var vus = [];
    itemsCombien(l, pc).forEach(function (x) { if (vus.indexOf(x.element) < 0) vus.push(x.element); });
    return vus.map(function (e) { return { code: e }; });
  }
  function etatCombien(code, pc) {
    var e = etatPartie(code, pc);
    if (!e.combien) e.combien = etatEtape();
    return e.combien;
  }
  // Consigne : quoi compter, selon la place du son (DEC-0042).
  function consigneCombien(sym) {
    if (sym.place === 'ton') return 'Combien de fois entendez-vous le ton ' + (sym.nom || '') + ' ?';
    if (sym.place === 'debut') return 'Combien de mots commencent par ce son ?';
    if (sym.place === 'fin') return 'Combien de mots finissent par ce son ?';
    return 'Combien de fois entendez-vous cette voyelle ?';
  }

  function ecranCombien(code, pc) {
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var items = itemsCombien(l, pc);
    var cibles = ciblesCombien(l, pc);
    var e = etatCombien(code, pc);
    var derniereVoix = null, dernierItem = null;

    // Tirage : en phase 2, les sons pas encore réussis 2 fois sortent plus souvent (comme E2/E3).
    function choisir() {
      var poids = items.map(function (x) {
        var manque = Math.max(0, P.min_reussites_par_serie - (e.reussites[x.element] || 0));
        return (x === dernierItem ? 0.2 : 1) + (e.debit === 'normal' ? manque * 2 : 0);
      });
      var total = poids.reduce(function (a, b) { return a + b; }, 0), r = Math.random() * total;
      for (var i = 0; i < poids.length; i++) { r -= poids[i]; if (r < 0) return items[i]; }
      return items[items.length - 1];
    }

    function nouvelItem() {
      var x = choisir();
      dernierItem = x;
      var voix = voixUnique(l, e.debit) ? voixModele() : voixAuHasard(l, derniereVoix);
      derniereVoix = voix;
      afficher(x, voix);
    }

    function afficher(x, voix) {
      vider();
      btnRetour.onclick = function () { arreterSon(); ecranLecon(code); };
      titreBarre.textContent = titreEcran(l, pa, 'Combien de fois ?');
      var debit = e.debit, son = debitSon(l, debit), m = mesure(e, debit);
      app.appendChild(el('div', { class: 'mesures' }, [
        el('div', { class: 'mesure' }, [el('b', { text: l.tons ? (debit === 'slow' ? 'Repère' : 'Symbole') : (debit === 'slow' ? 'Lent' : 'Normal') }), el('span', { text: l.tons ? 'phase' : 'débit' })]),
        el('div', { class: 'mesure' }, [el('b', { text: m.justes + ' / ' + m.n }), el('span', { text: 'justes · objectif ' + pourcent(l.seuil) + ' sur ' + P.fenetre_score })]),
        el('div', { class: 'mesure' }, [el('b', { text: debit === 'normal' ? seriesCouvertes(cibles, e) + ' / ' + cibles.length : '—' }), el('span', { text: 'sons réussis 2 fois' })])
      ]));
      // Ce qu'il faut compter : le symbole (avec repère en phase 1), sans aucun écrit vietnamien.
      app.appendChild(el('div', { class: 'consigne' }, [el('h1', { text: consigneCombien(x.symbole) })]));
      app.appendChild(el('div', { class: 'carte-son' }, contenuTerme({ symbole: x.symbole, image: '', sens: '' }, debit === 'slow' ? 'lent' : 'normal')));
      // Mode test (DEC-0047) : l'info sur le son (fichier, locuteur, débit) est affichée DÈS L'ÉCOUTE,
      // sous le bouton : contrairement à E2/E3, elle ne trahit pas la réponse (le nombre).
      var infoSon = el('div', { class: 'info-combien' });
      // Trois écoutes au choix (DEC-0058) : vitesse normale, vitesse lente (leçons de sons seulement,
      // DEC-0043), mots espacés (phrases : points de suspension entre les mots, débit normal).
      // En phase 2, une réponse donnée après une écoute lente ou espacée n'est pas comptée (DEC-0057).
      var aideLente = false;
      var aide = function () { if (!repondu && debit === 'normal') aideLente = true; };
      var boutonsEcoute = [el('button', { class: 'ecoute', type: 'button', text: '▶ Vitesse normale',
        onclick: function () { jouer(x, voix, 'normal', infoSon); } })];
      if (!l.tons) boutonsEcoute.push(el('button', { class: 'ecoute', type: 'button', text: '🐢 Vitesse lente',
        onclick: function () { aide(); jouer(x, voix, 'slow', infoSon); } }));
      if (x.nature === 'phrase') boutonsEcoute.push(el('button', { class: 'ecoute', type: 'button', text: '… Mots espacés',
        onclick: function () { aide(); jouer(x, voix, 'spaced', infoSon); } }));
      app.appendChild(el('div', { class: 'ecoutes-combien' }, boutonsEcoute));
      app.appendChild(infoSon);
      if (debit === 'normal' && boutonsEcoute.length > 1) app.appendChild(el('p', { class: 'petit centre',
        text: 'Les écoutes lente et espacée aident, mais la réponse qui suit n’est pas comptée pour valider l’étape.' }));
      var retour = el('p', { class: 'retour-reponse', role: 'status' });
      var revele = el('div', { class: 'suite-revelee', hidden: true });
      var suivant = el('button', { class: 'bouton', type: 'button', text: 'Suivant', hidden: true, onclick: nouvelItem });
      var repondu = false;
      var boutons = NOMBRES_COMBIEN.map(function (n) {
        return el('button', { class: 'tuile nombre', type: 'button', text: String(n), 'aria-label': n + ' fois', onclick: function () {
          if (repondu) return;
          repondu = true;
          var ok = n === x.nombre;
          // Avec l'aide lente, la réponse est gardée dans l'historique (d = 'aide') mais ne compte
          // ni dans le taux de la phase, ni dans les réussites par son (DEC-0057).
          e.hist.push({ s: x.element, i: x.code, ok: ok, v: voix, d: aideLente ? 'aide' : debit, t: Date.now(), c: x.nombre, r: n });
          if (e.hist.length > 3000) e.hist = e.hist.slice(-3000);
          if (ok && debit === 'normal' && !aideLente) e.reussites[x.element] = (e.reussites[x.element] || 0) + 1;
          var passage = aideLente ? null : verifierPassages(l.seuil, cibles, e);
          sauver();
          boutons[NOMBRES_COMBIEN.indexOf(x.nombre)].classList.add('juste');
          if (!ok) this.classList.add('faux');
          retour.className = 'retour-reponse ' + (ok ? 'juste' : 'faux');
          retour.textContent = (ok ? 'Juste : ' + x.nombre + ' fois.' : 'Il fallait ' + x.nombre + '. Réécoutez en suivant les mots.') +
            (aideLente ? ' (Écoute lente ou espacée utilisée : réponse non comptée.)' : '');
          // Révélation de l'écrit (après la réponse seulement), cibles en évidence.
          // Suite : mots séparés par « · » ; phrase (DEC-0056) : syllabes séparées par des espaces,
          // majuscule et ponctuation de la phrase, puis sa traduction.
          revele.innerHTML = '';
          var phrase = x.nature === 'phrase';
          x.mots.forEach(function (w, k) {
            if (k) revele.appendChild(document.createTextNode(phrase ? ' ' : ' · '));
            var t = phrase && k === 0 ? w.ecrit.charAt(0).toUpperCase() + w.ecrit.slice(1) : w.ecrit;
            revele.appendChild(el('span', { class: w.cible ? 'mot-cible' : 'mot', text: t }));
          });
          var ponct = phrase ? (x.ecrit.match(/[.?!]$/) || [''])[0] : '';
          if (ponct) revele.appendChild(document.createTextNode(ponct));
          if (x.sens) revele.appendChild(el('span', { class: 'sens-phrase', text: x.sens }));
          revele.hidden = false;
          jouer(x, voix, son, infoSon);
          suivant.hidden = false;
          if (passage === 'normal') retour.textContent += l.tons ? ' Seuil atteint : on passe aux symboles seuls, avec plusieurs voix.' : ' Seuil atteint au débit lent : on passe au débit normal.';
          if (passage === 'validee') {
            retour.textContent += ' Étape validée !';
            suivant.textContent = 'Revenir à la leçon (voir l’écrit)';
            suivant.onclick = function () { ecranLecon(code); };
          }
          suivant.focus();
        } });
      });
      app.appendChild(el('div', { class: 'nombres' }, boutons));
      app.appendChild(retour);
      app.appendChild(revele);
      app.appendChild(el('div', { class: 'actions' }, [suivant]));
      app.appendChild(el('p', { class: 'petit', text: 'Réécouter ne coûte rien. Comptez les syllabes qui contiennent le son ou le ton.' }));
      setTimeout(function () { jouer(x, voix, son, infoSon); }, 300);
    }

    if (!items.length) { ecranLecon(code); return; }
    nouvelItem();
  }

  /* ---------- 11. Écran : l'écrit (fin d'E3) ----------
     Montre l'écrit de tous les termes de la partie ; le bouton valide la partie et,
     si c'est la dernière, enregistre la date de validation de l'écoute de la leçon
     (ce qui ouvre la leçon suivante). */
  /* ---------- Fin d'E3 : l'écrit (R-ECR-02 ; syllabes inventées jamais affichées, R-LEX-06) ---------- */
  function ecranEcrit(code, pc) {
    arreterSon();
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var etatL = etatLecon(code);
    var etat = etatPartie(code, pc);
    vider();
    btnRetour.onclick = function () { ecranLecon(code); };
    titreBarre.textContent = titreEcran(l, pa, 'L’écrit');
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Fin d’E3' + (nomPartie(l, pa) ? ' · ' + nomPartie(l, pa) : '') }),
      el('h1', { text: 'Voici comment ils s’écrivent' }),
      el('p', { class: 'petit', text: 'Touchez une case pour réentendre. Rien à retenir par cœur : l’écrit se travaillera en E4–E5.' })
    ]));
    seriesDe(l, pa).forEach(function (s) {
      var g = el('div', { class: classeTuiles(s.termes.length) });
      s.termes.forEach(function (t) {
        var c = el('button', { class: 'tuile', type: 'button', 'aria-label': t.invente ? 'syllabe inventée' : t.ecrit,
          onclick: function () { jouer(t, (l.voix && l.voix[0]) || D.voix[0].code, 'normal', c); } }, contenuTerme(t, 'ecrit'));
        g.appendChild(c);
      });
      app.appendChild(g);
    });
    // Le bouton valide la partie ; si toutes les parties sont validées, la date de
    // validation de l'écoute est enregistrée (elle ouvre la leçon suivante).
    var derniere = l.parties.every(function (p) { return p.code === pc || partieTerminee(code, p); });
    var libelle = etat.ecrit ? 'Revenir à la leçon' :
      derniere ? 'Valider l’écoute de la leçon' : 'Valider la partie ' + pc;
    app.appendChild(el('div', { class: 'actions' }, [el('button', { class: 'bouton', type: 'button', text: libelle,
      onclick: function () {
        etat.ecrit = true;
        if (l.parties.every(function (p) { return partieTerminee(code, p); }) && !etatL.ecouteValideeLe) {
          etatL.ecouteValideeLe = new Date().toISOString().slice(0, 10);
        }
        sauver();
        ecranLecon(code);
      } })]));
  }

  /* ---------- 11 bis. Écran : E4 Répéter (volet production, DEC-0049, DEC-0050) ----------
     Les mots supports de la leçon (l.production), un par écran. Deux passages :
       passage 1 ('slow')   : le modèle F1 au débit lent (fichier lent FPT) ;
       passage 2 ('normal') : le modèle au débit normal, quand tous les mots ont une note au passage 1.
     Pour chaque mot : écouter le modèle, s'enregistrer, se réécouter (seul, ou « moi puis
     le modèle »), regarder les deux courbes mélodiques, puis se noter « proche » ou « à
     reprendre ». Au bout de P.essais_max_e4 « à reprendre », on passe au mot suivant.
     Verrou de production (R-VOL-08) : non décidé ; E4 est seulement marquée « parcourue ».
     Les enregistrements restent en mémoire le temps de l'écran : rien n'est gardé ni envoyé.
     État : etatLecon(code).e4 = { debit, notes: { 'W0029': { slow: {note, essais, t}, normal: {...} } },
                                   hist: [{ w, d, note, essais, t }], faiteLe } */
  var micro = null;   // un seul micro pour tout le lecteur (autorisation demandée une fois)
  function etatE4(code) {
    var e = etatLecon(code);
    if (!e.e4) e.e4 = { debit: 'slow', notes: {}, hist: [], faiteLe: null };
    return e.e4;
  }
  function ouvertureE4(code) { return toutOuvert() || !!etatLecon(code).ecouteValideeLe; }   // R-VOL-03 ; mode essai : DEC-0051
  // Nombre de mots notés au passage en cours, et nombre de « proche ».
  function bilanE4(l, e, debit) {
    var notes = l.production.map(function (m) { return e.notes[m.code] && e.notes[m.code][debit]; }).filter(Boolean);
    return { notes: notes.length, proches: notes.filter(function (n) { return n.note === 'proche'; }).length, total: l.production.length };
  }
  // Premier mot sans note au passage en cours (ou 0).
  function premierE4(l, e) {
    for (var i = 0; i < l.production.length; i++) {
      var n = e.notes[l.production[i].code];
      if (!n || !n[e.debit]) return i;
    }
    return 0;
  }
  // Courbe du modèle au format de prononciation.js : points { x de 0 à 1, st }.
  function courbeModele(m, debit) {
    var c = m.courbes && m.courbes[debit];
    if (!c || !c.p.length) return null;
    var n = c.p.length;
    return { points: c.p.map(function (st, k) { return { x: n > 1 ? k / (n - 1) : 0, st: st }; }), medianeHz: c.m };
  }

  function ecranE4(code, index) {
    arreterSon();
    var l = trouverLecon(code);
    var e = etatE4(code);
    var debit = e.debit;
    var m = l.production[index];
    var essais = (e.notes[m.code] && e.notes[m.code][debit] && e.notes[m.code][debit].essais) || 0;
    var miennes = null, urlMoi = null, enreg = false;
    var C = window.Prononciation;
    vider();
    btnRetour.onclick = function () { arreterSon(); if (micro) micro.arreter(); ecranLecon(code); };
    titreBarre.textContent = 'Leçon ' + l.numero + ' · E4 Répéter';
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: (m.avec_classificateur ? 'Avec son classificateur · ' : '') + 'Mot ' + (index + 1) + ' sur ' + l.production.length +
        ' · modèle ' + (debit === 'slow' ? 'lent (passage 1)' : 'normal (passage 2)') }),
      el('h1', { text: 'Écoutez, répétez, comparez' }),
      el('p', { class: 'petit', text: 'Écoutez le modèle, enregistrez-vous, réécoutez-vous à côté du modèle, puis notez-vous honnêtement.' })
    ]));

    // Le mot : image, écrit (visible en E4, R-ECR-03), sens.
    var carteMot = el('div', { class: 'carte-son carte-e4' }, [
      m.image ? el('span', { class: 'image', text: m.image, 'aria-hidden': 'true' }) : null,
      el('span', { class: 'ecrit-e4', text: m.ecrit }),
      el('span', { class: 'sens', text: m.sens })
    ]);
    app.appendChild(carteMot);   // mode test (DEC-0047) : l'info sur le son du modèle s'y affiche

    // Ce qu'il faut réussir : son ou ton de la leçon, et chemin de prononciation (DEC-0038).
    m.cibles.forEach(function (s) {
      var sym = el('span', { class: 'symbole' + (s.categorie ? ' cat-' + s.categorie : '') }, [
        s.categorie ? el('span', { class: 'marque', text: MARQUES[s.categorie], 'aria-hidden': 'true' }) : null, s.texte]);
      if (s.couleur) sym.style.color = s.couleur;
      var pl = placeDe(s);
      var bloc = el('div', { class: 'cible-e4' }, [
        el('div', { class: 'cible-tete' }, [sym, el('span', { class: 'petit', text: s.place === 'ton' ? s.indication : (pl ? pl.long : '') })])
      ]);
      if (s.chemin && reglages().aides) {
        bloc.appendChild(el('dl', { class: 'chemin' }, [
          el('dt', { text: 'Départ' }), el('dd', { text: s.chemin.depart }),
          el('dt', { text: 'Changement' }), el('dd', { text: s.chemin.changement }),
          el('dt', { text: 'Vérifier' }), el('dd', { text: s.chemin.verification + (s.chemin.certitude === 'à vérifier' ? ' (indication à vérifier)' : '') })
        ]));
      }
      app.appendChild(bloc);
    });

    // Boutons d'écoute et d'enregistrement.
    var modele = { ecrit: m.ecrit, audio: m.audio };
    var vm = voixModele();
    var bModele = el('button', { class: 'ecoute choisi', type: 'button', text: '▶ Modèle' + (debit === 'slow' ? ' (lent)' : ''),
      onclick: function () { jouer(modele, vm, debit, carteMot); } });
    var bEnreg = el('button', { class: 'ecoute enreg', type: 'button', text: '🎤 M’enregistrer', onclick: basculer });
    var bMoi = el('button', { class: 'ecoute', type: 'button', text: '▶ Moi', disabled: true, onclick: function () { jouerMoi(); } });
    var bLesDeux = el('button', { class: 'ecoute', type: 'button', text: '▶ Moi puis le modèle', disabled: true,
      onclick: function () { jouerMoi().then(function () { return pause(500); }).then(function () { return jouer(modele, vm, debit, carteMot); }); } });
    var etat = el('p', { class: 'retour-reponse', text: '' });
    app.appendChild(el('div', { class: 'boutons-e4' }, [bModele, bEnreg, bMoi, bLesDeux]));
    app.appendChild(etat);

    // Courbes : modèle (au débit joué) et ma voix.
    var canvas = el('canvas', { class: 'courbe-e4', 'aria-label': 'Courbes mélodiques du modèle et de ma voix' });
    app.appendChild(el('div', { class: 'cadre-courbe' }, [
      el('div', { class: 'legende' }, [
        el('span', { class: 'trait-legende modele', text: 'modèle' }), el('span', { class: 'trait-legende moi', text: 'ma voix' })]),
      canvas,
      el('p', { class: 'petit', text: l.tons
        ? 'Comparez la FORME : monte, descend, se casse. Un trou = voix grinçante ou coup de glotte, normal pour ngã et nặng.'
        : 'La courbe montre la mélodie (le ton), pas la voyelle ni la consonne : pour elles, comparez à l’oreille avec « Moi puis le modèle ».' })
    ]));
    function couleur(nom) { return getComputedStyle(document.documentElement).getPropertyValue(nom).trim(); }
    function dessiner() {
      if (!C) return;
      C.dessiner(canvas, [
        { courbe: courbeModele(m, debit), couleur: couleur('--accent') },
        { courbe: miennes, couleur: couleur('--moi') || '#d9572b' }
      ]);
    }
    dessiner();
    window.onresize = dessiner;

    function jouerMoi() {
      return new Promise(function (resolve) {
        if (!urlMoi) { resolve(); return; }
        arreterSon();
        var a = new Audio(urlMoi);
        lectureEnCours = a;
        a.onended = resolve; a.onerror = resolve;
        a.play().catch(resolve);
      });
    }
    // Enregistrer / arrêter (même bouton). Le micro est demandé au premier clic.
    function basculer() {
      if (!C) { etat.textContent = 'Module micro absent (prononciation.js).'; return; }
      if (enreg) { micro.arreter(); return; }
      if (!micro) micro = new C.Micro();
      arreterSon();
      etat.className = 'retour-reponse';
      etat.textContent = 'Autorisation du micro…';
      micro.autoriser().then(function () {
        enreg = true;
        bEnreg.textContent = '■ Arrêter';
        bEnreg.classList.add('en-cours');
        etat.textContent = '● Enregistrement : dites le mot (arrêt automatique à 3 s).';
        return micro.enregistrer(C.PARAM.dureeMax);
      }).then(function (blob) {
        enreg = false;
        bEnreg.textContent = '🎤 Recommencer';
        bEnreg.classList.remove('en-cours');
        if (urlMoi) URL.revokeObjectURL(urlMoi);
        urlMoi = URL.createObjectURL(blob);
        bMoi.disabled = false; bLesDeux.disabled = false;
        etat.textContent = 'Analyse…';
        return C.analyser(blob);
      }).then(function (r) {
        miennes = r.courbe;
        etat.textContent = r.courbe.points.length ? 'Réécoutez-vous à côté du modèle, puis notez-vous.' : 'Voix trop faible : rapprochez-vous du micro et recommencez.';
        dessiner();
        noter.hidden = false;
      }).catch(function (err) {
        enreg = false;
        bEnreg.textContent = '🎤 M’enregistrer';
        bEnreg.classList.remove('en-cours');
        etat.className = 'retour-reponse faux';
        etat.textContent = 'Micro indisponible (' + (err && err.name ? err.name : err) + ') : autorisez le micro pour cette page (icône à gauche de l’adresse), puis recommencez.';
      });
    }

    // Auto-évaluation (PROG-ACT) : apparaît après un enregistrement.
    var essaisMax = P.essais_max_e4 || 3;
    var info = el('p', { class: 'petit centre', text: 'Essai ' + Math.min(essais + 1, essaisMax) + ' sur ' + essaisMax + '.' });
    var noter = el('div', { class: 'noter-e4', hidden: true }, [
      el('p', { class: 'petit', text: 'Ma prononciation est-elle proche du modèle ?' }),
      el('div', { class: 'actions centre' }, [
        el('button', { class: 'bouton', type: 'button', text: '✔ Proche', onclick: function () { enregistrerNote('proche'); } }),
        el('button', { class: 'bouton second', type: 'button', text: '↻ À reprendre', onclick: function () { enregistrerNote('reprendre'); } })
      ])
    ]);
    app.appendChild(noter);
    app.appendChild(info);
    function enregistrerNote(note) {
      essais += 1;
      var fini = note === 'proche' || essais >= essaisMax;
      e.hist.push({ w: m.code, d: debit, note: note, essais: essais, t: Date.now() });
      if (fini) {
        e.notes[m.code] = e.notes[m.code] || {};
        e.notes[m.code][debit] = { note: note, essais: essais, t: Date.now() };
      } else {
        e.notes[m.code] = e.notes[m.code] || {};
        e.notes[m.code][debit] = null;
        e.notes[m.code]['essais_' + debit] = essais;
      }
      sauver();
      if (!fini) {
        // Nouvel essai sur le même mot.
        miennes = null; dessiner(); noter.hidden = true;
        etat.className = 'retour-reponse';
        etat.textContent = 'Réécoutez le modèle, puis réessayez.';
        info.textContent = 'Essai ' + (essais + 1) + ' sur ' + essaisMax + '.';
        return;
      }
      suivant();
    }
    // Mot suivant, ou fin du passage.
    function suivant() {
      var b = bilanE4(l, e, debit);
      if (b.notes < b.total) { ecranE4(code, premierE4(l, e)); return; }
      if (debit === 'slow') e.debit = 'normal';
      else if (!e.faiteLe) e.faiteLe = jour(Date.now());
      sauver();
      ecranFinE4(code, debit, b);
    }
    // Les essais déjà faits sur ce mot, avant de quitter l'écran (note « à reprendre » intermédiaire).
    if (!essais && e.notes[m.code] && e.notes[m.code]['essais_' + debit]) {
      essais = e.notes[m.code]['essais_' + debit];
      info.textContent = 'Essai ' + Math.min(essais + 1, essaisMax) + ' sur ' + essaisMax + '.';
    }
    app.appendChild(el('div', { class: 'actions' }, [
      el('button', { class: 'bouton discret', type: 'button', text: 'Passer ce mot', onclick: function () {
        var i = (index + 1) % l.production.length; ecranE4(code, i); } })
    ]));
    // Le modèle est joué une fois en arrivant.
    setTimeout(function () { jouer(modele, vm, debit, carteMot); }, 300);
  }

  // Fin d'un passage d'E4 : bilan, et suite.
  function ecranFinE4(code, debit, b) {
    var l = trouverLecon(code);
    vider();
    btnRetour.onclick = function () { ecranLecon(code); };
    titreBarre.textContent = 'Leçon ' + l.numero + ' · E4 Répéter';
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: debit === 'slow' ? 'Passage 1 terminé' : 'E4 parcourue' }),
      el('h1', { text: b.proches + ' mot' + (b.proches > 1 ? 's' : '') + ' sur ' + b.total + ' jugé' + (b.proches > 1 ? 's' : '') + ' proche' + (b.proches > 1 ? 's' : '') }),
      el('p', { class: 'petit', text: debit === 'slow'
        ? 'Passage 2 : les mêmes mots, avec le modèle au débit normal.'
        : 'Le verrou de production n’est pas encore défini (R-VOL-08) : vous pouvez refaire E4 autant que vous voulez.' })
    ]));
    app.appendChild(el('div', { class: 'actions' }, [
      debit === 'slow' ? el('button', { class: 'bouton', type: 'button', text: 'Commencer le passage 2', onclick: function () { ecranE4(code, 0); } }) : null,
      el('button', { class: 'bouton second', type: 'button', text: 'Retour à la leçon', onclick: function () { ecranLecon(code); } })
    ]));
  }

  /* ---------- 11 ter. Écran : « Les 6 tons » (référence, DEC-0052, DEC-0053) ----------
     La même syllabe (ma, má, mà, mả, mã, mạ : reference_tons.csv) dite avec les 6 tons, par une
     voix de femme (F1) ou d'homme (H3), au débit normal ou lent.
     Chaque ton est montré par un SCHÉMA simple (DEC-0053), pas par une courbe mesurée :
     hauteur sur l'échelle de 1 (grave) à 5 (aigu) de Chao (colonne chao de tons.csv), coup de
     glotte marqué ˀ (ngã, au milieu) ou ʔ (nặng, à la fin), nặng plus court.
     SCHEMAS_TONS : le tracé de chaque ton. x de 0 (début) à 1 (fin) ; n = niveau de 1 à 5.
       trait     : points du tracé principal (reliés en courbe douce)
       suite     : second morceau après la cassure (ngã)
       option    : morceau en pointillés (hỏi : remontée faible ou absente à Hanoï)
       glotte    : { x, n, signe } : marque du coup de glotte */
  var SCHEMAS_TONS = {
    ngang: { trait: [[0, 3], [1, 3]] },
    sac:   { trait: [[0, 3], [0.45, 3.1], [1, 5]] },
    huyen: { trait: [[0, 2], [0.5, 1.6], [1, 1]] },
    hoi:   { trait: [[0, 3], [0.45, 1.6], [0.72, 1]], option: [[0.72, 1], [0.88, 1.2], [1, 2.4]] },
    nga:   { trait: [[0, 3], [0.25, 3], [0.42, 2.5]], suite: [[0.56, 3], [0.78, 3.8], [1, 5]], glotte: { x: 0.49, n: 2.75, signe: 'ˀ' } },
    nang:  { trait: [[0, 2], [0.3, 1.9], [0.6, 1]], glotte: { x: 0.62, n: 1, signe: 'ʔ' } }
  };
  var SVG = 'http://www.w3.org/2000/svg';
  function svg(tag, attrs, enfants) {
    var n = document.createElementNS(SVG, tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    (enfants || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  // Courbe douce passant par les points (segments quadratiques par les milieux).
  function cheminDoux(pts, X, Y) {
    if (pts.length === 2) return 'M' + X(pts[0][0]) + ' ' + Y(pts[0][1]) + ' L' + X(pts[1][0]) + ' ' + Y(pts[1][1]);
    var d = 'M' + X(pts[0][0]) + ' ' + Y(pts[0][1]);
    for (var i = 1; i < pts.length - 1; i++) {
      var mx = (X(pts[i][0]) + X(pts[i + 1][0])) / 2, my = (Y(pts[i][1]) + Y(pts[i + 1][1])) / 2;
      d += ' Q' + X(pts[i][0]) + ' ' + Y(pts[i][1]) + ' ' + (i === pts.length - 2 ? X(pts[i + 1][0]) + ' ' + Y(pts[i + 1][1]) : mx + ' ' + my);
    }
    return d;
  }
  // Ajoute le schéma d'un ton dans un <svg> déjà dessiné (grille comprise).
  function tracerTon(g, code, couleur, X, Y, epaisseur, opacite) {
    var s = SCHEMAS_TONS[code];
    if (!s) return;
    var groupe = svg('g', { stroke: couleur, fill: 'none', 'stroke-width': epaisseur, 'stroke-linecap': 'round', opacity: opacite });
    groupe.appendChild(svg('path', { d: cheminDoux(s.trait, X, Y) }));
    if (s.suite) groupe.appendChild(svg('path', { d: cheminDoux(s.suite, X, Y) }));
    if (s.option) groupe.appendChild(svg('path', { d: cheminDoux(s.option, X, Y), 'stroke-dasharray': '2 5' }));
    if (s.glotte) {
      var gx = X(s.glotte.x), gy = Y(s.glotte.n);
      if (code === 'nang') groupe.appendChild(svg('path', { d: 'M' + gx + ' ' + (gy - 9) + ' L' + gx + ' ' + (gy + 5) }));
      var t = svg('text', { x: gx, y: gy - 12, 'text-anchor': 'middle', fill: couleur, stroke: 'none', 'font-size': 16, 'font-weight': 700 });
      t.textContent = s.glotte.signe;
      groupe.appendChild(t);
    }
    g.appendChild(groupe);
  }
  // Grille des 5 niveaux ; renvoie { racine, X, Y } pour y tracer des tons.
  function grilleTons(largeur, hauteur, avecEtiquettes) {
    var mg = avecEtiquettes ? 40 : 8, mh = 14, mb = 10;
    var X = function (x) { return Math.round(mg + x * (largeur - mg - 10)); };
    var Y = function (n) { return Math.round(mh + (5 - n) / 4 * (hauteur - mh - mb)); };
    var racine = svg('svg', { viewBox: '0 0 ' + largeur + ' ' + hauteur, class: 'schema-ton', role: 'img' });
    for (var n = 1; n <= 5; n++) {
      racine.appendChild(svg('line', { x1: mg, x2: largeur - 10, y1: Y(n), y2: Y(n), class: 'grille-ton' + (n === 3 ? ' milieu' : '') }));
      if (avecEtiquettes) {
        var t = svg('text', { x: 4, y: Y(n) + 4, class: 'etiquette-ton' });
        t.textContent = n === 5 ? '5 aigu' : n === 1 ? '1 grave' : String(n);
        racine.appendChild(t);
      }
    }
    return { racine: racine, X: X, Y: Y };
  }

  function ecranTons(retour) {
    arreterSon();
    var R = D.reference_tons || [];
    var voixDispo = ['F1', 'H3'].filter(function (v) { return R.some(function (t) { return t.audio && t.audio[v]; }); });
    var codeVoix = voixDispo[0] || 'F1', debit = 'normal', choisi = -1;
    vider();
    btnRetour.hidden = false;
    btnRetour.onclick = function () { arreterSon(); retour(); };
    titreBarre.textContent = 'Les 6 tons';
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Référence' }),
      el('h1', { text: 'Les 6 tons sur une même syllabe' }),
      el('p', { class: 'petit', text: 'Seule la mélodie change : ma, má, mà, mả, mã, mạ. Chaque schéma montre comment la voix évolue, du début à la fin du mot, entre grave (1) et aigu (5).' })
    ]));
    if (!R.length) { app.appendChild(el('p', { text: 'Série des tons absente des données (reference_tons.csv).' })); return; }

    // Choix de la voix et du débit (pour l'écoute).
    function groupe(options, valeur, choisir) {
      var boutons = options.map(function (o) {
        var b = el('button', { class: 'choix-voix' + (o[0] === valeur ? ' choisi' : ''), type: 'button', text: o[1],
          'aria-pressed': o[0] === valeur ? 'true' : 'false', onclick: function () {
            boutons.forEach(function (x) { var oui = x === b; x.classList.toggle('choisi', oui); x.setAttribute('aria-pressed', oui ? 'true' : 'false'); });
            choisir(o[0]);
          } });
        return b;
      });
      return el('div', { class: 'choix-voix-groupe', role: 'group' }, boutons);
    }
    var noms = { F1: '👩 Ban Mai', H3: '👨 Le Minh' };
    if (voixDispo.length > 1) app.appendChild(groupe(voixDispo.map(function (v) { return [v, noms[v] || v]; }), codeVoix, function (v) { codeVoix = v; }));
    app.appendChild(groupe([['normal', '▶ Débit normal'], ['slow', '🐢 Débit lent']], debit, function (d) { debit = d; }));

    // Grand schéma : les 6 tons ensemble ; celui qu'on écoute est mis en avant.
    var cadre = el('div', { class: 'cadre-courbe' });
    function grandSchema() {
      cadre.innerHTML = '';
      var gr = grilleTons(320, 170, true);
      gr.racine.setAttribute('aria-label', 'Schéma des 6 tons');
      R.forEach(function (t, i) {
        if (i !== choisi) tracerTon(gr.racine, t.ton, t.couleur, gr.X, gr.Y, 3, choisi < 0 ? 0.9 : 0.18);
      });
      if (choisi >= 0) tracerTon(gr.racine, R[choisi].ton, R[choisi].couleur, gr.X, gr.Y, 5, 1);
      cadre.appendChild(gr.racine);
      cadre.appendChild(el('p', { class: 'petit', text: 'ˀ : coup de glotte au milieu (ngã) ; ʔ : arrêt net en fin de mot (nặng). Pointillés : remontée faible ou absente à Hanoï (hỏi).' }));
    }
    app.appendChild(cadre);

    // Cartes des 6 tons : schéma, syllabe, nom ; toucher une carte joue la syllabe.
    var grille = el('div', { class: 'tuiles trois tons-grille' });
    var cartes = R.map(function (t, i) {
      var petit = grilleTons(100, 80, false);
      tracerTon(petit.racine, t.ton, t.couleur, petit.X, petit.Y, 3.5, 1);
      petit.racine.setAttribute('aria-hidden', 'true');
      var b = el('button', { class: 'tuile carte-ton', type: 'button', 'aria-label': 'ton ' + t.nom + ', ' + t.ecrit,
        onclick: function () { choisir(i); dire(i); } }, [
        petit.racine,
        el('span', { class: 'ecrit', text: t.ecrit }),
        el('span', { class: 'nom-ton', text: t.pictogramme + ' ' + t.nom }),
        el('span', { class: 'sens', text: t.contour })
      ]);
      b.querySelector('.nom-ton').style.color = t.couleur;
      b.style.borderTopColor = t.couleur;
      grille.appendChild(b);
      return b;
    });
    var tous = el('button', { class: 'ecoute', type: 'button', text: '▶ Les 6 à la suite', onclick: function () {
      tous.disabled = true;
      var seq = Promise.resolve();
      R.forEach(function (t, i) { seq = seq.then(function () { choisir(i); return dire(i); }).then(function () { return pause(600); }); });
      seq.then(function () { choisir(-1); tous.disabled = false; });
    } });
    app.appendChild(el('div', { class: 'actions centre' }, [tous]));
    app.appendChild(grille);

    function dire(i) { var t = R[i]; return jouer({ ecrit: t.ecrit, audio: t.audio }, codeVoix, debit, cartes[i]); }   // info de test dans la carte
    function choisir(i) {
      choisi = i;
      cartes.forEach(function (b, k) { b.classList.toggle('joue', k === i); });
      grandSchema();
    }
    grandSchema();
  }

  /* ---------- 12. Écran : réglages (enregistrés avec la progression) ---------- */
  function ecranReglages() {
    arreterSon();
    var R = reglages();
    vider();
    btnRetour.hidden = false;
    btnRetour.onclick = ecranAccueil;
    titreBarre.textContent = 'Réglages';
    app.appendChild(el('div', { class: 'consigne' }, [el('h1', { text: 'Réglages' }),
      el('p', { class: 'petit', text: 'Enregistrés sur cet appareil.' })]));
    // ligne() : une ligne de réglage (titre, aide, contrôle) ; interrupteur() : case à cocher
    // reliée à un réglage, enregistrée à chaque changement.
    function ligne(id, titre, aide, controle) {
      return el('div', { class: 'etape reglage' }, [
        el('div', { class: 'reglage-texte' }, [el('label', { for: id, text: titre }), el('p', { class: 'petit', text: aide })]),
        controle
      ]);
    }
    function interrupteur(id, cle) {
      var c = el('input', { type: 'checkbox', id: id, class: 'interrupteur' });
      c.checked = !!R[cle];
      c.addEventListener('change', function () { R[cle] = c.checked; sauver(); appliquerReglages(); });
      return c;
    }
    var vit = el('select', { id: 'reglage-vitesse' }, [
      el('option', { value: '0.8', text: 'Plus lente' }), el('option', { value: '1', text: 'Normale' }), el('option', { value: '1.2', text: 'Plus rapide' })]);
    vit.value = String(R.vitesse);
    vit.addEventListener('change', function () { R.vitesse = parseFloat(vit.value); sauver(); });
    var essai = el('button', { class: 'bouton second', type: 'button', text: '▶ Essayer', onclick: function () {
      var t = D.lecons[0].series[0].termes[0]; jouer(t, D.voix[0].code, 'slow');
    } });
    app.appendChild(el('div', { class: 'etapes' }, [
      ligne('reglage-vitesse', 'Vitesse de la voix de synthèse', 'Agit sur la voix provisoire de l’appareil, pas sur les enregistrements.', el('div', { class: 'actions' }, [vit, essai])),
      ligne('reglage-auto', 'Question suivante automatique', 'Après une bonne réponse, passer seul à la question suivante.', interrupteur('reglage-auto', 'suivantAuto')),
      ligne('reglage-aides', 'Aides sous les symboles', 'Mot repère et indice d’écoute en E1, repère au débit lent. La catégorie (= ≈ ★) reste affichée.', interrupteur('reglage-aides', 'aides')),
      ligne('reglage-texte', 'Grand texte', 'Agrandit le texte et les symboles.', interrupteur('reglage-texte', 'grandTexte')),
      ligne('reglage-ouvert', 'Mode essai : tout ouvert', 'Toutes les leçons et toutes les étapes accessibles, sans attendre les verrous. Les scores restent calculés. À couper avant d’ouvrir la formation à d’autres apprenants.', interrupteur('reglage-ouvert', 'toutOuvert')),
      ligne('reglage-info', 'Infos de test sur le son', 'Pendant les essais : dans la case du mot joué, fichier, personnage, femme ou homme, modèle FPT et vitesse (en E2–E3, après la réponse).', interrupteur('reglage-info', 'infoTest'))
    ]));
  }

  /* ---------- 13. Écran : mes progrès ----------
     Calculé à partir de l'historique des réponses d'E2 et E3 (toutes parties) :
     par jour, par série (les plus difficiles d'abord), confusions fréquentes.
     L'échauffement et E1 ne sont pas comptés. */
  function jour(ms) { var d = new Date(ms); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function jourFr(j) { var x = j.split('-'); return x[2] + '/' + x[1]; }
  function barre(part, classe) {
    var b = el('span', { class: 'barre-mesure' + (classe ? ' ' + classe : '') }, [el('span')]);
    b.firstChild.style.width = Math.round(Math.max(0, Math.min(1, part)) * 100) + '%';
    return b;
  }
  function ecranProgres(code) {
    arreterSon();
    var l = trouverLecon(code);
    var etatL = etatLecon(code);
    vider();
    btnRetour.onclick = function () { ecranLecon(code); };
    titreBarre.textContent = 'Leçon ' + l.numero + ' · Progrès';
    app.appendChild(el('div', { class: 'consigne' }, [el('span', { class: 'etiquette', text: 'Leçon ' + l.numero }), el('h1', { text: 'Mes progrès' })]));

    // Toutes les réponses de la leçon, toutes parties et étapes confondues
    // toutes = toutes les réponses d'E2 et E3 de la leçon, avec leur étape et leur partie.
    var toutes = [];
    l.parties.forEach(function (pa) {
      var ep = etatL.parties[pa.code];
      if (!ep) return;
      ['e2', 'e3'].forEach(function (cle) { ep[cle].hist.forEach(function (h) { toutes.push({ h: h, etape: cle, partie: pa }); }); });
    });
    if (!toutes.length) {
      app.appendChild(el('p', { text: 'Pas encore de réponses dans cette leçon. Les progrès apparaîtront dès vos premières réponses en E2.' }));
      return;
    }

    // 1. Par jour : réponses, réussite, temps (écarts de moins de 2 min entre deux réponses)
    // Temps de travail estimé : somme des écarts de moins de 2 minutes entre deux réponses du même jour.
    var parJour = {};
    var datees = toutes.filter(function (x) { return x.h.t; }).sort(function (a, b) { return a.h.t - b.h.t; });
    datees.forEach(function (x, i) {
      var j = jour(x.h.t);
      var d = parJour[j] = parJour[j] || { n: 0, ok: 0, ms: 0 };
      d.n++; if (x.h.ok) d.ok++;
      if (i > 0) { var ecart = x.h.t - datees[i - 1].h.t; if (ecart < 120000 && jour(datees[i - 1].h.t) === j) d.ms += ecart; }
    });
    var jours = Object.keys(parJour).sort();
    var sec1 = el('div', { class: 'etape' }, [el('h2', { text: 'Par jour' })]);
    if (!jours.length) sec1.appendChild(el('p', { class: 'petit', text: 'Le détail par jour commence avec les réponses données à partir de cette version.' }));
    var tab1 = el('div', { class: 'tableau' });
    tab1.appendChild(el('div', { class: 'tab-ligne tab-tete' }, [el('span', { text: 'Jour' }), el('span', { text: 'Réponses' }), el('span', { text: 'Temps' }), el('span', { text: 'Réussite' })]));
    jours.slice(-14).forEach(function (j) {
      var d = parJour[j];
      tab1.appendChild(el('div', { class: 'tab-ligne' }, [
        el('span', { text: jourFr(j) }), el('span', { text: String(d.n) }),
        el('span', { text: Math.max(1, Math.round(d.ms / 60000)) + ' min' }),
        el('span', { class: 'tab-barre' }, [barre(d.ok / d.n), el('span', { text: pourcent(d.ok / d.n) })])
      ]));
    });
    if (jours.length) sec1.appendChild(tab1);
    app.appendChild(sec1);

    // 2. Par série : réussite au débit normal (là où se mesure le verrou), sinon toutes
    var sec2 = el('div', { class: 'etape' }, [el('h2', { text: 'Par série' }),
      el('p', { class: 'petit', text: 'Réussite sur les réponses au débit normal (au débit lent s’il n’y en a pas encore). Les séries les plus difficiles en premier.' })]);
    var stats = l.series.map(function (s) {
      var hs = toutes.filter(function (x) { return x.h.s === s.code; });
      var norm = hs.filter(function (x) { return x.h.d === 'normal'; });
      var base = norm.length ? norm : hs;
      var ok = base.filter(function (x) { return x.h.ok; }).length;
      return { s: s, n: base.length, taux: base.length ? ok / base.length : null, normal: norm.length > 0 };
    }).filter(function (x) { return x.n > 0; }).sort(function (a, b) { return a.taux - b.taux; });
    var tab2 = el('div', { class: 'tableau' });
    stats.forEach(function (x) {
      var nom = (x.s.termes[0].image ? x.s.termes[0].image + ' ' : '') + x.s.termes.map(function (t) { return t.symbole.texte; }).join(' – ');
      tab2.appendChild(el('div', { class: 'tab-ligne tab-serie' }, [
        el('span', { class: 'symbole-petit', text: nom }),
        el('span', { class: 'petit', text: x.n + ' rép.' + (x.normal ? '' : ' (lent)') }),
        el('span', { class: 'tab-barre' }, [barre(x.taux, x.taux < l.seuil ? 'faible' : ''), el('span', { text: pourcent(x.taux) })])
      ]));
    });
    sec2.appendChild(tab2);
    app.appendChild(sec2);

    // 3. Confusions : « vous avez choisi X alors que c'était Y »
    // Confusions : pour chaque erreur, « attendu → choisi », comptées et triées.
    var conf = {};
    toutes.forEach(function (x) {
      if (x.h.ok || x.h.c == null || x.h.r == null || x.h.c < 0 || x.h.r < 0) return;
      var s = l.series.filter(function (z) { return z.code === x.h.s; })[0];
      if (!s) return;
      var cle = s.termes[x.h.c].symbole.texte + '→' + s.termes[x.h.r].symbole.texte;
      conf[cle] = conf[cle] || { attendu: s.termes[x.h.c].symbole.texte, choisi: s.termes[x.h.r].symbole.texte, n: 0 };
      conf[cle].n++;
    });
    var liste = Object.keys(conf).map(function (k) { return conf[k]; }).sort(function (a, b) { return b.n - a.n; }).slice(0, 6);
    var sec3 = el('div', { class: 'etape' }, [el('h2', { text: 'Confusions fréquentes' })]);
    if (!liste.length) sec3.appendChild(el('p', { class: 'petit', text: 'Aucune confusion enregistrée pour l’instant.' }));
    liste.forEach(function (c) {
      sec3.appendChild(el('p', {}, [
        el('span', { class: 'symbole-petit', text: c.attendu }), ' entendu, ',
        el('span', { class: 'symbole-petit', text: c.choisi }), ' choisi : ',
        el('b', { text: c.n + ' fois' })
      ]));
    });
    app.appendChild(sec3);
  }

  /* ---------- 14. Démarrage ----------
     LecteurOutils : quelques fonctions rendues visibles pour les essais automatiques.
     ecranAccueil() : premier écran affiché. */
  window.LecteurOutils = { Stockage: Stockage, mesure: mesure, verifierPassages: verifierPassages };
  ecranAccueil();
})();
