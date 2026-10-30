# -*- coding: utf-8 -*-
"""
Compare des voix de synthèse sur le CONTRASTE DES TONS (07_QUALITE/contraste_tons_voix_2026-10-30.md).

36 mots d'une syllabe (6 par ton, sans finale -p, -t, -c, -ch), au débit normal, pour chaque voix
demandée. Pour chaque voix, le script mesure à quel point les 6 tons se distinguent par la mélodie :
  - « reconnus » : part des mots dont le ton est retrouvé par le ton moyen le plus proche
    (le mot étant laissé de côté) ;
  - « contraste » : écart moyen entre tons / dispersion à l'intérieur d'un ton ;
  - quelques paires difficiles (sắc/ngã, hỏi/nặng, huyền/nặng, huyền/hỏi).
Il dit aussi, pour chaque ton, la hauteur moyenne (début → fin, en demi-tons) et la durée.

Les audios déjà présents dans 04_DONNEES/audio/ sont réutilisés. Les autres (voix inactives de
voix.csv, par exemple H1 Quang Anh, H5 Minh Quan) sont générés avec --executer dans
04_DONNEES/audio/_essais/tons/ : ils N'entrent PAS dans audios.csv ni dans le lecteur.

Nécessite numpy et soundfile, et la clé FPT_MKP_API_KEY pour --executer. Usage (depuis C:\\VIET_PROJECT) :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\tester_voix_tons.py . --voix F1 F3 H1 H3 H4 H5
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\tester_voix_tons.py . --voix F1 F3 H1 H3 H4 H5 --executer
Sans --executer : plan seulement (fichiers manquants listés, rien n'est appelé).

Option --doubler : pour les voix demandées, régénère les 36 mots en envoyant « mot, mot. » et en
gardant la 2e occurrence (même méthode que generer_audio_fpt.py --doubler), dans
04_DONNEES/audio/_essais/tons/<mot>-<voix>-double.mp3, et mesure ces fichiers-là. Sert à vérifier si
cette méthode corrige une voix qui tronque le début du mot (Thu Minh, Huy Phong : 2026-10-30).

Le tableau donne aussi, pour les mots qui commencent par une consonne, le silence avant le mot et
la durée de la consonne (ms) : une consonne très courte signale un début de mot tronqué.
"""
import argparse
import csv
import math
import os
import sys
import time

# Les 36 mots du test du 2026-10-30 (6 par ton), pour comparer toutes les voix sur la même base.
MOTS = {
    'ngang': ['W0318', 'W0015', 'W0046', 'W0009', 'W0336', 'W0220'],
    'sac':   ['W0243', 'W0163', 'W0066', 'W0029', 'W0141', 'W0145'],
    'huyen': ['W0004', 'W0228', 'W0146', 'W0095', 'W0037', 'W0110'],
    'hoi':   ['W0259', 'W0291', 'W0165', 'W0226', 'W0167', 'W0227'],
    'nga':   ['W0281', 'W0278', 'W0255', 'W0309', 'W0283', 'W0279'],
    'nang':  ['W0334', 'W0071', 'W0327', 'W0212', 'W0332', 'W0138'],
}
TONS = list(MOTS)
PAIRES = [('sac', 'nga'), ('hoi', 'nang'), ('huyen', 'nang'), ('huyen', 'hoi')]


def lire(chemin):
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


DOUBLER = False


def chemin_audio(donnees, mot, voix):
    """Fichier de la voix pour ce mot : audio du projet s'il existe, sinon fichier d'essai.
    Avec --doubler : toujours le fichier d'essai « double »."""
    if DOUBLER:
        return os.path.join(donnees, 'audio', '_essais', 'tons', f'{mot}-{voix}-double.mp3')
    normal = os.path.join(donnees, 'audio', f'{mot}-{voix}-normal.mp3')
    if os.path.exists(normal):
        return normal
    return os.path.join(donnees, 'audio', '_essais', 'tons', f'{mot}-{voix}-normal.mp3')


def generer(manquants, donnees, voix_info, mots):
    import generer_audio_fpt as g
    import decoupe_audio
    cle = os.environ.get('FPT_MKP_API_KEY')
    if not cle:
        sys.exit('Clé FPT_MKP_API_KEY absente : voir 05_PRODUCTION/03_audio.md, § 3.')
    bruts = os.path.join(donnees, 'audio', '_essais', 'tons', '_bruts')
    os.makedirs(bruts, exist_ok=True)
    for i, (mot, voix, dest) in enumerate(manquants, 1):
        v = voix_info[voix]
        print(f'[{i}/{len(manquants)}] {mots[mot]} · {voix} ({v["provider_voice"]}) … ', end='', flush=True)
        texte = f'{mots[mot]}, {mots[mot]}.' if DOUBLER else mots[mot]
        contenu = g.synthetiser(texte, cle, v['provider_voice'], 1.0, v.get('provider_model') or g.MODELE)
        brut = os.path.join(bruts, os.path.basename(dest))
        with open(brut, 'wb') as f:
            f.write(contenu)
        decoupe_audio.traiter_fichier(brut, dest, DOUBLER)    # même traitement que le projet
        print('ok')
        time.sleep(g.DELAI_ENTRE_APPELS)


# Mots du test qui commencent par une consonne audible (attaque à mesurer).
ATTAQUES = ['W0336', 'W0291', 'W0227', 'W0167', 'W0226', 'W0066', 'W0015', 'W0220', 'W0009', 'W0255', 'W0046']


