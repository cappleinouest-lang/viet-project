/*
 * prononciation.js — briques du volet production (E4), version d'essai
 * ---------------------------------------------------------------------------
 * Rôle : enregistrer la voix de l'élève au micro, calculer la COURBE MÉLODIQUE
 * (hauteur de la voix au fil du temps) d'un son, et la dessiner à côté de
 * celle du modèle. Aucun service extérieur : tout se fait dans le navigateur.
 *
 * Utilisé par : essai_micro.html (page d'essai) ; plus tard par lecteur.js (E4).
 * Décisions : DEC-0049 (E4 d'abord, sur PC) ; règles R-AUD-03 (un modèle unique),
 * R-VOL-08 (verrou de production : la courbe est une AIDE, sans seuil automatique).
 *
 * Sommaire
 *   1. Micro       : autorisation, niveau en direct, enregistrement (MediaRecorder)
 *   2. Décodage    : enregistrement ou fichier audio -> échantillons (Float32Array)
 *   3. Hauteur     : algorithme YIN, une mesure toutes les 10 ms
 *   4. Courbe      : nettoyage, passage en demi-tons, temps ramené de 0 à 1
 *   5. Dessin      : une ou deux courbes sur un <canvas>
 *
 * Pourquoi des demi-tons autour de la hauteur moyenne ? La voix de l'élève et
 * celle du modèle n'ont pas la même hauteur ; un ton vietnamien est une FORME
 * mélodique relative à la voix de celui qui parle. On compare donc les formes :
 * 0 = hauteur médiane de la personne, +2 = deux demi-tons au-dessus, etc.
 *
 * Pourquoi le temps ramené de 0 à 1 ? Un mot dit plus lentement ou plus vite
 * garde la même forme ; on étire chaque courbe sur toute la largeur.
 */
