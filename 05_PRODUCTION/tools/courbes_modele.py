# -*- coding: utf-8 -*-
"""
Calcule À L'AVANCE la courbe mélodique de chaque audio de la voix modèle (F1), ainsi que de la
série des 6 tons (reference_tons.csv, toutes voix, DEC-0052), et écrit
04_DONNEES/courbes_modele.csv, que generer_lecteur.py met dans le lecteur (volet E4).

Pourquoi à l'avance ? Ouvert par double-clic, le lecteur peut JOUER un mp3 mais n'a pas le
droit de le LIRE pour l'analyser. La courbe de l'élève, elle, est calculée en direct dans
le navigateur (05_PRODUCTION/lecteur/prononciation.js).

Le calcul est le MÊME que dans prononciation.js (passage à 16 kHz, YIN, nettoyage, demi-tons
autour de la médiane, temps de 0 à 1), pour que les deux courbes soient comparables.
Toute modification d'un côté doit être faite de l'autre (mêmes noms de fonctions et de
paramètres). Décisions : DEC-0049, DEC-0050.

Nécessite numpy et soundfile (présents dans .venv-asr). Usage (depuis C:\\VIET_PROJECT) :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\courbes_modele.py .
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\courbes_modele.py . --voix F4,F1 --tout
Voix par défaut (DEC-0067) : la voix modèle de generer_audio_fpt.py (F4) et la voix qui fournit son
débit lent (colonne slow_from de voix.csv : F1).
Par défaut seuls les audios dont la courbe manque ou dont le fichier a changé sont calculés.

Colonnes de courbes_modele.csv :
    audio_code  : code de audios.csv (A-W0029-F1-normal)
    file        : fichier audio (audio/W0029-F1-normal.mp3)
    size        : taille du fichier en octets (sert à repérer un fichier regénéré)
    median_hz   : hauteur médiane de la voix dans ce mot (Hz)
    voiced_s    : durée de la partie voisée (s)
    points      : hauteurs en demi-tons autour de la médiane, une toutes les 10 ms, de la
                  première à la dernière mesure de voix, séparées par des espaces ;
                  « _ » = pas de voix mesurable à cet instant
"""
import csv
import math
import os
import sys

PARAM = {
    'hzMin': 70,
    'hzMax': 500,
    'pas': 0.010,
    'fenetre': 0.030,
    'seuilYin': 0.15,
    'aperiodiciteMax': 0.35,
    'silenceRelatif': 0.08,
    'fragmentMin': 4,
    'sautMax': 7,
    'frequenceTravail': 16000,
}
COLONNES = ['audio_code', 'file', 'size', 'median_hz', 'voiced_s', 'points']


def arrondi(x):
    """Math.round de JavaScript (0,5 arrondi vers le haut), différent de round() de Python."""
    return int(math.floor(x + 0.5))


def reduire(d, frequence):
    """Passage à exactement 16 kHz : moyenne glissante sur k échantillons, puis interpolation."""
    import numpy as np
    fc = PARAM['frequenceTravail']
    if frequence == fc:
        return d, fc
    k = max(1, arrondi(frequence / fc))
    m = d
    if k > 1:
        c = np.cumsum(d)
        m = c.copy()
        m[k:] = c[k:] - c[:-k]
        m = m / np.minimum(np.arange(1, len(d) + 1), k)
    n = int(math.floor((len(d) - 1) * fc / frequence)) + 1
    x = np.arange(n) * frequence / fc
    i0 = np.floor(x).astype(int)
    a = x - i0
    i1 = np.minimum(i0 + 1, len(m) - 1)
    return m[i0] * (1 - a) + m[i1] * a, fc


