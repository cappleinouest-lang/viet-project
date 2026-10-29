/*
 * Lecteur d'activités — Module 0, volet écoute (E1 → E3).
 * Règles appliquées : PROG-ACT, R-PARC-01 à 05, R-ECR-01/02, R-LEX-06, R-VOL-02/05 à 07,
 * DEC-0028/0029 (étiquettes), DEC-0032 (minimum par série), DEC-0033 (positions 1 et 2 en E2),
 * DEC-0037 (leçon en deux parties).
 * Données : window.DONNEES_LECTEUR, produit par 05_PRODUCTION/tools/generer_lecteur.py.
 * Ne pas modifier les contenus ici : ils viennent de 04_DONNEES.
 */
(function () {
  'use strict';

  var D = window.DONNEES_LECTEUR;
  var P = D.parametres;
  var app = document.getElementById('app');
  var titreBarre = document.getElementById('barre-titre');
  var btnRetour = document.getElementById('btn-retour');
  var bandeau = document.getElementById('bandeau-voix');
  var pied = document.getElementById('pied');

  /* ---------- Enregistrement de la progression (seul endroit à remplacer
     pour passer à WordPress ou Firebase : DEC-0030) ---------- */
  var CLE = 'viet-lecteur-progression-v1';
  var memoire = null;
  var Stockage = {
    charger: function () {
      try {
        var t = window.localStorage.getItem(CLE);
        if (t) return JSON.parse(t);
      } catch (e) { /* stockage indisponible : on garde la progression en mémoire */ }
      return memoire || { version: 2, lecons: {} };
    },
    enregistrer: function (p) {
      memoire = p;
      try { window.localStorage.setItem(CLE, JSON.stringify(p)); } catch (e) { /* idem */ }
    }
  };

  function trouverLecon(code) { return D.lecons.filter(function (l) { return l.code === code; })[0]; }
  function seriesDe(l, partie) {
    return l.series.filter(function (s) { return partie.series.indexOf(s.code) >= 0; });
  }
  function etatEtape() { return { debit: 'slow', hist: [], reussites: {}, validee: false }; }
  function etatPartieNeuf() { return { e1: { vues: [] }, e2: etatEtape(), e3: etatEtape(), ecrit: false }; }

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
  var prog = migrer(Stockage.charger());

  function etatLecon(code) {
    if (!prog.lecons[code]) prog.lecons[code] = { parties: {}, ecouteValideeLe: null };
    return prog.lecons[code];
  }
  function etatPartie(code, pc) {
    var e = etatLecon(code);
    if (!e.parties[pc]) e.parties[pc] = etatPartieNeuf();
    return e.parties[pc];
  }
  function sauver() { Stockage.enregistrer(prog); }

  /* ---------- Outils ---------- */
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
  function vider() { app.innerHTML = ''; window.scrollTo(0, 0); }
  function hasard(n) { return Math.floor(Math.random() * n); }
  function melanger(t) { t = t.slice(); for (var i = t.length - 1; i > 0; i--) { var j = hasard(i + 1); var x = t[i]; t[i] = t[j]; t[j] = x; } return t; }
  function pourcent(x) { return Math.round(x * 100) + ' %'; }
  function nomPartie(l, pa) { return l.parties.length > 1 ? 'Partie ' + pa.code + ' · ' + pa.titre : ''; }
  function titreEcran(l, pa, etape) {
    return 'Leçon ' + l.numero + (l.parties.length > 1 ? pa.code : '') + ' · ' + etape;
  }

  /* ---------- Audio : fichier validé si présent, sinon voix de synthèse (provisoire) ---------- */
  var voixVi = null;
  function chercherVoix() {
    if (!('speechSynthesis' in window)) return;
    var v = window.speechSynthesis.getVoices().filter(function (x) { return /^vi/i.test(x.lang); });
    voixVi = v.length ? v[0] : null;
    afficherBandeau();
  }
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

  var lectureEnCours = null;
  function jouer(terme, codeVoix, debit) {
    return new Promise(function (resolve) {
      var fini = false;
      function fin() { if (!fini) { fini = true; resolve(); } }
      var f = terme.audio[codeVoix] && terme.audio[codeVoix][debit];
      if (f) {
        if (lectureEnCours) lectureEnCours.pause();
        var a = new Audio(f);
        lectureEnCours = a;
        a.onended = fin; a.onerror = fin;
        a.play().catch(fin);
        setTimeout(fin, 6000);
        return;
      }
      if (!('speechSynthesis' in window)) { fin(); return; }
      var v = D.voix.filter(function (x) { return x.code === codeVoix; })[0] || D.voix[0];
      var u = new SpeechSynthesisUtterance(terme.ecrit);
      u.lang = 'vi-VN';
      if (voixVi) u.voice = voixVi;
      u.pitch = v.hauteur || 1;
      u.rate = (D.debits[debit] || 0.9) * (v.vitesse || 1);
      u.onend = fin; u.onerror = fin;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
      setTimeout(fin, 5000);
    });
  }
  function arreterSon() {
    if (lectureEnCours) lectureEnCours.pause();
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  }
  function pause(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function voixAuHasard(sauf) {
    var c = D.voix.map(function (v) { return v.code; }).filter(function (x) { return x !== sauf; });
    return c.length ? c[hasard(c.length)] : D.voix[0].code;
  }

  /* ---------- Affichage d'un terme ---------- */
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
    var img = t.image ? el('span', { class: 'image', text: t.image, 'aria-hidden': 'true' }) : null;
    if (mode === 'ecrit') {
      if (img) morceaux.push(img);
      morceaux.push(t.invente ? el('span', { class: 'ecrit', text: '🔊' }) : el('span', { class: 'ecrit', text: t.ecrit }));
      morceaux.push(el('span', { class: 'sens', text: t.invente ? 'syllabe inventée (jamais écrite)' : t.sens }));
      return morceaux;
    }
    if (img) morceaux.push(img);
    morceaux.push(sym);
    var r = t.symbole.repere;
    if (r && r.image && avecIndices) {
      // Mot repère (DEC-0038) : français écrit ; vietnamien en image seulement (pas d'écrit en E1–E2).
      morceaux.push(el('span', { class: 'repere' + (mode === 'lent' ? ' petit-repere' : ''), title: 'mot repère' }, [
        el('span', { 'aria-hidden': 'true', text: r.langue === 'fr' ? '🇫🇷 ' : '🇻🇳 ' }),
        el('span', { text: r.image + (r.mot && mode === 'decouverte' ? ' ' + r.mot : '') })
      ]));
    }
    if (mode === 'decouverte') {
      if (t.symbole.indication) morceaux.push(el('span', { class: 'indication', text: t.symbole.indication }));
      if (t.sens) morceaux.push(el('span', { class: 'sens', text: 'mot entendu : ' + t.sens }));
    }
    return morceaux;
  }
  var MARQUES = { identique: '=', proche: '≈', nouveau: '★' };
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
  function nomAccessible(t) {
    return (t.sens ? t.sens + ', ' : '') + 'symbole ' + t.symbole.texte;  // ne pas modifier : utilisé par les essais automatiques
  }
  function classeTuiles(n) { return 'tuiles' + (n === 3 ? ' trois' : n === 4 ? ' quatre' : ''); }

  /* ---------- Calcul des scores et des verrous ---------- */
  function mesure(etat, debit) {
    var h = etat.hist.filter(function (x) { return x.d === debit; }).slice(-P.fenetre_score);
    var justes = h.filter(function (x) { return x.ok; }).length;
    var voix = {};
    h.forEach(function (x) { voix[x.v] = true; });
    return { n: h.length, justes: justes, taux: h.length ? justes / h.length : 0, voix: Object.keys(voix).length };
  }
  function seriesCouvertes(series, etat) {
    return series.filter(function (s) { return (etat.reussites[s.code] || 0) >= P.min_reussites_par_serie; }).length;
  }
  function verifierPassages(seuil, series, etat) {
    var m = mesure(etat, etat.debit);
    var seuilAtteint = m.n >= P.fenetre_score && m.taux >= seuil;
    if (etat.debit === 'slow' && seuilAtteint) { etat.debit = 'normal'; return 'normal'; }
    if (etat.debit === 'normal' && seuilAtteint && m.voix >= P.min_voix && seriesCouvertes(series, etat) === series.length && !etat.validee) {
      etat.validee = true; return 'validee';
    }
    return null;
  }

  /* ---------- Écran : liste des leçons ---------- */
  function leconOuverte(i) {
    if (i === 0) return true;
    var prec = prog.lecons[D.lecons[i - 1].code];
    return !!(prec && prec.ecouteValideeLe);
  }
  function ecranAccueil() {
    arreterSon();
    vider();
    btnRetour.hidden = true;
    titreBarre.textContent = 'Vietnamien · Module 0';
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Volet écoute' }),
      el('h1', { text: 'Les sons et les tons' }),
      el('p', { class: 'petit', text: 'Chaque leçon s’ouvre quand l’écoute de la précédente est validée. 20 à 30 minutes par jour suffisent.' })
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
    pied.textContent = 'Données générées le ' + D.genere_le + '. Progression enregistrée dans ce navigateur, sur cet appareil.';
  }

  /* ---------- Écran : une leçon ---------- */
  function partieTerminee(code, pa) { var e = etatLecon(code).parties[pa.code]; return !!(e && e.ecrit); }

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

    l.parties.forEach(function (pa, k) {
      var series = seriesDe(l, pa);
      var etat = etatPartie(code, pa.code);
      var partieOuverte = k === 0 || partieTerminee(code, l.parties[k - 1]);
      var etapes = el('div', { class: 'etapes' });
      if (l.parties.length > 1) {
        etapes.appendChild(el('div', { class: 'partie-tete' }, [
          el('h2', { text: nomPartie(l, pa) }),
          el('span', { class: 'pastille' + (etat.ecrit ? ' ok' : partieOuverte ? '' : ' ferme'),
            text: etat.ecrit ? 'Validée' : partieOuverte ? series.length + ' séries' : 'Après la partie ' + l.parties[k - 1].code })
        ]));
      }
      var e1Fait = etat.e1.vues.length >= series.length;
      etapes.appendChild(blocEtape('E1 · Écouter', 'Écoutez chaque série, sans répondre.',
        etat.e1.vues.length + ' / ' + series.length + ' séries', etat.e1.vues.length / series.length,
        e1Fait ? 'Réécouter' : 'Commencer', partieOuverte, function () { ecranE1(code, pa.code, 0); }));

      [['e2', 'E2 · Distinguer', 'Lequel avez-vous entendu ? Deux choix.'], ['e3', 'E3 · Opposer', 'Lequel avez-vous entendu ? Toute la série.']].forEach(function (x, j) {
        var e = etat[x[0]];
        var m = mesure(e, e.debit);
        var ouvert = partieOuverte && (j === 0 ? e1Fait : etat.e2.validee);
        var texte = e.validee ? 'Validée' :
          'Débit ' + (e.debit === 'slow' ? 'lent' : 'normal') + ' · ' + m.justes + ' justes sur les ' + m.n + ' dernières' +
          (e.debit === 'normal' ? ' · séries réussies 2 fois : ' + seriesCouvertes(series, e) + ' / ' + series.length : '');
        etapes.appendChild(blocEtape(x[1], x[2], texte, e.validee ? 1 : Math.min(1, m.taux * Math.min(1, m.n / P.fenetre_score) / l.seuil),
          e.validee ? 'Refaire' : 'Continuer', ouvert, function () { ecranQuiz(code, pa.code, x[0]); }));
      });

      etapes.appendChild(blocEtape('Fin d’E3 · L’écrit', 'Découvrez comment s’écrivent les mots entendus.',
        etat.ecrit ? 'Vu' : 'Après la validation d’E3', etat.ecrit ? 1 : 0,
        'Voir l’écrit', partieOuverte && etat.e3.validee, function () { ecranEcrit(code, pa.code); }));
      app.appendChild(etapes);
    });

    var resume = el('div', { class: 'etapes' });
    resume.appendChild(el('div', { class: 'etape' }, [
      el('div', { class: 'etape-tete' }, [el('h2', { text: 'Écoute de la leçon' }),
        el('span', { class: 'pastille' + (etatL.ecouteValideeLe ? ' ok' : ' ferme'), text: etatL.ecouteValideeLe ? 'Validée le ' + etatL.ecouteValideeLe : 'Pas encore validée' })]),
      el('p', { class: 'petit', text: 'Valider l’écoute ouvre la leçon suivante.' })
    ]));
    resume.appendChild(el('div', { class: 'etape' }, [
      el('div', { class: 'etape-tete' }, [el('h2', { text: 'E4–E5 · Répéter, stabiliser' }), el('span', { class: 'pastille ferme', text: 'À venir' })]),
      el('p', { class: 'petit', text: 'Le volet production (micro, courbe mélodique) sera ajouté ensuite.' })
    ]));
    app.appendChild(resume);

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
  function partieDe(l, pc) { return l.parties.filter(function (p) { return p.code === pc; })[0]; }

  /* ---------- E1 : écoute des séries (découverte + écoute contrastée) ---------- */
  function ecranE1(code, pc, index) {
    arreterSon();
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var series = seriesDe(l, pa);
    var etat = etatPartie(code, pc);
    var s = series[index];
    vider();
    btnRetour.onclick = function () { ecranLecon(code); };
    titreBarre.textContent = titreEcran(l, pa, 'E1 Écouter');
    var groupe = l.tons ? 'tons' : ['voyelles', 'consonnes', 'finales', 'autres'][s.groupe];
    app.appendChild(el('div', { class: 'consigne' }, [
      el('span', { class: 'etiquette', text: 'Série ' + (index + 1) + ' sur ' + series.length + ' · ' + groupe }),
      el('h1', { text: 'Écoutez, sans répondre' }),
      el('p', { class: 'petit', text: 'Touchez une case pour la réentendre. Chaque son est dit par plusieurs voix, lentement.' })
    ]));
    var grille = el('div', { class: classeTuiles(s.termes.length) });
    var tours = {};
    var tuiles = s.termes.map(function (t, i) {
      var b = el('button', { class: 'tuile', type: 'button', 'aria-label': nomAccessible(t), onclick: function () {
        tours[i] = ((tours[i] || 0) + 1) % D.voix.length;
        surligner(i); jouer(t, D.voix[tours[i]].code, 'slow').then(function () { surligner(-1); });
      } }, contenuTerme(t, 'decouverte'));
      grille.appendChild(b);
      return b;
    });
    function surligner(k) { tuiles.forEach(function (b, i) { b.classList.toggle('joue', i === k); }); }
    var suivant = el('button', { class: 'bouton', type: 'button', disabled: etat.e1.vues.indexOf(s.code) < 0,
      text: index + 1 < series.length ? 'Série suivante' : 'Terminer E1',
      onclick: function () { if (index + 1 < series.length) ecranE1(code, pc, index + 1); else ecranLecon(code); } });
    var ecoute = el('button', { class: 'ecoute', type: 'button', text: '▶ Écouter la série', onclick: function () {
      ecoute.disabled = true;
      // Chaque terme avec chaque voix ; la paire d'E2 (positions 1 et 2) en premier.
      var seq = Promise.resolve();
      D.voix.forEach(function (v) {
        s.termes.forEach(function (t, i) {
          seq = seq.then(function () { surligner(i); return jouer(t, v.code, 'slow'); }).then(function () { return pause(350); });
        });
      });
      seq.then(function () {
        surligner(-1); ecoute.disabled = false;
        if (etat.e1.vues.indexOf(s.code) < 0) { etat.e1.vues.push(s.code); sauver(); }
        suivant.disabled = false;
      });
    } });
    app.appendChild(ecoute);
    app.appendChild(grille);
    var lg = legende([s]); if (lg) app.appendChild(lg);
    app.appendChild(el('div', { class: 'actions' }, [suivant]));
  }

  /* ---------- E2 et E3 : « Lequel ? » ---------- */
  function ecranQuiz(code, pc, cle) {
    var l = trouverLecon(code);
    var pa = partieDe(l, pc);
    var series = seriesDe(l, pa);
    var e = etatPartie(code, pc)[cle];
    var derniereVoix = null;
    var positionsJustes = [];

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
      var voix = voixAuHasard(derniereVoix);
      derniereVoix = voix;
      afficherItem(s, ordre, cible, voix);
    }

    function afficherItem(s, ordre, cible, voix) {
      vider();
      btnRetour.onclick = function () { ecranLecon(code); };
      titreBarre.textContent = titreEcran(l, pa, cle === 'e2' ? 'E2 Distinguer' : 'E3 Opposer');
      var debit = e.debit;
      var m = mesure(e, debit);
      app.appendChild(el('div', { class: 'mesures' }, [
        el('div', { class: 'mesure' }, [el('b', { text: debit === 'slow' ? 'Lent' : 'Normal' }), el('span', { text: 'débit' })]),
        el('div', { class: 'mesure' }, [el('b', { text: m.justes + ' / ' + m.n }), el('span', { text: 'justes · objectif ' + pourcent(l.seuil) + ' sur ' + P.fenetre_score })]),
        el('div', { class: 'mesure' }, [el('b', { text: debit === 'normal' ? seriesCouvertes(series, e) + ' / ' + series.length : '—' }), el('span', { text: 'séries réussies 2 fois' })])
      ]));
      var ecoute = el('button', { class: 'ecoute', type: 'button', text: '▶ Réécouter', onclick: function () { jouer(cible, voix, debit); } });
      app.appendChild(el('div', { class: 'consigne' }, [el('h1', { text: 'Lequel avez-vous entendu ?' })]));
      app.appendChild(ecoute);
      var mode = debit === 'slow' ? 'lent' : 'normal';
      var grille = el('div', { class: classeTuiles(ordre.length) });
      var retour = el('p', { class: 'retour-reponse', role: 'status' });
      var repondu = false;
      var suivant = el('button', { class: 'bouton', type: 'button', text: 'Suivant', hidden: true, onclick: nouvelItem });
      var tuiles = ordre.map(function (t) {
        var cls = 'tuile' + (mode === 'normal' ? ' symbole-seul' : '');
        var b = el('button', { class: cls, type: 'button', 'aria-label': nomAccessible(t), onclick: function () {
          if (repondu) { jouer(t, voix, debit); return; }
          repondu = true;
          var ok = t === cible;
          e.hist.push({ s: s.code, ok: ok, v: voix, d: debit });
          if (e.hist.length > 400) e.hist = e.hist.slice(-400);
          if (ok && debit === 'normal') e.reussites[s.code] = (e.reussites[s.code] || 0) + 1;
          var passage = verifierPassages(l.seuil, series, e);
          sauver();
          tuiles[ordre.indexOf(cible)].classList.add('juste');
          if (ok) {
            retour.className = 'retour-reponse juste'; retour.textContent = 'Juste.';
            jouer(cible, voix, debit);
          } else {
            b.classList.add('faux');
            retour.className = 'retour-reponse faux'; retour.textContent = 'C’était l’autre. Écoutez les deux.';
            jouer(cible, voix, debit).then(function () { return pause(400); }).then(function () { return jouer(t, voix, debit); });
          }
          suivant.hidden = false;
          if (passage === 'normal') retour.textContent += ' Seuil atteint au débit lent : on passe au débit normal, avec les symboles seuls.';
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
      setTimeout(function () { jouer(cible, voix, debit); }, 250);
    }

    nouvelItem();
  }

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
        g.appendChild(el('button', { class: 'tuile', type: 'button', 'aria-label': t.invente ? 'syllabe inventée' : t.ecrit,
          onclick: function () { jouer(t, D.voix[0].code, 'normal'); } }, contenuTerme(t, 'ecrit')));
      });
      app.appendChild(g);
    });
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

  window.LecteurOutils = { Stockage: Stockage, mesure: mesure, verifierPassages: verifierPassages };
  ecranAccueil();
})();
