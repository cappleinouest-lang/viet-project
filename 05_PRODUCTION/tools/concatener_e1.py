# -*- coding: utf-8 -*-
"""
SÉQUENCES D'ÉCOUTE DE L'E1 (MOD-D25)
====================================

À QUOI IL SERT
    En E1, « Écouter » (débit normal) joue les audios d'un son à la suite. Ce script colle
    ces audios en UN fichier MP3 par voix, pour une écoute continue :
        voyelle seule (si elle existe) -> syllabes sans sens -> mots d'exemple.
    Pause entre deux morceaux = silence déjà présent à la fin (et au début) de chaque
    fichier d'origine : AUCUN silence ajouté.
    Une voix par fichier, jamais de mélange (choix de Christophe, MOD-D25) : côté femme,
    F1 (voyelle seule + syllabes) puis F4 (mots) = deux fichiers joués l'un après l'autre ;
    côté homme, H4 (H3 en leçon de tons) = un fichier.
    Débit lent, clic sur une tuile, E2–E5, page des tons : non concernés.

PRÉREQUIS
    Python de .venv-asr (numpy et soundfile, comme decoupe_audio.py) ; rien d'autre.

USAGE (depuis C:\\VIET_PROJECT), dans cet ordre :
    1. python 05_PRODUCTION\\tools\\generer_lecteur.py .            (ajouter --non-valides pour un essai)
    2. .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\concatener_e1.py . --lecon M0-L01
       (sans --lecon : toutes les leçons ; --refaire : refabrique même les fichiers déjà à jour)
    3. relancer generer_lecteur.py (mêmes options qu'en 1) : il ajoute les séquences au lecteur.
    Le script lit 06_LIVRABLES/lecteur/donnees.js (fichiers exacts de chaque tuile, voix
    choisies par VOIX_PAR_USAGE) : la séquence suit donc toujours ce que le lecteur jouerait.

SORTIES
    04_DONNEES/audio/e1_sequences/SEQ-<leçon>-<son>-<voix>.mp3
    04_DONNEES/audio/e1_sequences/sequences_e1.csv : une ligne par fichier, avec ses morceaux
        (segments), le début de chaque morceau (starts_ms) et la durée totale (duration_ms).
        generer_lecteur.py n'utilise une séquence que si ses morceaux sont EXACTEMENT ceux
        du lecteur du moment (sinon : lecture fichier par fichier, comme avant).
"""
import csv
import json
import os
import sys

DOSSIER_SEQ = 'audio/e1_sequences'          # relatif à 04_DONNEES
INDEX = 'sequences_e1.csv'
COLONNES = ['file', 'lesson_code', 'element', 'side', 'voice', 'segments', 'starts_ms', 'duration_ms']


# ---------------------------------------------------------------------------
# Fonctions partagées avec generer_lecteur.py (Python standard seulement)
# ---------------------------------------------------------------------------
def parties_sequence(d):
    """Plan des séquences d'un écran d'E1 (d = decouverte[son] de donnees.js).
    Renvoie {'F': [partie, ...], 'H': [...]} ; partie = {'voix', 'morceaux': [(i, fichier)]},
    i = rang de la tuile dans d['mots'] (-1 : la voyelle seule). Ordre : voyelle seule,
    syllabes sans sens, mots. Une partie par voix (jamais de mélange). Un côté est absent
    si un fichier manque (le lecteur joue alors fichier par fichier) ou si la voix manque
    (rappel court : femme seule)."""
    items = []
    if d.get('seul'):
        items.append((-1, d['seul']))
    items += [(i, m) for i, m in enumerate(d['mots']) if m.get('syllabe')]
    items += [(i, m) for i, m in enumerate(d['mots']) if not m.get('syllabe')]
    res = {}
    for cote in ('F', 'H'):
        parts, ok = [], bool(items)
        for i, m in items:
            v = m.get('voix') or []
            if cote == 'H' and len(v) < 2:
                ok = False
                break
            code = v[0] if cote == 'F' else v[-1]
            f = (m.get('audio', {}).get(code) or {}).get('normal')
            if not f:
                ok = False
                break
            if parts and parts[-1]['voix'] == code:
                parts[-1]['morceaux'].append((i, f))
            else:
                parts.append({'voix': code, 'morceaux': [(i, f)]})
        if ok:
            res[cote] = parts
    return res


def nom_fichier(lecon, element, voix):
    return DOSSIER_SEQ + '/SEQ-' + lecon + '-' + element + '-' + voix + '.mp3'