def hauteurs(echantillons, frequence):
    """YIN : liste de dict { t, hz (ou None), energie }, une mesure toutes les 10 ms."""
    import numpy as np
    from numpy.lib.stride_tricks import sliding_window_view
    d, f = reduire(np.asarray(echantillons, dtype=np.float64), frequence)
    W = arrondi(PARAM['fenetre'] * f)
    tau_min = int(math.floor(f / PARAM['hzMax']))
    tau_max = int(math.ceil(f / PARAM['hzMin']))
    pas = arrondi(PARAM['pas'] * f)
    res = []
    debut = 0
    while debut + W + tau_max < len(d):
        x = d[debut:debut + W]
        e = math.sqrt(float(np.dot(x, x)) / W)
        fen = sliding_window_view(d[debut + 1:debut + tau_max + W], W)      # tau = 1 .. tau_max
        diff = np.empty(tau_max + 1)
        diff[0] = 0
        diff[1:] = ((fen - x) ** 2).sum(axis=1)
        cumul = np.cumsum(diff[1:])
        cmnd = np.ones(tau_max + 1)
        tau = np.arange(1, tau_max + 1)
        cmnd[1:] = np.where(cumul > 0, diff[1:] * tau / np.where(cumul > 0, cumul, 1), 1)

        choisi = -1
        t = tau_min
        while t <= tau_max:
            if cmnd[t] < PARAM['seuilYin']:
                while t + 1 <= tau_max and cmnd[t + 1] < cmnd[t]:
                    t += 1
                choisi = t
                break
            t += 1
        if choisi < 0:
            choisi = tau_min + int(np.argmin(cmnd[tau_min:tau_max + 1]))
        hz = None
        if cmnd[choisi] <= PARAM['aperiodiciteMax']:
            t0 = float(choisi)
            if 1 < choisi < tau_max:
                a, b, c = cmnd[choisi - 1], cmnd[choisi], cmnd[choisi + 1]
                den = a - 2 * b + c
                if den != 0:
                    t0 = choisi + (a - c) / (2 * den)
            hz = f / t0
        res.append({'t': (debut + W / 2) / f, 'hz': hz, 'energie': e})
        debut += pas

    emax = max([p['energie'] for p in res] + [0])
    for p in res:
        if p['energie'] < emax * PARAM['silenceRelatif']:
            p['hz'] = None
    return res


