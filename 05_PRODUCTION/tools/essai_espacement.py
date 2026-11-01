# -*- coding: utf-8 -*-
"""
ESSAI D'ESPACEMENT DES MOTS DANS LES PHRASES (demande du 2026-10-31)
====================================================================

BUT
    Choisir comment écrire la phrase envoyée à FPT pour la version « mots espacés » (DEC-0058,
    aujourd'hui avec des points de suspension), et avec quelle voix du Nord.

CE QUI EST TESTÉ
    6 vraies phrases du projet (04_DONNEES/comptage.csv), chacune écrite de 4 façons :
        A normal       Tôi ăn nem.
        B virgules     Tôi, ăn, nem.
        C suspension   Tôi… ăn… nem.      (méthode actuelle, même calcul que generer_audio_fpt.py)
        D points       Tôi. Ăn. Nem.
    Un mot de deux syllabes (hôm nay, cà phê…) reste d'un seul tenant, comme dans le projet.
    Voix du Nord : Ban Mai (FPT.TTS-pro), Huy Phong et Le Minh (FPT.AI-VITs),
    Ban Mai, Viet Khoa et Quang Anh (FPT.TTS-ultra).

    Rien n'est écrit dans voix.csv, audios.csv ni le lecteur : tout va dans
    04_DONNEES/audio/_essais/espacement/ (fichier reçu de FPT gardé dans _bruts/).

USAGE (depuis C:\\VIET_PROJECT ; Python du projet : .venv-asr\\Scripts\\python.exe)
    1. Plan :                 ... essai_espacement.py .
    2. Génération + page :    ... essai_espacement.py . --executer
       -> page 04_DONNEES/audio/_essais/espacement/essai_espacement.html (double-clic).
          Une carte = une phrase dite par une voix, avec ses 4 façons. Pour chaque façon, noter :
          Espacement (trop faible / bon / trop long) et Naturel (oui / non), remarque facultative.
          Bouton « Exporter mes résultats » : fichier essai_espacement_<date>.csv dans Téléchargements.
    3. Bilan :                ... essai_espacement.py . --resultats            (dernier export)
                              ... essai_espacement.py . --resultats C:\\chemin\\essai_espacement_....csv
       -> tableau par façon et par voix, écrit dans 07_QUALITE/essai_espacement_<date>.md
          (copie de l'export dans 07_QUALITE/validations/).

MESURE AUTOMATIQUE (affichée sur chaque ligne de la page)
    Pauses entre les mots : silence d'au moins 50 ms sous -50 dBFS (comme decoupe_audio.py).
    « 3/3 » = toutes les pauses attendues trouvées ; « min » = pause la plus courte (ms).
"""
import argparse
import csv
import datetime
import glob
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generer_audio_fpt as g      # noqa: E402

VOIX = {   # code -> (nom, identifiant FPT, modèle)
    'F1': ('Ban Mai (pro)', 'std_banmai', 'FPT.TTS-pro'),
    'H4': ('Huy Phong (VITs)', 'std_huyphong', 'FPT.AI-VITs'),
    'H3': ('Le Minh (VITs)', 'std_leminh', 'FPT.AI-VITs'),
    'U1': ('Ban Mai (Ultra)', 'std_banmai', 'FPT.TTS-ultra'),
    'U2': ('Viet Khoa (Ultra)', 'std_vietkhoa', 'FPT.TTS-ultra'),
    'U4': ('Quang Anh (Ultra)', 'std_quanganh', 'FPT.TTS-ultra'),
}
PHRASES = ['P-L01-01', 'P-L01-04', 'P-L02-06', 'P-L04-01', 'P-L04-03', 'P-L04-06']   # 3 à 5 mots, une question
FACONS = {'A': 'normal', 'B': 'virgules', 'C': 'points de suspension (actuel)', 'D': 'points',
          'E': 'normal, vitesse 0,75'}
VITESSE = {'E': 0.75}            # façon -> vitesse demandée à FPT (1.0 par défaut)


