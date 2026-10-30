# -*- coding: utf-8 -*-
"""
Test : le mot étudié est-il mieux prononcé (début du mot, ton) quand il est précédé d'un
classificateur, ou d'un chiffre et d'un classificateur ? (discussion du 2026-10-30)

Pour 8 noms, trois versions, par les voix d'écoute des leçons de sons (F3 Thu Minh, H4 Huy Phong) :
    seul    « mèo »
    clf     « con mèo »          (classificateur)
    num     « hai con mèo »      (chiffre au ton ngang + classificateur)
Fichiers : 04_DONNEES/audio/_essais/appui/<mot>-<version>-<voix>.mp3 (hors audios.csv et lecteur).
Page d'écoute : 04_DONNEES/audio/_essais/appui/comparer.html (double-clic).

Mesure : durée de la consonne de début du DERNIER mot (le nom étudié) : du silence (ou du creux
d'énergie) qui le précède jusqu'au début de sa voix. Plus elle est courte, plus le début du mot
risque de paraître tronqué. Mesure approchée à l'intérieur d'une phrase : l'écoute décide.

Options (2026-10-30, « peu d'espace entre les mots ») :
    --lent   : les mêmes 48 audios au débit lent de chaque voix (colonne provider_speed_slow, 0,6),
               fichiers <mot>-<version>-<voix>-lent.mp3 ;
    --pause  : 3 façons de demander une pause à FPT, voix F3, 2 phrases (« hai con mèo », « hai cây bút ») :
               ssml   <speak>hai <break time="300ms"/> con <break time="300ms"/> mèo</speak>
               points « hai… con… mèo »
               tiret  « hai - con - mèo »
               (si FPT ne connaît pas le SSML, il risque de LIRE les balises : l'écoute le dira).
Le script mesure aussi l'ESPACE entre les mots : total des silences de plus de 30 ms entre le début
et la fin de la parole (ms).

Nécessite numpy et soundfile (.venv-asr), et FPT_MKP_API_KEY pour --executer. Usage :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\tester_appui.py .              -> plan
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\tester_appui.py . --executer   -> génère, mesure, page
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\tester_appui.py . --executer --lent --pause
"""
import csv
import os
import sys
import time

# mot, classificateur (ton) : ngang si possible ; cái et cuốn (sắc) pour comparer.
MOTS = [('mèo', 'con'), ('cá', 'con'), ('gà', 'con'), ('hoa', 'bông'), ('nhà', 'căn'),
        ('bút', 'cây'), ('bàn', 'cái'), ('sách', 'cuốn')]
CHIFFRE = 'hai'
VOIX = ['F3', 'H4']
VERSIONS = [('seul', 'seul'), ('clf', 'classificateur + nom'), ('num', 'chiffre + classificateur + nom')]


PAUSES = {
    'ssml': lambda m: '<speak>' + ' <break time="300ms"/> '.join(m) + '</speak>',
    'points': lambda m: '… '.join(m),
    'tiret': lambda m: ' - '.join(m),
}
PHRASES_PAUSE = [('mèo', 'con'), ('bút', 'cây')]


def texte(mot, clf, version):
    return {'seul': mot, 'clf': f'{clf} {mot}', 'num': f'{CHIFFRE} {clf} {mot}'}[version]


def nom_fichier(mot, version, voix, lent=False):
    import generer_audio_fpt as g
    return f"{g.telex(mot)}-{version}-{voix}{'-lent' if lent else ''}.mp3"


def consonne_dernier_mot(chemin):
    """ms entre la fin de la voix (ou le creux) qui précède le dernier mot et le début de sa voix."""
    import numpy as np
    import soundfile as sf
    import courbes_modele as cm
    x, sr = sf.read(chemin, dtype='float64', always_2d=True)
    x = x[:, 0]
    h = cm.hauteurs(x, sr)
    voix = [p['hz'] is not None for p in h]
    # début du dernier morceau voisé d'au moins 60 ms
    fin = len(voix) - 1
    while fin >= 0 and not voix[fin]:
        fin -= 1
    debut = fin
    while debut > 0 and voix[debut - 1]:
        debut -= 1
    if fin - debut < 5:
        return None
    t_voix = h[debut]['t']
    # avant : fin du morceau voisé précédent, sinon début de la parole
    avant = debut - 1
    while avant >= 0 and not voix[avant]:
        avant -= 1
    if avant >= 0:
        t0 = h[avant]['t']
    else:
        n = max(1, int(0.005 * sr))
        en = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)])
        db = 20 * np.log10(en / en.max() + 1e-9)
        t0 = int(np.argmax(db > -40)) * 0.005
    return max(0.0, t_voix - t0) * 1000


