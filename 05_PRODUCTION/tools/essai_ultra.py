# -*- coding: utf-8 -*-
"""
Essai de FPT.TTS-ultra avec toutes les voix du Nord proposées par la marketplace (demande du 2026-10-31) :
Ban Mai, Viet Khoa, Minh Quang, Quang Anh.

Ce script ne touche NI à voix.csv, NI à audios.csv, NI au lecteur : tout va dans
04_DONNEES/audio/_essais/ultra/ (fichier reçu de FPT gardé dans _bruts/).

Trois étapes, chacune lancée séparément (depuis C:\\VIET_PROJECT) :

 1. Sonde : trouve le bon identifiant de chaque voix (un appel par identifiant possible, mot « ba »).
        .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\essai_ultra.py . --sonde
    Le script affiche, pour chaque identifiant essayé : accepté ou refusé, et une « empreinte » du
    fichier. Deux voix différentes doivent avoir des empreintes différentes ; si toutes les
    empreintes sont identiques, le service ignore la voix et lit tout avec sa voix par défaut.

 2. Génération : les 36 mots du test des tons (tester_voix_tons.py) + quelques syllabes d'accent
    (r-, d-, gi-, s-, x-, tr-, ch-), au débit normal, pour chaque voix Ultra.
        .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\essai_ultra.py . --ids U1=std_banmai,U2=fci_vietkhoa,U3=...,U4=... --executer
    (sans --executer : plan seulement, rien n'est appelé)

 3. Mesure et page d'écoute (relancer la même commande sans --executer une fois les fichiers créés) :
    tableau comparatif (même mesure que tester_voix_tons.py) avec, pour référence, Ban Mai en
    FPT.TTS-pro (F1) et Huy Phong en FPT.AI-VITs (H4), et page 04_DONNEES/audio/_essais/ultra/ecoute.html
    pour écouter les voix côte à côte.

Test d'accent Nord / Sud (2026-10-31) : 15 mots et phrases choisis pour séparer les deux accents,
page 04_DONNEES/audio/_essais/ultra/accent/accent.html :
    .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\essai_ultra.py . --accent --ids U1=std_banmai,U5=fci_xuantoan,U6=fci_phuongan,U7=std_kimngan --executer

Clé : variable d'environnement FPT_MKP_API_KEY, comme generer_audio_fpt.py.
"""
import argparse
import hashlib
import html
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generer_audio_fpt as g      # noqa: E402  (même appel https, mêmes messages d'erreur)
import tester_voix_tons as t       # noqa: E402  (mêmes 36 mots, même mesure)

MODELE_ULTRA = 'FPT.TTS-ultra'
VOIX_ULTRA = {          # code d'essai -> (nom affiché, identifiants possibles à sonder)
    'U1': ('Ban Mai', ['std_banmai', 'banmai', 'fci_banmai']),
    'U2': ('Viet Khoa', ['fci_vietkhoa', 'vietkhoa', 'std_vietkhoa']),
    'U3': ('Minh Quang', ['std_minhquang', 'minhquang', 'fci_minhquang']),
    'U4': ('Quang Anh', ['std_quanganh', 'quanganh', 'fci_quanganh']),
    'U5': ('Xuan Toan', ['fci_xuantoan']),
    'U6': ('Phuong An', ['fci_phuongan']),
    'U7': ('Kim Ngan', ['std_kimngan']),
}

# Test d'accent Nord / Sud (--accent) : (texte, ce qu'on attend à Hanoï, ce qu'on entend au Sud)
TEST_ACCENT = [
    ('ra', 'r- = « z »', 'r- roulé ou « r »'),
    ('rau', 'r- = « z »', 'r- roulé ou « r »'),
    ('da', 'd- = « z »', 'd- = « y »'),
    ('gia', 'gi- = « z »', 'gi- = « y »'),
    ('vui', 'v- = « v »', 'v- proche de « y »'),
    ('sáu', 's- = « s », comme x-', 's- chuintant « ch »'),
    ('xấu', 'x- = « s »', 'x- = « s »'),
    ('tre', 'tr- = « tch », comme ch-', 'tr- rétroflexe, distinct de ch-'),
    ('che', 'ch- = « tch »', 'ch- = « tch »'),
    ('bạn', 'finale -n', 'finale -ng'),
    ('mắt', 'finale -t', 'finale -c (« mắc »)'),
    ('bảo', 'hỏi : descend puis remonte, voix tendue', 'hỏi et ngã identiques'),
    ('bão', 'ngã : monte, coupé au milieu', 'hỏi et ngã identiques'),
    ('Tôi rất vui được gặp bạn.', 'phrase', 'phrase'),
    ('Hôm nay trời rất đẹp.', 'phrase', 'phrase'),
]
REFERENCES = {'F1': 'Ban Mai (TTS-pro, actuelle)', 'H4': 'Huy Phong (VITs, actuel)'}
ACCENT = ['ra', 'rau', 'da', 'dê', 'gia', 'gì', 'sa', 'xa', 'tra', 'cha']