def mediane(v):
    s = sorted(v)
    return s[len(s) // 2] if s else None


def courbe(points):
    """Même nettoyage que prononciation.js : { points: [(x, st ou None)], medianeHz, duree, partVoisee }."""
    hz = [p['hz'] for p in points]
    # 4.1 sauts d'octave
    for i in range(1, len(hz) - 1):
        if hz[i] is None or hz[i - 1] is None or hz[i + 1] is None:
            continue
        rapport = hz[i] / ((hz[i - 1] + hz[i + 1]) / 2)
        if 1.8 < rapport < 2.2:
            hz[i] /= 2
        elif 0.45 < rapport < 0.55:
            hz[i] *= 2
    # 4.2 fragments trop courts (coupure aussi sur un saut de plus de sautMax demi-tons)
    segments, debut = [], -1
    for i in range(len(hz) + 1):
        voise = i < len(hz) and hz[i] is not None
        saut = voise and debut >= 0 and abs(12 * math.log2(hz[i] / hz[i - 1])) > PARAM['sautMax']
        if debut >= 0 and (not voise or saut):
            segments.append((debut, i - 1))
            debut = -1
        if voise and debut < 0:
            debut = i
    plus_long = max([s[1] - s[0] + 1 for s in segments] + [0])
    for s in segments:
        n = s[1] - s[0] + 1
        if n < PARAM['fragmentMin'] and n < plus_long:
            for k in range(s[0], s[1] + 1):
                hz[k] = None
    # 4.3 lissage : médiane sur 5 mesures voisines voisées
    lisse = []
    for k, v in enumerate(hz):
        if v is None:
            lisse.append(None)
            continue
        lisse.append(mediane([hz[m] for m in range(k - 2, k + 3) if 0 <= m < len(hz) and hz[m] is not None]))
    # 4.4 partie voisée
    idx = [i for i, v in enumerate(lisse) if v is not None]
    if not idx:
        return {'points': [], 'medianeHz': None, 'duree': 0, 'partVoisee': 0}
    voix = lisse[idx[0]:idx[-1] + 1]
    med = mediane([v for v in voix if v is not None])
    n = len(voix)
    return {
        'points': [(k / (n - 1) if n > 1 else 0, None if v is None else 12 * math.log2(v / med))
                   for k, v in enumerate(voix)],
        'medianeHz': med,
        'duree': n * PARAM['pas'],
        'partVoisee': sum(1 for v in voix if v is not None) / n,
    }


def courbe_fichier(chemin):
    import numpy as np
    import soundfile as sf
    x, sr = sf.read(chemin, dtype='float64', always_2d=True)
    return courbe(hauteurs(x[:, 0], sr))


def lire(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def main():
    args = sys.argv[1:]
    choix = args[args.index('--voix') + 1] if '--voix' in args and args.index('--voix') + 1 < len(args) else None
    racine = next((a for a in args if not a.startswith('--') and a != choix), '.')
    tout = '--tout' in sys.argv
    donnees = os.path.join(racine, '04_DONNEES')
    if choix:
        voix = set(choix.split(','))
    else:                    # voix modèle + voix de son débit lent (DEC-0067)
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from generer_audio_fpt import VOIX_MODELE
        lignes_voix = {v['voice_code']: v for v in lire(os.path.join(donnees, 'voix.csv'))}
        voix = {VOIX_MODELE} | ({lignes_voix[VOIX_MODELE]['slow_from']}
                               if lignes_voix.get(VOIX_MODELE, {}).get('slow_from') else set())
    try:
        import numpy  # noqa: F401
        import soundfile  # noqa: F401
    except ImportError:
        sys.exit("numpy et soundfile sont nécessaires : lancer avec .venv-asr\\Scripts\\python.exe")

    sortie = os.path.join(donnees, 'courbes_modele.csv')
    anciennes = {l['audio_code']: l for l in lire(sortie)}
    # Voix modèle, plus toutes les voix pour la série de la page « Les 6 tons » (DEC-0052).
    refs_tons = {x['word_code'] or x['written'] for x in lire(os.path.join(donnees, 'reference_tons.csv'))}
    audios = [a for a in lire(os.path.join(donnees, 'audios.csv')) if a['voice'] in voix or a['item_ref'] in refs_tons]
    lignes, calcules, absents = [], 0, 0
    for i, a in enumerate(audios):
        chemin = os.path.join(donnees, a['file'].replace('/', os.sep))
        if not os.path.exists(chemin):
            absents += 1
            continue
        taille = str(os.path.getsize(chemin))
        ancienne = anciennes.get(a['audio_code'])
        if ancienne and ancienne['size'] == taille and ancienne['file'] == a['file'] and not tout:
            lignes.append(ancienne)
            continue
        c = courbe_fichier(chemin)
        lignes.append({
            'audio_code': a['audio_code'], 'file': a['file'], 'size': taille,
            'median_hz': '' if c['medianeHz'] is None else str(round(c['medianeHz'])),
            'voiced_s': '%.2f' % c['duree'],
            'points': ' '.join('_' if st is None else '%.1f' % st for _, st in c['points']),
        })
        calcules += 1
        if calcules % 50 == 0:
            print(f'  {calcules} courbes calculées…')
    with open(sortie, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';', lineterminator='\n')
        w.writeheader()
        w.writerows(lignes)
    print(f'Voix {", ".join(sorted(voix))} et série des tons : {len(lignes)} courbes ({calcules} calculées, {len(lignes) - calcules} reprises), '
          f'{absents} fichier(s) audio absent(s).')
    print('Écrit :', sortie)


if __name__ == '__main__':
    main()
