# -*- coding: utf-8 -*-
"""
Page de test : les voix savent-elles dire une VOYELLE SEULE ? (demande du 2026-10-31)

Chaque voyelle (a, ă, â, e, ê, i, y, o, ô, ơ, u, ư) est envoyée seule à FPT, avec chaque voix du Nord :
F4 Ban Mai et H6 Quang Anh (FPT.TTS-ultra), F1 Ban Mai (FPT.TTS-pro), H4 Huy Phong et H3 Le Minh
(FPT.AI-VITs). À écouter : la voyelle est-elle dite, ou la voix lit-elle le NOM de la lettre
(ă -> « á », â -> « ớ », comme quand on épelle) ?

Rien n'est écrit dans voix.csv, audios.csv ni le lecteur : tout va dans
04_DONNEES/audio/_essais/voyelles/ (page ecoute.html, fichiers reçus de FPT dans _bruts/).

Usage (depuis C:\\VIET_PROJECT) :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\essai_voyelles.py .             -> plan seulement
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\essai_voyelles.py . --executer  -> génère et fait la page
"""
import argparse
import html
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generer_audio_fpt as g      # noqa: E402  (même appel à FPT)

VOYELLES = ['a', 'ă', 'â', 'e', 'ê', 'i', 'y', 'o', 'ô', 'ơ', 'u', 'ư']
VOIX = {   # code -> (nom, identifiant FPT, modèle)
    'F4': ('Ban Mai (Ultra)', 'std_banmai', 'FPT.TTS-ultra'),
    'H6': ('Quang Anh (Ultra)', 'std_quanganh', 'FPT.TTS-ultra'),
    'F1': ('Ban Mai (pro)', 'std_banmai', 'FPT.TTS-pro'),
    'H4': ('Huy Phong (VITs)', 'std_huyphong', 'FPT.AI-VITs'),
    'H3': ('Le Minh (VITs)', 'std_leminh', 'FPT.AI-VITs'),
}


def nom_fichier(v, code):
    return f'V-{g.telex(v)}-{code}.mp3'


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true')
    args = a.parse_args()
    dossier = os.path.join(args.racine, '04_DONNEES', 'audio', '_essais', 'voyelles')
    os.makedirs(dossier, exist_ok=True)
    manquants = [(v, c) for v in VOYELLES for c in VOIX if not os.path.exists(os.path.join(dossier, nom_fichier(v, c)))]
    print(f'{len(manquants)} audio(s) à générer ({len(VOYELLES)} voyelles × {len(VOIX)} voix), '
          f'environ {len(manquants)} caractères.')
    if manquants and not args.executer:
        print('Plan seulement. Ajoutez --executer pour générer.')
        return
    if manquants:
        try:
            import decoupe_audio
        except ImportError:
            sys.exit('numpy et soundfile sont nécessaires : lancer avec .venv-asr\\Scripts\\python.exe')
        cle = os.environ.get('FPT_MKP_API_KEY')
        if not cle:
            sys.exit("La variable FPT_MKP_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")
        bruts = os.path.join(dossier, '_bruts')
        os.makedirs(bruts, exist_ok=True)
        for n, (v, c) in enumerate(manquants, 1):
            nom, vid, modele = VOIX[c]
            print(f'[{n}/{len(manquants)}] {v} · {nom} … ', end='', flush=True)
            try:
                brut = os.path.join(bruts, nom_fichier(v, c))
                with open(brut, 'wb') as f:
                    f.write(g.synthetiser(v, cle, vid, 1.0, modele))
                # même traitement que le projet : volume égalisé ; Ultra : silence final complété (DEC-0068)
                decoupe_audio.traiter_fichier(brut, os.path.join(dossier, nom_fichier(v, c)),
                                              fin='ultra' in modele.lower())
                print('ok')
            except Exception as e:
                print('erreur :', e)
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    sys.exit('Arrêt : problème de clé ou de solde.')
            time.sleep(g.DELAI_ENTRE_APPELS)

    lignes = []
    for v in VOYELLES:
        cel = ''.join(f'<td><audio controls preload="none" src="{nom_fichier(v, c)}"></audio></td>'
                      if os.path.exists(os.path.join(dossier, nom_fichier(v, c))) else '<td>—</td>' for c in VOIX)
        lignes.append(f'<tr><th>{html.escape(v)}</th>{cel}</tr>')
    entete = ''.join(f'<th>{html.escape(n)}</th>' for n, _, _ in VOIX.values())
    page = ('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Essai voyelles seules</title>'
            '<style>body{font-family:system-ui,"Segoe UI",sans-serif;margin:16px}table{border-collapse:collapse}'
            'td,th{border:1px solid #ccc;padding:4px 8px;text-align:left}th:first-child{font-size:1.6em;text-align:center}'
            'audio{width:150px}</style>'
            '<h1>Voyelles seules : la voyelle, ou le nom de la lettre ?</h1>'
            '<p>Attention à <b>ă</b> et <b>â</b> : elles ne forment jamais une syllabe seules en vietnamien ; '
            'une voix peut lire le nom de la lettre (« á », « ớ ») au lieu du son.</p>'
            f'<table><tr><th>Voyelle</th>{entete}</tr>{"".join(lignes)}</table>')
    with open(os.path.join(dossier, 'ecoute.html'), 'w', encoding='utf-8') as f:
        f.write(page)
    print('Page :', os.path.abspath(os.path.join(dossier, 'ecoute.html')))


if __name__ == '__main__':
    main()