def synthetiser_ultra(texte, cle, voix):
    """Comme g.synthetiser, mais envoie le texte sous les deux noms de champ (« input » pour
    l'API de type OpenAI, « text » dans l'exemple de la fiche Ultra)."""
    corps = {'model': MODELE_ULTRA, 'input': texte, 'text': texte, 'speed': 1.0, 'response_format': 'mp3'}
    if voix:
        corps['voice'] = voix
    req = urllib.request.Request(g.API_URL, data=json.dumps(corps, ensure_ascii=False).encode('utf-8'),
                                 method='POST', headers={'Authorization': 'Bearer ' + cle,
                                                         'Content-Type': 'application/json'})
    type_contenu, contenu = g.avec_patience(lambda: g.ouvrir(req, 60), 'la demande')
    if 'json' in type_contenu or contenu[:1] in (b'{', b'['):
        raise RuntimeError('réponse JSON au lieu d\'un audio : ' + contenu.decode('utf-8', 'replace')[:300])
    if len(contenu) < 500:
        raise RuntimeError(f'fichier trop petit ({len(contenu)} octets)')
    return contenu


def cle_api():
    cle = os.environ.get('FPT_MKP_API_KEY')
    if not cle:
        sys.exit("La variable FPT_MKP_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")
    return cle


def sonde(dossier):
    cle = cle_api()
    rep = os.path.join(dossier, '_sonde')
    os.makedirs(rep, exist_ok=True)
    print('Voix par défaut (sans identifiant) … ', end='', flush=True)
    try:
        c = synthetiser_ultra('ba', cle, None)
        open(os.path.join(rep, 'ba-defaut.mp3'), 'wb').write(c)
        print('ok, empreinte', hashlib.md5(c).hexdigest()[:8])
    except Exception as e:
        print('erreur :', e)
    for code, (nom, ids) in VOIX_ULTRA.items():
        for vid in ids:
            print(f'{code} {nom:11} {vid:16} … ', end='', flush=True)
            try:
                c = synthetiser_ultra('ba', cle, vid)
                open(os.path.join(rep, f'ba-{vid}.mp3'), 'wb').write(c)
                print('accepté, empreinte', hashlib.md5(c).hexdigest()[:8])
            except Exception as e:
                print('refusé :', str(e)[:160])
            time.sleep(g.DELAI_ENTRE_APPELS)
    print(f'\nFichiers à écouter : {rep}')
    print('Gardez pour chaque voix un identifiant « accepté » dont l\'empreinte diffère des autres voix.')


def liste_items(mots):
    """(référence de fichier, texte) : 36 mots des tons puis syllabes d'accent."""
    items = [(m, mots[m]) for ton in t.TONS for m in t.MOTS[ton]]
    return items + [('S-' + g.telex(s), s) for s in ACCENT]


def chemin(dossier, ref, code):
    return os.path.join(dossier, f'{ref}-{code}-normal.mp3')


def generer(dossier, ids, items, executer):
    manquants = [(ref, txt, code) for code in ids for ref, txt in items if not os.path.exists(chemin(dossier, ref, code))]
    print(f'{len(manquants)} audio(s) à générer (environ {sum(len(x[1]) for x in manquants)} caractères) ; '
          + ', '.join(f'{c} = {VOIX_ULTRA[c][0]} ({v})' for c, v in ids.items()))
    if not manquants:
        return
    if not executer:
        print('Plan seulement. Ajoutez --executer pour les générer.')
        sys.exit(0)
    import decoupe_audio
    cle = cle_api()
    bruts = os.path.join(dossier, '_bruts')
    os.makedirs(bruts, exist_ok=True)
    erreurs = 0
    for i, (ref, txt, code) in enumerate(manquants, 1):
        print(f'[{i}/{len(manquants)}] {txt} · {code} … ', end='', flush=True)
        try:
            contenu = synthetiser_ultra(txt, cle, ids[code])
            brut = os.path.join(bruts, os.path.basename(chemin(dossier, ref, code)))
            open(brut, 'wb').write(contenu)
            decoupe_audio.traiter_fichier(brut, chemin(dossier, ref, code))   # même égalisation de volume
            print('ok')
        except Exception as e:
            erreurs += 1
            print('erreur :', e)
            if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                sys.exit('Arrêt : problème de clé ou de solde.')
        time.sleep(g.DELAI_ENTRE_APPELS)
    print(f'Génération terminée, {erreurs} erreur(s). Relancez sans --executer pour la mesure et la page d\'écoute.')
    sys.exit(0)