def attaque(chemin):
    """(silence avant le mot, durée de la consonne de début) en ms."""
    import numpy as np
    import soundfile as sf
    import courbes_modele as cm
    x, sr = sf.read(chemin, dtype='float64', always_2d=True)
    x = x[:, 0]
    n = max(1, int(0.005 * sr))
    en = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)])
    db = 20 * np.log10(en / en.max() + 1e-9)
    t0 = int(np.argmax(db > -40)) * 0.005
    t1 = next((p['t'] for p in cm.hauteurs(x, sr) if p['hz']), t0)
    return t0 * 1000, max(0.0, t1 - 0.015 - t0) * 1000


def mesurer(courbes):
    """courbes : { ton: [courbe de courbes_modele.courbe(), ...] } pour UNE voix."""
    import numpy as np
    tous = [c for l in courbes.values() for c in l if c['medianeHz']]
    ref = float(np.median([c['medianeHz'] for c in tous]))
    X, lab = [], []
    for t in TONS:
        for c in courbes[t]:
            if not c['medianeHz'] or not c['points']:
                continue
            decal = 12 * math.log2(c['medianeHz'] / ref)
            p = np.array([np.nan if s is None else s + decal for _, s in c['points']])
            ok = ~np.isnan(p)
            q = np.interp(np.linspace(0, len(p) - 1, 5), np.arange(len(p))[ok], p[ok])
            X.append(list(q) + [c['duree'] * 10, (1 - c['partVoisee']) * 10])
            lab.append(t)
    X, lab = np.array(X), np.array(lab)
    centre = {t: X[lab == t].mean(0) for t in TONS}
    justes = 0
    for i in range(len(X)):
        cc = {t: X[(lab == t) & (np.arange(len(X)) != i)].mean(0) for t in TONS}
        justes += min(TONS, key=lambda t: np.linalg.norm(X[i] - cc[t])) == lab[i]
    dedans = float(np.mean([np.linalg.norm(X[i] - centre[lab[i]]) for i in range(len(X))]))
    entre = float(np.mean([np.linalg.norm(centre[a] - centre[b]) for i, a in enumerate(TONS) for b in TONS[i + 1:]]))
    return {'reconnus': justes / len(X), 'contraste': entre / dedans,
            'paires': {p: float(np.linalg.norm(centre[p[0]] - centre[p[1]])) / dedans for p in PAIRES},
            'centre': centre, 'n': len(X)}


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--voix', nargs='+', default=['F1', 'F3', 'H3', 'H4'])
    a.add_argument('--executer', action='store_true', help='générer les audios manquants (appel FPT)')
    a.add_argument('--doubler', action='store_true', help='« mot, mot. », 2e occurrence gardée (fichiers -double)')
    args = a.parse_args()
    global DOUBLER
    DOUBLER = args.doubler
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    donnees = os.path.join(args.racine, '04_DONNEES')
    voix_info = {v['voice_code']: v for v in lire(os.path.join(donnees, 'voix.csv'))}
    mots = {m['word_code']: m['written'] for m in lire(os.path.join(donnees, 'mots.csv'))}
    inconnues = [v for v in args.voix if v not in voix_info]
    if inconnues:
        sys.exit('Voix absente(s) de voix.csv : ' + ', '.join(inconnues))
    os.makedirs(os.path.join(donnees, 'audio', '_essais', 'tons'), exist_ok=True)
    manquants = [(m, v, chemin_audio(donnees, m, v)) for v in args.voix for t in TONS for m in MOTS[t]
                 if not os.path.exists(chemin_audio(donnees, m, v))]
    if manquants:
        print(f'{len(manquants)} audio(s) à générer ({sum(len(mots[m]) for m, _, _ in manquants)} caractères), '
              f'voix : {", ".join(sorted({v for _, v, _ in manquants}))}.')
        if not args.executer:
            print('Plan seulement. Ajoutez --executer pour les générer, puis relancez pour la mesure.')
            return
        generer(manquants, donnees, voix_info, mots)

    try:
        import numpy  # noqa: F401
        import soundfile  # noqa: F401
    except ImportError:
        sys.exit("numpy et soundfile sont nécessaires : lancer avec .venv-asr\\Scripts\\python.exe")
    import courbes_modele as cm
    resultats = {}
    for v in args.voix:
        print(f'Mesure de {v}…', flush=True)
        resultats[v] = mesurer({t: [cm.courbe_fichier(chemin_audio(donnees, m, v)) for m in MOTS[t]] for t in TONS})
        att = [attaque(chemin_audio(donnees, m, v)) for m in ATTAQUES]
        resultats[v]['silence'] = sum(a for a, _ in att) / len(att)
        resultats[v]['consonne'] = sum(b for _, b in att) / len(att)

    def nom(v):
        x = voix_info[v]
        return f"{v} {(x.get('note') or x['provider_voice']).split(' :')[0].split(' (')[0]}"[:26]
    print()
    print(('Fichiers « mot, mot. » (--doubler)\n' if DOUBLER else '') +
          'Voix'.ljust(27) + 'Reconnus  Contraste  ' + '  '.join(f'{p[0]}/{p[1]}' for p in PAIRES) + '  Silence  Consonne')
    for v in sorted(args.voix, key=lambda v: -resultats[v]['contraste']):
        r = resultats[v]
        print(nom(v).ljust(27) + f"{r['reconnus'] * 100:6.0f} %  {r['contraste']:8.2f}   "
              + '  '.join(f'{r["paires"][p]:{len(p[0]) + len(p[1]) + 1}.2f}' for p in PAIRES)
              + f"  {r['silence']:5.0f} ms {r['consonne']:5.0f} ms")
    print('\nHauteur moyenne de chaque ton (demi-tons, début → fin) et durée :')
    for v in args.voix:
        print(nom(v))
        for t in TONS:
            c = resultats[v]['centre'][t]
            print(f'   {t:6} ' + ' '.join(f'{x:+5.1f}' for x in c[:5]) + f'   {c[5] / 10:.2f} s')


if __name__ == '__main__':
    main()