def lire_index(donnees):
    """sequences_e1.csv -> {fichier: ligne}. Fichier absent : dictionnaire vide."""
    chemin = os.path.join(donnees, DOSSIER_SEQ, INDEX)
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return {r['file']: r for r in csv.DictReader(f, delimiter=';')}


def sequence_lecteur(donnees, lecon, element, d, index):
    """Ce que reçoit le lecteur (d['sequence']) : {'F': [{fichier, voix, duree, morceaux:
    [{i, debut}]}], 'H': [...]}, seulement pour les côtés dont TOUTES les parties existent
    et sont à jour. None si aucun côté n'est prêt."""
    res = {}
    for cote, parts in parties_sequence(d).items():
        sortie = []
        for p in parts:
            f = nom_fichier(lecon, element, p['voix'])
            r = index.get(f)
            if (not r or r['segments'] != '|'.join(x[1] for x in p['morceaux'])
                    or not os.path.exists(os.path.join(donnees, f))):
                sortie = None
                break
            debuts = [int(x) for x in r['starts_ms'].split()]
            sortie.append({'fichier': f, 'voix': p['voix'], 'duree': int(r['duration_ms']),
                           'morceaux': [{'i': x[0], 'debut': t} for x, t in zip(p['morceaux'], debuts)]})
        if sortie:
            res[cote] = sortie
    return res or None


# ---------------------------------------------------------------------------
# Fabrication des fichiers
# ---------------------------------------------------------------------------
def coller(donnees, morceaux, destination):
    """Colle les MP3 tels quels (aucun silence ajouté). Renvoie (débuts en ms, durée en ms)."""
    import numpy as np
    import soundfile as sf
    blocs, debuts, sr0, n = [], [], None, 0
    for f in morceaux:
        x, sr = sf.read(os.path.join(donnees, f), dtype='float64', always_2d=True)
        if sr0 is None:
            sr0, canaux = sr, x.shape[1]
        if sr != sr0 or x.shape[1] != canaux:
            raise SystemExit(f'Format différent dans une même séquence : {f} ({sr} Hz, {x.shape[1]} canal/canaux)')
        debuts.append(round(n * 1000 / sr0))
        blocs.append(x)
        n += len(x)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    sf.write(destination, np.concatenate(blocs), sr0, format='MP3', subtype='MPEG_LAYER_III')
    return debuts, round(n * 1000 / sr0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    racine = args[0] if args else '.'
    lecon_seule = sys.argv[sys.argv.index('--lecon') + 1] if '--lecon' in sys.argv else None
    refaire = '--refaire' in sys.argv
    donnees = os.path.join(racine, '04_DONNEES')
    js = os.path.join(racine, '06_LIVRABLES', 'lecteur', 'donnees.js')
    if not os.path.exists(js):
        raise SystemExit('Lancer d\'abord generer_lecteur.py (fichier absent : ' + js + ')')
    with open(js, encoding='utf-8') as f:
        texte = f.read()
    D = json.loads(texte[texte.index('{'):texte.rindex('}') + 1])
    index = lire_index(donnees)
    faits = gardes = sans = 0
    for l in D['lecons']:
        if lecon_seule and l['code'] != lecon_seule:
            continue
        for e, d in l['decouverte'].items():
            plan = parties_sequence(d)
            if not plan:
                sans += 1
                print(f'  {l["code"]} {e} : pas de séquence (fichier manquant)')
            for cote, parts in plan.items():
                for p in parts:
                    f = nom_fichier(l['code'], e, p['voix'])
                    seg = '|'.join(x[1] for x in p['morceaux'])
                    r = index.get(f)
                    if not refaire and r and r['segments'] == seg and os.path.exists(os.path.join(donnees, f)):
                        gardes += 1
                        continue
                    debuts, duree = coller(donnees, [x[1] for x in p['morceaux']], os.path.join(donnees, f))
                    index[f] = {'file': f, 'lesson_code': l['code'], 'element': e, 'side': cote,
                                'voice': p['voix'], 'segments': seg,
                                'starts_ms': ' '.join(map(str, debuts)), 'duration_ms': str(duree)}
                    faits += 1
    chemin = os.path.join(donnees, DOSSIER_SEQ, INDEX)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';')
        w.writeheader()
        for k in sorted(index):
            w.writerow(index[k])
    print(f'{faits} séquence(s) fabriquée(s), {gardes} déjà à jour, {sans} son(s) sans séquence -> {chemin}')
    print('Relancer generer_lecteur.py pour les mettre dans le lecteur.')


if __name__ == '__main__':
    main()