def mesurer_tout(donnees, dossier, ids):
    import courbes_modele as cm
    voix = {c: (VOIX_ULTRA[c][0] + ' (Ultra)', lambda m, c=c: chemin(dossier, m, c)) for c in ids}
    for c, nom in REFERENCES.items():
        if all(os.path.exists(t.chemin_audio(donnees, m, c)) for ton in t.TONS for m in t.MOTS[ton]):
            voix[c] = (nom, lambda m, c=c: t.chemin_audio(donnees, m, c))
    res = {}
    for c, (nom, ch) in voix.items():
        print(f'Mesure de {nom}…', flush=True)
        r = t.mesurer({ton: [cm.courbe_fichier(ch(m)) for m in t.MOTS[ton]] for ton in t.TONS})
        att = [t.attaque(ch(m)) for m in t.ATTAQUES]
        r['silence'] = sum(a for a, _ in att) / len(att)
        r['consonne'] = sum(b for _, b in att) / len(att)
        res[c] = r
    print('\n' + 'Voix'.ljust(30) + 'Reconnus  Contraste  ' + '  '.join(f'{a}/{b}' for a, b in t.PAIRES) + '  Silence  Consonne')
    for c in sorted(res, key=lambda c: -res[c]['contraste']):
        r = res[c]
        print(voix[c][0][:29].ljust(30) + f"{r['reconnus'] * 100:6.0f} %  {r['contraste']:8.2f}   "
              + '  '.join(f'{r["paires"][p]:{len(p[0]) + len(p[1]) + 1}.2f}' for p in t.PAIRES)
              + f"  {r['silence']:5.0f} ms {r['consonne']:5.0f} ms")
    print('\nLecture : « Reconnus » et « Contraste » plus hauts = tons mieux distincts ; '
          '« Consonne » très courte = début de mot tronqué.')
    return voix


def page_ecoute(dossier, donnees, voix, items):
    lignes = []
    for ref, txt in items:
        cellules = []
        for c, (_, ch) in voix.items():
            f = ch(ref) if not ref.startswith('S-') or c in VOIX_ULTRA else None
            if f and os.path.exists(f):
                src = os.path.relpath(f, dossier).replace(os.sep, '/')
                cellules.append(f'<td><audio controls preload="none" src="{html.escape(src)}"></audio></td>')
            else:
                cellules.append('<td>—</td>')
        lignes.append(f'<tr><th>{html.escape(txt)}</th>{"".join(cellules)}</tr>')
    entete = ''.join(f'<th>{html.escape(n)}</th>' for n, _ in voix.values())
    page = ('<!doctype html><meta charset="utf-8"><title>Essai FPT.TTS-ultra</title>'
            '<style>body{font-family:sans-serif;margin:16px}table{border-collapse:collapse}'
            'td,th{border:1px solid #ccc;padding:4px 8px}th{text-align:left}audio{width:160px}</style>'
            '<h1>Essai FPT.TTS-ultra — voix du Nord</h1>'
            '<p>À écouter : tons (mả / mã bien distincts), accent du Nord (r-, d-, gi- prononcés « z »), '
            'début de mot non coupé.</p>'
            f'<table><tr><th>Mot</th>{entete}</tr>{"".join(lignes)}</table>')
    sortie = os.path.join(dossier, 'ecoute.html')
    open(sortie, 'w', encoding='utf-8').write(page)
    print('\nPage d\'écoute :', os.path.abspath(sortie))