(function (global) {
  'use strict';

  var PARAM = {
    hzMin: 70,            // voix d'homme grave
    hzMax: 500,           // voix de femme aiguë
    pas: 0.010,           // une mesure toutes les 10 ms
    fenetre: 0.030,       // chaque mesure regarde 30 ms de son
    seuilYin: 0.15,       // en dessous : la période est jugée fiable
    aperiodiciteMax: 0.35,// au-dessus : pas de voix (souffle, bruit, consonne)
    silenceRelatif: 0.08, // énergie < 8 % du maximum : silence
    fragmentMin: 4,       // morceau de voix de moins de 4 mesures (40 ms) : écarté (§ 4.2)
    sautMax: 7,           // saut de plus de 7 demi-tons en 10 ms : coupure (§ 4.2)
    frequenceTravail: 16000, // on réduit l'enregistrement à 16 kHz pour aller vite
    dureeMax: 3           // secondes d'enregistrement au plus
  };

  // ---------------------------------------------------------------------------
  // 1. Micro
  // ---------------------------------------------------------------------------

  // Diagnostic : ce que le navigateur permet, pour l'afficher à l'élève.
  function diagnostic() {
    return {
      contexteSur: !!global.isSecureContext,
      microDisponible: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
      enregistreur: typeof global.MediaRecorder !== 'undefined',
      adresse: location.protocol
    };
  }

  // Micro : objet qui garde le flux ouvert une fois autorisé.
  //   autoriser()             -> promesse ; ouvre la fenêtre d'autorisation du navigateur
  //   niveau()                -> 0 à 1, volume actuel (pour une barre de niveau)
  //   enregistrer(dureeMax)   -> promesse résolue avec un Blob audio quand on arrête
  //   arreter()               -> arrête l'enregistrement en cours
  function Micro() {
    this.flux = null;
    this.ctx = null;
    this.analyseur = null;
    this.enreg = null;
    this.minuterie = null;
  }

  Micro.prototype.autoriser = function () {
    var self = this;
    if (self.flux) return Promise.resolve();
    // Annulation d'écho et réglage automatique du volume coupés : ils déforment
    // la voix. La réduction de bruit est gardée (pièce bruyante).
    return navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: false, autoGainControl: false, noiseSuppression: true }
    }).then(function (flux) {
      self.flux = flux;
      self.ctx = new (global.AudioContext || global.webkitAudioContext)();
      var source = self.ctx.createMediaStreamSource(flux);
      self.analyseur = self.ctx.createAnalyser();
      self.analyseur.fftSize = 1024;
      source.connect(self.analyseur);
    });
  };

  Micro.prototype.niveau = function () {
    if (!this.analyseur) return 0;
    var d = new Float32Array(this.analyseur.fftSize);
    this.analyseur.getFloatTimeDomainData(d);
    var s = 0;
    for (var i = 0; i < d.length; i++) s += d[i] * d[i];
    return Math.min(1, Math.sqrt(s / d.length) * 6);
  };

  Micro.prototype.enregistrer = function (dureeMax) {
    var self = this;
    return new Promise(function (resolve, reject) {
      var morceaux = [];
      try {
        self.enreg = new MediaRecorder(self.flux);
      } catch (e) { reject(e); return; }
      self.enreg.ondataavailable = function (ev) { if (ev.data && ev.data.size) morceaux.push(ev.data); };
      self.enreg.onstop = function () {
        clearTimeout(self.minuterie);
        resolve(new Blob(morceaux, { type: self.enreg.mimeType || 'audio/webm' }));
      };
      self.enreg.onerror = function (ev) { reject(ev.error || ev); };
      self.enreg.start();
      self.minuterie = setTimeout(function () { self.arreter(); }, (dureeMax || PARAM.dureeMax) * 1000);
    });
  };

  Micro.prototype.arreter = function () {
    if (this.enreg && this.enreg.state === 'recording') this.enreg.stop();
  };

  Micro.prototype.enCours = function () {
    return !!(this.enreg && this.enreg.state === 'recording');
  };

  // ---------------------------------------------------------------------------
  // 2. Décodage : Blob ou File -> { echantillons, frequence }
  // ---------------------------------------------------------------------------
  // Un fichier choisi par l'élève (bouton « Choisir un fichier ») se lit même
  // quand la page est ouverte par double-clic, contrairement à fetch().
  function decoder(blob) {
    var Ctx = global.AudioContext || global.webkitAudioContext;
    var ctx = new Ctx();
    return blob.arrayBuffer().then(function (buf) {
      return ctx.decodeAudioData(buf);
    }).then(function (audio) {
      var d = audio.getChannelData(0);
      ctx.close();
      return { echantillons: d, frequence: audio.sampleRate, duree: audio.duration };
    });
  }

  // Réduction de fréquence simple (moyenne de k échantillons) : suffit pour la
  // hauteur de la voix, qui reste bien en dessous de 8 kHz.
  function reduire(d, frequence) {
    var k = Math.max(1, Math.floor(frequence / PARAM.frequenceTravail));
    if (k === 1) return { d: d, f: frequence };
    var n = Math.floor(d.length / k), r = new Float32Array(n);
    for (var i = 0; i < n; i++) {
      var s = 0;
      for (var j = 0; j < k; j++) s += d[i * k + j];
      r[i] = s / k;
    }
    return { d: r, f: frequence / k };
  }

  // ---------------------------------------------------------------------------
  // 3. Hauteur : YIN (de Cheveigné et Kawahara, 2002)
  // ---------------------------------------------------------------------------
  // Pour chaque tranche de 30 ms, on cherche la période qui se répète le mieux.
  // Résultat : tableau de { t (s), hz (ou null si pas de voix), energie }.
  function hauteurs(echantillons, frequence) {
    var r = reduire(echantillons, frequence), d = r.d, f = r.f;
    var W = Math.round(PARAM.fenetre * f);
    var tauMin = Math.floor(f / PARAM.hzMax), tauMax = Math.ceil(f / PARAM.hzMin);
    var pas = Math.round(PARAM.pas * f);
    var res = [], diff = new Float32Array(tauMax + 1), cmnd = new Float32Array(tauMax + 1);

    for (var debut = 0; debut + W + tauMax < d.length; debut += pas) {
      // énergie de la tranche
      var e = 0;
      for (var i = 0; i < W; i++) e += d[debut + i] * d[debut + i];
      e = Math.sqrt(e / W);

      // fonction de différence
      for (var tau = 1; tau <= tauMax; tau++) {
        var s = 0;
        for (var j = 0; j < W; j++) {
          var x = d[debut + j] - d[debut + j + tau];
          s += x * x;
        }
        diff[tau] = s;
      }
      // différence normalisée cumulée
      cmnd[0] = 1;
      var cumul = 0;
      for (tau = 1; tau <= tauMax; tau++) {
        cumul += diff[tau];
        cmnd[tau] = cumul > 0 ? diff[tau] * tau / cumul : 1;
      }
      // premier creux sous le seuil, sinon le minimum absolu
      var choisi = -1;
      for (tau = tauMin; tau <= tauMax; tau++) {
        if (cmnd[tau] < PARAM.seuilYin) {
          while (tau + 1 <= tauMax && cmnd[tau + 1] < cmnd[tau]) tau++;
          choisi = tau;
          break;
        }
      }
      if (choisi < 0) {
        var min = Infinity;
        for (tau = tauMin; tau <= tauMax; tau++) if (cmnd[tau] < min) { min = cmnd[tau]; choisi = tau; }
      }
      var hz = null;
      if (cmnd[choisi] <= PARAM.aperiodiciteMax) {
        // interpolation parabolique pour une période plus précise
        var t0 = choisi;
        if (choisi > 1 && choisi < tauMax) {
          var a = cmnd[choisi - 1], b = cmnd[choisi], c = cmnd[choisi + 1];
          var den = a - 2 * b + c;
          if (den !== 0) t0 = choisi + (a - c) / (2 * den);
        }
        hz = f / t0;
      }
      res.push({ t: (debut + W / 2) / f, hz: hz, energie: e });
    }

    // silence : énergie trop faible par rapport au maximum
    var emax = 0;
    res.forEach(function (p) { if (p.energie > emax) emax = p.energie; });
    res.forEach(function (p) { if (p.energie < emax * PARAM.silenceRelatif) p.hz = null; });
    return res;
  }

  // ---------------------------------------------------------------------------
  // 4. Courbe : nettoyage et normalisation
  // ---------------------------------------------------------------------------
  function mediane(v) {
    var s = v.slice().sort(function (a, b) { return a - b; });
    return s.length ? s[Math.floor(s.length / 2)] : null;
  }

  // courbe(points) -> { points: [{ x (0 à 1), st (demi-tons ou null) }], medianeHz,
  //                     duree (s, partie voisée), partVoisee (0 à 1) }
  function courbe(points) {
    // 4.1 sauts d'octave : une mesure au double ou à la moitié de ses voisines est corrigée
    var hz = points.map(function (p) { return p.hz; });
    for (var i = 1; i < hz.length - 1; i++) {
      if (hz[i] == null || hz[i - 1] == null || hz[i + 1] == null) continue;
      var voisin = (hz[i - 1] + hz[i + 1]) / 2, rapport = hz[i] / voisin;
      if (rapport > 1.8 && rapport < 2.2) hz[i] /= 2;
      else if (rapport > 0.45 && rapport < 0.55) hz[i] *= 2;
    }
    // 4.2 fragments trop courts : un morceau de voix de moins de 40 ms entre deux trous
    // (ou en bord de mot) est presque toujours une fausse mesure (voix grinçante mesurée
    // à la moitié de sa hauteur, souffle final) ; il est écarté. Essai sur les audios de
    // Ban Mai : « 116 116 » après le sắc de lá, « 140 144 149 » dans la cassure du ngã de mũ.
    // Un saut de plus de PARAM.sautMax demi-tons en 10 ms coupe aussi le morceau :
    // aucune voix ne fait ça, c'est une erreur de mesure collée à la vraie voix.
    var segments = [], debut = -1;
    for (i = 0; i <= hz.length; i++) {
      var voise = i < hz.length && hz[i] != null;
      var saut = voise && debut >= 0 && Math.abs(12 * Math.log(hz[i] / hz[i - 1]) / Math.LN2) > PARAM.sautMax;
      if (debut >= 0 && (!voise || saut)) { segments.push([debut, i - 1]); debut = -1; }
      if (voise && debut < 0) debut = i;
    }
    var plusLong = Math.max.apply(null, segments.map(function (s) { return s[1] - s[0] + 1; }).concat([0]));
    segments.forEach(function (s) {
      var n = s[1] - s[0] + 1;
      if (n < PARAM.fragmentMin && n < plusLong) for (var k = s[0]; k <= s[1]; k++) hz[k] = null;
    });
    // 4.3 lissage : médiane sur 5 mesures voisines voisées
    var lisse = hz.map(function (v, k) {
      if (v == null) return null;
      var f = [];
      for (var m = k - 2; m <= k + 2; m++) if (m >= 0 && m < hz.length && hz[m] != null) f.push(hz[m]);
      return mediane(f);
    });
    // 4.4 partie voisée : de la première à la dernière mesure de voix
    var premier = lisse.findIndex(function (v) { return v != null; });
    var dernier = lisse.length - 1;
    while (dernier >= 0 && lisse[dernier] == null) dernier--;
    if (premier < 0) return { points: [], medianeHz: null, duree: 0, partVoisee: 0 };
    var voix = lisse.slice(premier, dernier + 1);
    var med = mediane(voix.filter(function (v) { return v != null; }));
    var n = voix.length;
    return {
      points: voix.map(function (v, k) {
        return { x: n > 1 ? k / (n - 1) : 0, st: v == null ? null : 12 * Math.log(v / med) / Math.LN2 };
      }),
      medianeHz: med,
      duree: n * PARAM.pas,
      partVoisee: voix.filter(function (v) { return v != null; }).length / n
    };
  }

  // analyser(blob) -> promesse { courbe, brut, duree } : décodage + hauteur + courbe
  function analyser(blob) {
    return decoder(blob).then(function (a) {
      var brut = hauteurs(a.echantillons, a.frequence);
      return { courbe: courbe(brut), brut: brut, duree: a.duree };
    });
  }

  // ---------------------------------------------------------------------------
  // 5. Dessin
  // ---------------------------------------------------------------------------
  // dessiner(canvas, [{ courbe, couleur, nom }], options)
  // Axe vertical : demi-tons de -12 à +12 autour de la hauteur médiane de chacun.
  // Axe horizontal : début à fin de la partie voisée du mot.
  // Un trou dans la courbe = pas de voix mesurable (coup de glotte, voix grinçante,
  // consonne sourde) : fréquent et normal pour les tons nặng et ngã.
  function dessiner(canvas, series, options) {
    options = options || {};
    var c = canvas.getContext('2d');
    var ratio = global.devicePixelRatio || 1;
    var L = canvas.clientWidth, H = canvas.clientHeight;
    canvas.width = L * ratio; canvas.height = H * ratio;
    c.setTransform(ratio, 0, 0, ratio, 0, 0);
    var st = options.ecart || 12, mg = 34, mh = 12, mb = 22;
    var X = function (x) { return mg + x * (L - mg - 10); };
    var Y = function (v) { return mh + (st - v) / (2 * st) * (H - mh - mb); };
    var styles = getComputedStyle(canvas);
    var trait = styles.getPropertyValue('--grille').trim() || '#ccc';
    var texte = styles.getPropertyValue('--texte-doux').trim() || '#666';

    c.clearRect(0, 0, L, H);
    c.font = '11px system-ui, sans-serif';
    c.fillStyle = texte;
    c.strokeStyle = trait;
    c.lineWidth = 1;
    for (var v = -st; v <= st; v += 4) {
      c.beginPath(); c.moveTo(mg, Y(v)); c.lineTo(L - 10, Y(v));
      c.setLineDash(v === 0 ? [] : [3, 4]); c.stroke();
      c.fillText((v > 0 ? '+' : '') + v, 6, Y(v) + 4);
    }
    c.setLineDash([]);
    c.fillText('début', mg, H - 6);
    c.fillText('fin', L - 30, H - 6);

    series.forEach(function (s) {
      if (!s.courbe || !s.courbe.points.length) return;
      c.strokeStyle = s.couleur;
      c.lineWidth = s.epaisseur || 3;
      c.lineJoin = 'round'; c.lineCap = 'round';
      c.beginPath();
      var leve = true;
      s.courbe.points.forEach(function (p) {
        if (p.st == null) { leve = true; return; }
        var y = Y(Math.max(-st, Math.min(st, p.st)));
        if (leve) { c.moveTo(X(p.x), y); leve = false; } else c.lineTo(X(p.x), y);
      });
      c.stroke();
    });
  }

  global.Prononciation = {
    PARAM: PARAM,
    diagnostic: diagnostic,
    Micro: Micro,
    decoder: decoder,
    hauteurs: hauteurs,
    courbe: courbe,
    analyser: analyser,
    dessiner: dessiner
  };
})(window);