def espace(chemin):
    """Total (ms) des silences de plus de 30 ms à l'intérieur de la parole."""
    import numpy as np
    import soundfile as sf
    x, sr = sf.read(chemin, dtype='float64', always_2d=True)
    x = x[:, 0]
    n = max(1, int(0.005 * sr))
    en = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)])
    parole = 20 * np.log10(en / en.max() + 1e-9) > -35
    idx = np.where(parole)[0]
    if len(idx) == 0:
        return 0
    total, courant = 0, 0
    for p in parole[idx[0]:idx[-1] + 1]:
        if not p:
            courant += 1
        else:
            if courant * 5 > 30:
                total += courant * 5
            courant = 0
    return total


def page(dossier):
    lignes = []
    for mot, clf in MOTS:
        cases = []
        for v in VOIX:
            for code, _ in VERSIONS:
                f = nom_fichier(mot, code, v)
                fl = nom_fichier(mot, code, v, True)
                lent = (f' <button onclick="new Audio(\'{fl}\').play()">🐢</button>'
                        if os.path.exists(os.path.join(dossier, fl)) else '')
                cases.append(f'<td><button onclick="new Audio(\'{f}\').play()">▶ {texte(mot, clf, code)}</button>{lent}</td>')
        lignes.append(f'<tr><th>{mot}</th>{"".join(cases)}</tr>')
    tete = ''.join(f'<th>{v} · {nom}</th>' for v in VOIX for _, nom in VERSIONS)
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Test mots d'appui</title>
<style>body{{font:15px system-ui,sans-serif;margin:16px;background:#f7f5f0;color:#1f2328}}
table{{border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:6px;text-align:left}}
button{{font:inherit;padding:6px 10px;border-radius:6px;border:1px solid #bbb;background:#fff;cursor:pointer}}</style></head>
<body><h1>Mot seul, avec classificateur, avec chiffre</h1>
<p>Écoutez le <b>début du dernier mot</b> (consonne complète ?) et la <b>netteté de son ton</b>.</p>
<table><tr><th>Mot</th>{tete}</tr>{''.join(lignes)}</table>
<p>▶ débit normal · 🐢 débit lent (si généré avec --lent)</p>
{section_pauses(dossier)}</body></html>"""
    with open(os.path.join(dossier, 'comparer.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def section_pauses(dossier):
    lignes = []
    for mot, clf in PHRASES_PAUSE:
        cases = []
        for nom in PAUSES:
            f = f"pause-{nom}-{nom_fichier(mot, 'num', 'F3')}"
            if os.path.exists(os.path.join(dossier, f)):
                cases.append(f'<td><button onclick="new Audio(\'{f}\').play()">▶ {nom}</button></td>')
        if cases:
            base = nom_fichier(mot, 'num', 'F3')
            lignes.append(f'<tr><th>{texte(mot, clf, "num")}</th><td><button onclick="new Audio(\'{base}\').play()">▶ sans pause</button></td>{"".join(cases)}</tr>')
    if not lignes:
        return ''
    return ('<h2>Pauses demandées à FPT (Thu Minh)</h2><p>Les balises SSML sont-elles lues à voix haute ? '
            'La pause est-elle naturelle ?</p><table>' + ''.join(lignes) + '</table>')


def main():
    racine = next((a for a in sys.argv[1:] if not a.startswith('--')), '.')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import generer_audio_fpt as g
    donnees = os.path.join(racine, '04_DONNEES')
    dossier = os.path.join(donnees, 'audio', '_essais', 'appui')
    os.makedirs(os.path.join(dossier, '_bruts'), exist_ok=True)
    with open(os.path.join(donnees, 'voix.csv'), encoding='utf-8-sig', newline='') as f:
        voix_info = {v['voice_code']: v for v in csv.DictReader(f, delimiter=';')}
    # (texte envoyé, voix, vitesse, fichier)
    taches = []
    for m, c in MOTS:
        for ver, _ in VERSIONS:
            for v in VOIX:
                taches.append((texte(m, c, ver), v, 1.0, nom_fichier(m, ver, v)))
                if '--lent' in sys.argv:
                    vit = float(voix_info[v].get('provider_speed_slow') or 0.8)
                    taches.append((texte(m, c, ver), v, vit, nom_fichier(m, ver, v, True)))
    if '--pause' in sys.argv:
        for m, c in PHRASES_PAUSE:
            for nom, f in PAUSES.items():
                taches.append((f([CHIFFRE, c, m]), 'F3', 1.0, f"pause-{nom}-{nom_fichier(m, 'num', 'F3')}"))
    a_faire = [t for t in taches if not os.path.exists(os.path.join(dossier, t[3]))]
    print(f'{len(a_faire)} fichier(s) à générer ({sum(len(t[0]) for t in a_faire)} caractères).')
    if a_faire and '--executer' not in sys.argv:
        print('Plan seulement. Ajoutez --executer.')
        return
    if a_faire:
        import decoupe_audio
        cle = os.environ.get('FPT_MKP_API_KEY') or sys.exit('Clé FPT_MKP_API_KEY absente.')
        for i, (t, v, vit, nom) in enumerate(a_faire, 1):
            info = voix_info[v]
            print(f'[{i}/{len(a_faire)}] {t} · {v} · {vit} … ', end='', flush=True)
            try:
                contenu = g.synthetiser(t, cle, info['provider_voice'], vit, info.get('provider_model') or g.MODELE)
            except Exception as e:                       # une pause refusée ne doit pas tout arrêter
                print('ERREUR :', e)
                continue
            brut = os.path.join(dossier, '_bruts', nom)
            with open(brut, 'wb') as f:
                f.write(contenu)
            decoupe_audio.traiter_fichier(brut, os.path.join(dossier, nom), False)
            print('ok')
            time.sleep(g.DELAI_ENTRE_APPELS)
    page(dossier)
    print('\nConsonne de début du nom étudié (ms) :')
    print('Mot'.ljust(8) + ''.join(f'{v + " " + ver:>12}' for v in VOIX for ver, _ in VERSIONS))
    moy = {}
    for m, c in MOTS:
        ligne = m.ljust(8)
        for v in VOIX:
            for ver, _ in VERSIONS:
                d = consonne_dernier_mot(os.path.join(dossier, nom_fichier(m, ver, v)))
                moy.setdefault((v, ver), []).append(d or 0)
                ligne += f'{"?" if d is None else round(d):>12}'
        print(ligne)
    print('moyenne'.ljust(8) + ''.join(f'{sum(moy[(v, ver)]) / len(moy[(v, ver)]):>12.0f}' for v in VOIX for ver, _ in VERSIONS))
    # Espace entre les mots (version « chiffre + classificateur + nom »)
    print('\nEspace entre les mots, « hai + classificateur + nom » (ms de silence) :')
    for v in VOIX:
        for lent in (False, True):
            ch = [os.path.join(dossier, nom_fichier(m, 'num', v, lent)) for m, _ in MOTS]
            ch = [c for c in ch if os.path.exists(c)]
            if ch:
                print(f"   {v} {'lent  ' if lent else 'normal'} : {sum(espace(c) for c in ch) / len(ch):5.0f} ms en moyenne")
    for m, c in PHRASES_PAUSE:
        for nom in PAUSES:
            f = os.path.join(dossier, f"pause-{nom}-{nom_fichier(m, 'num', 'F3')}")
            if os.path.exists(f):
                print(f"   F3 pause {nom:6} « {texte(m, c, 'num')} » : {espace(f):5.0f} ms")
    print('\nPage d\'écoute :', os.path.join(dossier, 'comparer.html'))


if __name__ == '__main__':
    main()