def test_accent(dossier, ids, executer):
    """Petit test d'écoute Nord / Sud : TEST_ACCENT dit par chaque voix, page accent.html."""
    rep = os.path.join(dossier, 'accent')
    os.makedirs(rep, exist_ok=True)
    def fichier(i, code):
        return os.path.join(rep, f'{i:02d}-{code}.mp3')
    manquants = [(i, txt, code) for code in ids for i, (txt, _, _) in enumerate(TEST_ACCENT, 1)
                 if not os.path.exists(fichier(i, code))]
    print(f'{len(manquants)} audio(s) à générer ; ' + ', '.join(f'{c} = {VOIX_ULTRA[c][0]} ({v})' for c, v in ids.items()))
    if manquants and not executer:
        print('Plan seulement. Ajoutez --executer pour les générer.')
        return
    if manquants:
        import decoupe_audio
        cle = cle_api()
        bruts = os.path.join(rep, '_bruts')
        os.makedirs(bruts, exist_ok=True)
        for n, (i, txt, code) in enumerate(manquants, 1):
            print(f'[{n}/{len(manquants)}] {txt} · {code} … ', end='', flush=True)
            try:
                brut = os.path.join(bruts, os.path.basename(fichier(i, code)))
                open(brut, 'wb').write(synthetiser_ultra(txt, cle, ids[code]))
                decoupe_audio.traiter_fichier(brut, fichier(i, code))
                print('ok')
            except Exception as e:
                print('erreur :', e)
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    sys.exit('Arrêt : problème de clé ou de solde.')
            time.sleep(g.DELAI_ENTRE_APPELS)
    lignes = []
    for i, (txt, nord, sud) in enumerate(TEST_ACCENT, 1):
        cel = ''.join(f'<td><audio controls preload="none" src="{i:02d}-{c}.mp3"></audio></td>'
                      if os.path.exists(fichier(i, c)) else '<td>—</td>' for c in ids)
        lignes.append(f'<tr><th>{html.escape(txt)}</th><td>{html.escape(nord)}</td><td>{html.escape(sud)}</td>{cel}</tr>')
    entete = ''.join(f'<th>{html.escape(VOIX_ULTRA[c][0])}</th>' for c in ids)
    page = ('<!doctype html><meta charset="utf-8"><title>Test accent Ultra</title>'
            '<style>body{font-family:sans-serif;margin:16px}table{border-collapse:collapse}'
            'td,th{border:1px solid #ccc;padding:4px 8px;text-align:left}audio{width:150px}</style>'
            '<h1>FPT.TTS-ultra — accent du Nord ou du Sud ?</h1>'
            '<p>Pour chaque ligne : la voix ressemble-t-elle à la colonne « Hanoï » ou à la colonne « Sud » ?</p>'
            f'<table><tr><th>Texte</th><th>Hanoï</th><th>Sud</th>{entete}</tr>{"".join(lignes)}</table>')
    open(os.path.join(rep, 'accent.html'), 'w', encoding='utf-8').write(page)
    print('Page d\'écoute :', os.path.abspath(os.path.join(rep, 'accent.html')))


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--sonde', action='store_true', help='étape 1 : trouver les identifiants des voix')
    a.add_argument('--ids', help='identifiants retenus, par ex. U1=std_banmai,U2=fci_vietkhoa')
    a.add_argument('--accent', action='store_true', help="petit test d'écoute Nord / Sud (page accent.html)")
    a.add_argument('--executer', action='store_true', help='appeler FPT (sinon : plan seulement)')
    args = a.parse_args()
    donnees = os.path.join(args.racine, '04_DONNEES')
    dossier = os.path.join(donnees, 'audio', '_essais', 'ultra')
    os.makedirs(dossier, exist_ok=True)
    if args.sonde:
        return sonde(dossier)
    if not args.ids:
        sys.exit('Indiquez --ids (résultat de la sonde), par ex. --ids U1=std_banmai,U2=fci_vietkhoa')
    ids = dict(x.split('=', 1) for x in args.ids.split(','))
    inconnus = [c for c in ids if c not in VOIX_ULTRA]
    if inconnus:
        sys.exit('Codes inconnus : ' + ', '.join(inconnus) + ' (attendus : U1 à U7)')
    if args.accent:
        return test_accent(dossier, ids, args.executer)
    mots = {m['word_code']: m['written'] for m in t.lire(os.path.join(donnees, 'mots.csv'))}
    items = liste_items(mots)
    generer(dossier, ids, items, args.executer)
    try:
        import numpy, soundfile   # noqa: F401
    except ImportError:
        sys.exit('numpy et soundfile sont nécessaires : lancer avec .venv-asr\\Scripts\\python.exe')
    voix = mesurer_tout(donnees, dossier, ids)
    page_ecoute(dossier, donnees, voix, items)


if __name__ == '__main__':
    main()