def lire(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def textes(x, mots):
    """Les 4 façons d'écrire la phrase x (ligne de comptage.csv)."""
    ecrits = [mots[w]['written'] if w in mots else w for w in x['word_codes'].split()]
    fin = x['written'].rstrip()[-1:] if x['written'].rstrip()[-1:] in '.?!' else '.'
    maj = lambda s: s[:1].upper() + s[1:]
    return {'A': x['written'].strip(),
            'B': maj(', '.join(ecrits)) + fin,
            'C': g.phrase_espacee(x, mots),
            'D': '. '.join(maj(e) for e in ecrits) + fin,
            'E': x['written'].strip()}, len(ecrits)


def nom_fichier(ref, f, v):
    return f'{ref}-{f}-{v}.mp3'


def synthetiser(texte, cle, vid, modele, vitesse=1.0):
    if modele == 'FPT.TTS-ultra':      # même appel que essai_ultra.py, avec la vitesse demandée
        import json
        import urllib.request
        corps = {'model': modele, 'input': texte, 'text': texte, 'voice': vid,
                 'speed': vitesse, 'response_format': 'mp3'}
        req = urllib.request.Request(g.API_URL, data=json.dumps(corps, ensure_ascii=False).encode('utf-8'),
                                     method='POST', headers={'Authorization': 'Bearer ' + cle,
                                                             'Content-Type': 'application/json'})
        type_contenu, contenu = g.avec_patience(lambda: g.ouvrir(req, 60), 'la demande')
        if 'json' in type_contenu or contenu[:1] in (b'{', b'[') or len(contenu) < 500:
            raise RuntimeError('réponse inattendue : ' + contenu[:300].decode('utf-8', 'replace'))
        return contenu
    return g.synthetiser(texte, cle, vid, vitesse, modele)


def pauses(chemin, attendu):
    import soundfile as sf
    import decoupe_audio as d
    x, sr = sf.read(chemin, dtype='float64', always_2d=True)
    x = x.mean(axis=1)
    duree = len(x) / sr
    p = sorted(((b - a) * 1000 for a, b in d.silences(x, sr) if a > 0.02 and b < duree - 0.02), reverse=True)[:attendu]
    return {'trouvees': len(p), 'attendues': attendu, 'min': round(min(p)) if p else 0,
            'moy': round(sum(p) / len(p)) if p else 0, 'duree': round(duree, 1)}


def generer_et_page(racine, executer):
    donnees = os.path.join(racine, '04_DONNEES')
    dossier = os.path.join(donnees, 'audio', '_essais', 'espacement')
    os.makedirs(dossier, exist_ok=True)
    mots = {m['word_code']: m for m in lire(os.path.join(donnees, 'mots.csv'))}
    comptage = {x['item_code']: x for x in lire(os.path.join(donnees, 'comptage.csv'))}
    absentes = [p for p in PHRASES if p not in comptage]
    if absentes:
        sys.exit('Phrases absentes de comptage.csv : ' + ', '.join(absentes))
    phrases = {p: textes(comptage[p], mots) for p in PHRASES}
    taches = [(p, f, v) for p in PHRASES for v in VOIX for f in FACONS]
    manquants = [t for t in taches if not os.path.exists(os.path.join(dossier, nom_fichier(*t)))]
    print(f'{len(taches)} audios prévus ({len(PHRASES)} phrases × {len(FACONS)} façons × {len(VOIX)} voix) ; '
          f'à générer : {len(manquants)} (environ {sum(len(phrases[p][0][f]) for p, f, _ in manquants)} caractères).')
    for f in FACONS:
        print(f'   {f} {FACONS[f]:30} {phrases[PHRASES[0]][0][f]}')
    if manquants and not executer:
        print('Plan seulement. Ajoutez --executer pour générer et fabriquer la page.')
        return
    try:
        import numpy, soundfile   # noqa: F401
    except ImportError:
        sys.exit('numpy et soundfile sont nécessaires : lancer avec .venv-asr\\Scripts\\python.exe')
    if manquants:
        import decoupe_audio
        cle = os.environ.get('FPT_MKP_API_KEY')
        if not cle:
            sys.exit("La variable FPT_MKP_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")
        bruts = os.path.join(dossier, '_bruts')
        os.makedirs(bruts, exist_ok=True)
        for n, (p, f, v) in enumerate(manquants, 1):
            texte = phrases[p][0][f]
            nom, vid, modele = VOIX[v]
            print(f'[{n}/{len(manquants)}] {texte} · {nom} … ', end='', flush=True)
            try:
                brut = os.path.join(bruts, nom_fichier(p, f, v))
                with open(brut, 'wb') as fo:
                    fo.write(synthetiser(texte, cle, vid, modele, VITESSE.get(f, 1.0)))
                decoupe_audio.traiter_fichier(brut, os.path.join(dossier, nom_fichier(p, f, v)))
                print('ok')
            except Exception as e:
                print('erreur :', e)
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    sys.exit('Arrêt : problème de clé ou de solde.')
            time.sleep(g.DELAI_ENTRE_APPELS)

    cartes = []
    for p in PHRASES:
        t, nb = phrases[p]
        for v, (nom, _, modele) in VOIX.items():
            lignes = []
            for f in FACONS:
                ch = os.path.join(dossier, nom_fichier(p, f, v))
                if os.path.exists(ch):
                    lignes.append({'code': f'{p}|{f}|{v}', 'facon': f, 'facon_fr': FACONS[f], 'texte': t[f],
                                   'fichier': nom_fichier(p, f, v), 'version': str(int(os.path.getmtime(ch))),
                                   'mesure': pauses(ch, nb - 1)})
            if lignes:
                cartes.append({'phrase': p, 'ecrit': t['A'], 'sens': comptage[p].get('note', ''),
                               'voix': v, 'nom_voix': nom, 'lignes': lignes})
    d = {'genere_le': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'cartes': cartes,
         'voix': [[v, n] for v, (n, _, _) in VOIX.items()], 'phrases': PHRASES}
    chemin = os.path.join(dossier, 'essai_espacement.html')
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fo:
        fo.write(PAGE.replace('/*DONNEES*/null', json.dumps(d, ensure_ascii=False)))
    print(f'{sum(len(c["lignes"]) for c in cartes)} audios en {len(cartes)} cartes.')
    # La vitesse 0,75 est-elle prise en compte ? Durée totale des phrases E / A, par voix.
    print('\nVitesse 0,75 : durée des phrases à 0,75 comparée à 1,0 (même texte)')
    for v, (nom, _, modele) in VOIX.items():
        da = sum(l['mesure']['duree'] for c in cartes if c['voix'] == v for l in c['lignes'] if l['facon'] == 'A')
        de = sum(l['mesure']['duree'] for c in cartes if c['voix'] == v for l in c['lignes'] if l['facon'] == 'E')
        if da and de:
            r = de / da
            avis = 'ralenti, vitesse prise en compte' if r > 1.12 else 'pas ou presque pas ralenti : vitesse ignorée ?'
            print(f'   {nom:20} {modele:14} x{r:.2f}  {avis}')
    print('   (à 0,75, une durée environ x1,25 à x1,35 est attendue)')
    print('Page :', os.path.abspath(chemin))
    print('Elle lit les audios de son dossier : ne pas la déplacer.')


# ---------------------------------------------------------------------------
# Bilan d'un export
# ---------------------------------------------------------------------------
def resultats(racine, source):
    if not source:
        fichiers = glob.glob(os.path.join(os.path.expanduser('~'), 'Downloads', 'essai_espacement_*.csv'))
        if not fichiers:
            sys.exit("Aucun fichier essai_espacement_*.csv dans Téléchargements : indiquez son chemin après --resultats.")
        source = max(fichiers, key=os.path.getmtime)
    print('Fichier lu :', source)
    r = lire(source)
    if not r or 'espacement' not in r[0]:
        sys.exit("Ce fichier ne ressemble pas à un export de la page d'essai d'espacement.")
    qualite = os.path.join(racine, '07_QUALITE')
    copie = os.path.join(qualite, 'validations', os.path.basename(source))
    os.makedirs(os.path.dirname(copie), exist_ok=True)
    if os.path.abspath(source) != os.path.abspath(copie):
        shutil.copyfile(source, copie)

    def bilan(lignes):
        n = len(lignes)
        c = lambda k, val: sum(x[k] == val for x in lignes)
        return n, c('espacement', 'faible'), c('espacement', 'bon'), c('espacement', 'long'), c('naturel', 'non')

    def tableau(titre, cles, nom, libelle):
        out = [f'### {titre}', '', '| | Jugés | Espacement trop faible | Bon | Trop long | Pas naturel |',
               '|---|---|---|---|---|---|']
        for k in cles:
            n, fa, bo, lo, nn = bilan([x for x in r if nom(x) == k])
            if n:
                out.append(f'| {libelle(k)} | {n} | {fa} | **{bo}** | {lo} | {nn} |')
        return out + ['']

    noms_voix = {v: n for v, (n, _, _) in VOIX.items()}
    md = ['---', f'id: QUAL-ESPACEMENT-{datetime.date.today():%Y%m%d}', 'titre: Essai d\'espacement des mots dans les phrases',
          'statut: VALIDE', 'version: 1.0', f'date: {datetime.date.today()}',
          'resume: >', '  Bilan de l\'écoute de l\'essai essai_espacement.py : 6 phrases de comptage.csv,',
          '  4 façons d\'écrire la phrase envoyée à FPT, 6 voix du Nord.',
          'entrees: [REG-DEC, PROD-AUDIO]', 'sorties: []', 'sources:',
          f'  - 07_QUALITE/validations/{os.path.basename(source)} (écoute de Christophe)', '---', '',
          '# Essai d\'espacement des mots dans les phrases', '',
          'Façons : A normal ; B virgules ; C points de suspension (actuel, DEC-0058) ; D points.', '']
    md += tableau('Par façon', list(FACONS), lambda x: x['facon'], lambda k: f'{k} {FACONS[k]}')
    md += tableau('Par voix', list(VOIX), lambda x: x['voix'], lambda k: f'{k} {noms_voix[k]}')
    md += ['### Par voix et par façon (nombre de « bon »)', '',
           '| Voix | ' + ' | '.join(f'{f} {FACONS[f].split(" (")[0]}' for f in FACONS) + ' |',
           '|---|' + '---|' * len(FACONS)]
    for v in VOIX:
        cel = []
        for f in FACONS:
            n, _, bo, _, nn = bilan([x for x in r if x['voix'] == v and x['facon'] == f])
            cel.append(f'{bo}/{n}' + (f' ({nn} pas naturel)' if nn else '') if n else '—')
        md.append(f'| {v} {noms_voix[v]} | ' + ' | '.join(cel) + ' |')
    rem = [x for x in r if x.get('remarque')]
    if rem:
        md += ['', '### Remarques', ''] + [f'- {x["phrase"]} · {x["voix"]} · {x["facon"]} : {x["remarque"]}' for x in rem]
    md += ['', '## Historique', '', '| Version | Date | Changement |', '|---|---|---|',
           f'| 1.0 | {datetime.date.today()} | Création (bilan automatique de l\'export). |', '']
    sortie = os.path.join(qualite, f'essai_espacement_{datetime.date.today()}.md')
    with open(sortie, 'w', encoding='utf-8', newline='\n') as fo:
        fo.write('\n'.join(md))
    print('\n'.join(md[md.index('### Par façon'):]))
    print('Bilan écrit :', sortie, '; copie de l\'export :', copie)


PAGE = r'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Essai d'espacement des mots</title>
<style>
  :root { --fond:#f6f5f2; --carte:#fff; --texte:#222; --doux:#666; --bord:#ddd;
          --ok:#1e7d3a; --ok-fond:#e3f3e7; --ko:#b3261e; --ko-fond:#fbe5e3; --moy:#8a5a00; --moy-fond:#fdf0d5; --actif:#2f5fb3; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:system-ui,"Segoe UI",sans-serif; background:var(--fond); color:var(--texte); }
  header { position:sticky; top:0; z-index:5; background:#fff; border-bottom:1px solid var(--bord);
           padding:10px 16px; display:flex; flex-wrap:wrap; gap:10px 18px; align-items:center; }
  header h1 { font-size:18px; margin:0 8px 0 0; }
  .compte { font-size:14px; color:var(--doux); } .compte b { color:var(--texte); }
  select, button, input { font:inherit; font-size:14px; }
  button { cursor:pointer; border:1px solid var(--bord); background:#fff; border-radius:6px; padding:4px 9px; }
  button:hover { border-color:#999; }
  #exporter { background:var(--actif); color:#fff; border-color:var(--actif); font-weight:600; }
  #exporter.a-jour { background:#fff; color:var(--actif); }
  .aide { width:100%; font-size:13px; color:var(--doux); }
  kbd { border:1px solid #bbb; border-bottom-width:2px; border-radius:4px; padding:0 4px; font-size:12px; background:#fafafa; }
  main { max-width:980px; margin:0 auto; padding:14px 16px 80px; }
  .carte { background:var(--carte); border:2px solid var(--bord); border-radius:10px; padding:10px 14px; margin:10px 0; }
  .carte.active { border-color:var(--actif); box-shadow:0 0 0 3px #2f5fb322; }
  .carte.finie { opacity:.7; }
  .tete { display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 12px; }
  .ecrit { font-size:22px; font-weight:600; } .sens, .voix { color:var(--doux); }
  .voix { font-weight:600; color:var(--actif); }
  .actions { margin-left:auto; }
  table { width:100%; border-collapse:collapse; margin-top:6px; font-size:14px; }
  td { padding:5px 6px; border-top:1px solid #eee; vertical-align:middle; }
  td.n { width:22px; color:var(--doux); }
  td.texte { min-width:220px; } td.texte small { display:block; color:var(--doux); }
  td.mesure { font-size:12px; color:var(--doux); white-space:nowrap; }
  tr.joue td { background:#eef3fc; }
  .groupe { display:inline-flex; gap:3px; margin:2px 8px 2px 0; align-items:center; white-space:nowrap; }
  .groupe span { font-size:12px; color:var(--doux); margin-right:2px; }
  .choisi.bon { background:var(--ok-fond); border-color:var(--ok); color:var(--ok); }
  .choisi.mal { background:var(--ko-fond); border-color:var(--ko); color:var(--ko); }
  .choisi.moy { background:var(--moy-fond); border-color:var(--moy); color:var(--moy); }
  input.rem { width:100%; margin-top:3px; padding:2px 6px; border:1px solid var(--bord); border-radius:6px; font-size:13px; }
  .vide { color:var(--doux); padding:30px 0; text-align:center; }
</style>
</head>
<body>
<header>
  <h1>Essai d'espacement des mots</h1>
  <label>Phrase <select id="f-phrase"></select></label>
  <label>Voix <select id="f-voix"></select></label>
  <label><input type="checkbox" id="f-finies"> masquer les cartes terminées</label>
  <span class="compte" id="compte"></span>
  <button id="exporter">Exporter mes résultats</button>
  <div class="aide">
    Pour chaque façon d'écrire la phrase : <b>Espacement</b> (trop faible / bon / trop long) et <b>Naturel</b>
    (non = ton faux, mot déformé, mélodie cassée). Remarque facultative.
    <kbd>Espace</kbd> écouter les 5 façons · <kbd>1</kbd>…<kbd>5</kbd> écouter une façon ·
    <kbd>↓</kbd> <kbd>↑</kbd> carte suivante / précédente. Les résultats restent dans ce navigateur jusqu'à l'export.
  </div>
</header>
<main id="liste"></main>
<audio id="lecteur" preload="none"></audio>
<script>
"use strict";
const D = /*DONNEES*/null;
const CLE = 'viet-essai-espacement-v1';
const ESP = [['faible', 'trop faible', 'mal'], ['bon', 'bon', 'bon'], ['long', 'trop long', 'moy']];
const NAT = [['oui', 'oui', 'bon'], ['non', 'non', 'mal']];
let res = {};
try { res = JSON.parse(localStorage.getItem(CLE) || '{}'); } catch (e) { res = {}; }
let exporte = (() => { try { return localStorage.getItem(CLE + '-exporte') || ''; } catch (e) { return ''; } })();
function sauver() { try { localStorage.setItem(CLE, JSON.stringify(res)); } catch (e) {} }
function r(l) { const x = res[l.code]; return x && x.v === l.version ? x : {}; }
function complet(l) { const x = r(l); return x.e && x.n; }
function echapper(s) { return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

const fP = document.getElementById('f-phrase'), fV = document.getElementById('f-voix'), fF = document.getElementById('f-finies');
fP.innerHTML = '<option value="">toutes</option>' + D.phrases.map(p => {
  const c = D.cartes.find(c => c.phrase === p); return c ? `<option value="${p}">${echapper(c.ecrit)}</option>` : ''; }).join('');
fV.innerHTML = '<option value="">toutes</option>' + D.voix.map(([v, n]) => `<option value="${v}">${v} ${echapper(n)}</option>`).join('');
for (const el of [fP, fV, fF]) el.addEventListener('change', afficher);

let visibles = [], active = 0;
function finie(c) { return c.lignes.every(complet); }
function afficher() {
  visibles = D.cartes.filter(c => (!fP.value || c.phrase === fP.value) && (!fV.value || c.voix === fV.value) && !(fF.checked && finie(c)));
  active = Math.min(active, Math.max(visibles.length - 1, 0));
  document.getElementById('liste').innerHTML = visibles.map((c, k) => `<section class="carte ${finie(c) ? 'finie' : ''}" data-k="${k}">
    <div class="tete"><span class="ecrit">${echapper(c.ecrit)}</span><span class="sens">${echapper(c.sens)}</span>
      <span class="voix">${c.voix} ${echapper(c.nom_voix)}</span>
      <span class="actions"><button data-act="tout">▶ Écouter les 5</button></span></div>
    <table>${c.lignes.map((l, n) => ligne(l, n)).join('')}</table></section>`).join('')
    || '<p class="vide">Plus rien à juger avec ces filtres. Pensez à exporter.</p>';
  marquer(false); compter();
}
function boutons(l, champ, choix) {
  const x = r(l);
  return choix.map(([val, txt, cls]) => `<button data-act="${champ}" data-val="${val}" class="${x[champ] === val ? 'choisi ' + cls : ''}">${txt}</button>`).join('');
}
function ligne(l, n) {
  const m = l.mesure, x = r(l);
  return `<tr data-code="${echapper(l.code)}">
    <td class="n">${n + 1}</td>
    <td><button data-act="jouer">▶</button></td>
    <td class="texte"><b>${l.facon}</b> ${echapper(l.facon_fr)}<small>${echapper(l.texte)}</small>
      <input class="rem" placeholder="remarque (facultatif)" value="${echapper(x.r || '')}"></td>
    <td class="mesure">pauses ${m.trouvees}/${m.attendues}<br>min ${m.min} ms · moy ${m.moy} ms<br>${m.duree} s</td>
    <td><span class="groupe"><span>Espacement</span>${boutons(l, 'e', ESP)}</span><br>
        <span class="groupe"><span>Naturel</span>${boutons(l, 'n', NAT)}</span></td></tr>`;
}
function tous() { return D.cartes.flatMap(c => c.lignes); }
function compter() {
  const t = tous(), faits = t.filter(complet).length;
  const nouveaux = Object.values(res).filter(x => x.t > exporte).length;
  document.getElementById('compte').innerHTML = `<b>${faits}</b> jugés sur ${t.length}`;
  const b = document.getElementById('exporter');
  b.textContent = nouveaux ? `Exporter mes résultats (${nouveaux} nouveaux)` : 'Exporter mes résultats';
  b.classList.toggle('a-jour', !nouveaux);
}
function marquer(defiler) {
  document.querySelectorAll('.carte').forEach(el => el.classList.toggle('active', +el.dataset.k === active));
  const el = document.querySelector(`.carte[data-k="${active}"]`);
  if (el && defiler) el.scrollIntoView({block: 'center', behavior: 'smooth'});
}
function rafraichir(k) {
  const c = visibles[k], el = document.querySelector(`.carte[data-k="${k}"]`);
  if (!c || !el) return;
  el.querySelector('table').innerHTML = c.lignes.map((l, n) => ligne(l, n)).join('');
  el.classList.toggle('finie', finie(c)); compter();
}
function trouver(code) { return tous().find(l => l.code === code); }
function noter(l, champ, val) {
  const x = Object.assign({}, r(l));
  x[champ] = x[champ] === val ? '' : val;        // second clic : annule
  x.v = l.version; x.t = new Date().toISOString();
  res[l.code] = x; sauver();
}

const lecteur = document.getElementById('lecteur');
let jeton = 0;
function jouer(liste) {
  const mien = ++jeton, file = liste.slice();
  const suivant = () => {
    if (mien !== jeton) return;
    document.querySelectorAll('tr.joue').forEach(tr => tr.classList.remove('joue'));
    const l = file.shift(); if (!l) return;
    const tr = document.querySelector(`tr[data-code="${CSS.escape(l.code)}"]`);
    if (tr) tr.classList.add('joue');
    lecteur.src = l.fichier;
    lecteur.onended = () => setTimeout(suivant, 600);
    lecteur.onerror = () => setTimeout(suivant, 100);
    lecteur.play().catch(() => {});
  };
  lecteur.pause(); suivant();
}

const liste = document.getElementById('liste');
liste.addEventListener('click', ev => {
  const carte = ev.target.closest('.carte');
  if (carte) { active = +carte.dataset.k; marquer(false); }
  const b = ev.target.closest('button'); if (!b || !carte) return;
  const tr = b.closest('tr'), l = tr && trouver(tr.dataset.code);
  if (b.dataset.act === 'tout') jouer(visibles[active].lignes);
  else if (b.dataset.act === 'jouer') jouer([l]);
  else if (b.dataset.act === 'e' || b.dataset.act === 'n') { noter(l, b.dataset.act, b.dataset.val); rafraichir(active); }
});
liste.addEventListener('change', ev => {
  if (!ev.target.classList.contains('rem')) return;
  const l = trouver(ev.target.closest('tr').dataset.code);
  const x = Object.assign({}, r(l)); x.r = ev.target.value.trim(); x.v = l.version; x.t = new Date().toISOString();
  res[l.code] = x; sauver(); compter();
});
document.addEventListener('keydown', ev => {
  if (['SELECT', 'INPUT'].includes(ev.target.tagName) || ev.ctrlKey || ev.altKey || ev.metaKey) return;
  const c = visibles[active]; if (!c) return;
  if (ev.key === ' ') { ev.preventDefault(); jouer(c.lignes); }
  else if (/^[1-5]$/.test(ev.key)) { const l = c.lignes[+ev.key - 1]; if (l) jouer([l]); }
  else if (ev.key === 'ArrowDown') { ev.preventDefault(); active = Math.min(active + 1, visibles.length - 1); marquer(true); }
  else if (ev.key === 'ArrowUp') { ev.preventDefault(); active = Math.max(active - 1, 0); marquer(true); }
});

document.getElementById('exporter').addEventListener('click', () => {
  const lignes = ['phrase;voix;facon;texte;espacement;naturel;remarque;pauses_min_ms;pauses_moy_ms;date'];
  for (const c of D.cartes) for (const l of c.lignes) {
    const x = r(l);
    if (x.e || x.n || x.r) lignes.push([c.phrase, c.voix, l.facon, l.texte, x.e || '', x.n || '',
      (x.r || '').replace(/[;\n]/g, ','), l.mesure.min, l.mesure.moy, (x.t || '').slice(0, 10)].join(';'));
  }
  const m = new Date(), d = n => String(n).padStart(2, '0');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['\ufeff' + lignes.join('\n') + '\n'], {type: 'text/csv;charset=utf-8'}));
  a.download = `essai_espacement_${m.getFullYear()}-${d(m.getMonth() + 1)}-${d(m.getDate())}_${d(m.getHours())}${d(m.getMinutes())}.csv`;
  document.body.appendChild(a); a.click(); a.remove();
  exporte = m.toISOString();
  try { localStorage.setItem(CLE + '-exporte', exporte); } catch (e) {}
  compter();
});
document.title = "Essai d'espacement (" + D.genere_le + ')';
afficher();
</script>
</body>
</html>
'''


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true', help='générer les audios manquants (appel FPT)')
    a.add_argument('--resultats', nargs='?', const='', default=None, help='bilan du dernier export (ou du fichier indiqué)')
    args = a.parse_args()
    if args.resultats is not None:
        resultats(args.racine, args.resultats)
    else:
        generer_et_page(args.racine, args.executer)


if __name__ == '__main__':
    main()
