# -*- coding: utf-8 -*-
"""
Découpage des audios « doublés » (DEC à venir, essais du 2026-10-29).

Problème constaté : prononcé seul, un mot court perd sa consonne de départ avec les
voix d'homme de FPT.TTS-pro. Solution retenue à l'écoute : envoyer « mot, mot. » et
ne garder que la 2e occurrence.

Méthode : on repère les silences (niveau sous SEUIL_DBFS pendant au moins SILENCE_MIN),
on prend le plus long silence situé entre deux passages parlés (la pause de la virgule),
et on garde ce qui suit, avec une petite marge avant et après.
Égalisation du volume (demande du 2026-10-29 : voix de niveaux différents) : chaque fichier
est ramené à NIVEAU_CIBLE (niveau moyen des passages parlés), sans que la crête dépasse CRETE_MAX.
Nécessite numpy et soundfile (présents dans .venv-asr).
"""
import numpy as np

SEUIL_DBFS = -50.0      # en dessous : silence (comme ffmpeg silencedetect n=-50dB)
SILENCE_MIN = 0.05      # s
TRAME = 0.01            # s
MARGE_AVANT = 0.06      # s gardées avant la reprise de la parole (protège la consonne de départ)
MARGE_APRES = 0.06      # s
SILENCE_DEBUT = 0.10    # s de silence ajoutées avant le mot
SILENCE_FIN = 0.35      # s de silence ajoutées après le mot
FONDU_DEBUT = 0.01
FONDU_FIN = 0.03
NIVEAU_CIBLE = -20.0    # dBFS, niveau moyen des passages parlés
CRETE_MAX = -1.0        # dBFS, crête à ne jamais dépasser (pas de saturation)


def silences(x, sr):
    """Liste des (début, fin) en secondes des passages silencieux."""
    n = max(1, int(TRAME * sr))
    nb = len(x) // n
    if nb == 0:
        return []
    trames = x[:nb * n].reshape(nb, n)
    db = 20 * np.log10(np.sqrt((trames ** 2).mean(axis=1)) + 1e-10)
    calme = db < SEUIL_DBFS
    res, debut = [], None
    for i, c in enumerate(list(calme) + [False]):
        if c and debut is None:
            debut = i
        elif not c and debut is not None:
            if (i - debut) * TRAME >= SILENCE_MIN:
                res.append((debut * TRAME, i * TRAME))
            debut = None
    return res


def garder_dernier_mot(x, sr):
    """x : signal mono (float, -1..1). Renvoie le signal du 2e mot, prêt à enregistrer."""
    duree = len(x) / sr
    sil = silences(x, sr)
    # silences intérieurs : ni au tout début, ni à la toute fin
    interieurs = [s for s in sil if s[0] > 0.02 and s[1] < duree - 0.02]
    if not interieurs:
        raise RuntimeError('pause entre les deux mots introuvable')
    pause = max(interieurs, key=lambda s: s[1] - s[0])
    debut = max(0.0, pause[1] - MARGE_AVANT)
    fin_parole = duree
    for s in sil:                      # silence final éventuel
        if s[0] > pause[1] and s[1] >= duree - 0.02:
            fin_parole = s[0]
    fin = min(duree, fin_parole + MARGE_APRES)
    mot = x[int(debut * sr):int(fin * sr)].copy()
    if len(mot) < int(0.1 * sr):
        raise RuntimeError(f'mot découpé trop court ({len(mot) / sr:.2f} s)')
    a, b = int(FONDU_DEBUT * sr), int(FONDU_FIN * sr)
    mot[:a] *= np.linspace(0, 1, a)
    mot[-b:] *= np.linspace(1, 0, b)
    return np.concatenate([np.zeros(int(SILENCE_DEBUT * sr)), mot, np.zeros(int(SILENCE_FIN * sr))])


def niveau_parole(x, sr):
    """Niveau moyen (dBFS) des trames non silencieuses."""
    n = max(1, int(TRAME * sr))
    trames = x[:len(x) // n * n].reshape(-1, n)
    rms = np.sqrt((trames ** 2).mean(axis=1))
    parole = trames[20 * np.log10(rms + 1e-10) >= SEUIL_DBFS]
    if len(parole) == 0:
        raise RuntimeError('aucune parole détectée')
    return 20 * np.log10(np.sqrt((parole ** 2).mean()) + 1e-10)


def normaliser(x, sr):
    gain = NIVEAU_CIBLE - niveau_parole(x, sr)
    crete = 20 * np.log10(np.abs(x).max() + 1e-10)
    gain = min(gain, CRETE_MAX - crete)
    return x * 10 ** (gain / 20)


def traiter_fichier(source, destination, doubler=False):
    """Lit le mp3 reçu de FPT ; garde le 2e mot si doubler ; égalise le volume ; écrit le mp3."""
    import soundfile as sf
    x, sr = sf.read(source, dtype='float64', always_2d=True)
    y = x.mean(axis=1)
    if doubler:
        y = garder_dernier_mot(y, sr)
    sf.write(destination, normaliser(y, sr), sr, format='MP3', subtype='MPEG_LAYER_III')
