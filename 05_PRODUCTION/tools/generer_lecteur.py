# -*- coding: utf-8 -*-
"""
Génère le lecteur d'activités à partir de 04_DONNEES (DEC-0017, DEC-0030).

Entrées  : 04_DONNEES/*.csv (source unique)
           05_PRODUCTION/lecteur/ (code du lecteur, fichiers provisoires)
Sortie   : 06_LIVRABLES/lecteur/  (regénérable, hors Git : DOC-03)
             index.html, lecteur.css, lecteur.js, donnees.js, audio/ (si présent)
             lecteur_autonome.html (tout en un seul fichier, pour l'envoyer ou l'essayer ailleurs)

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\generer_lecteur.py .

Ne modifie aucun fichier source. Ne nécessite aucune bibliothèque extérieure.
"""
import csv
import datetime
import json
import os
import shutil
import sys

RACINE = sys.argv[1] if len(sys.argv) > 1 else '.'
DONNEES = os.path.join(RACINE, '04_DONNEES')
LECTEUR = os.path.join(RACINE, '05_PRODUCTION', 'lecteur')
SORTIE = os.path.join(RACINE, '06_LIVRABLES', 'lecteur')

# Paramètres du verrou d'écoute (R-VOL-05, DEC-0032) et du lecteur (PROG-ACT).
PARAMETRES = {
    'fenetre_score': 20,          # nombre de dernières réponses prises en compte
    'min_reussites_par_serie': 2, # au débit normal (DEC-0032)
    'min_voix': 2,                # R-VOL-05
    'max_meme_position': 3,       # PROG-ACT § 4 : pas plus de 3 fois de suite la même bonne réponse
    'ecart_max_lecons': 3,        # R-VOL-04 (non contrôlé tant que le volet production n'existe pas)
}

# Réglages provisoires de la synthèse vocale du navigateur, en attendant les audios
# FPT.AI (DEC-0023). Les « voix » F1, F2, H1 sont simulées par la hauteur de voix.
VOIX_PROVISOIRES = {
    'F1': {'hauteur': 1.15, 'vitesse': 1.0},
    'F2': {'hauteur': 1.4, 'vitesse': 0.95},
    'H1': {'hauteur': 0.7, 'vitesse': 1.0},
}
DEBITS = {'slow': 0.55, 'normal': 0.9}

ORDRE_POSITIONS = {'nucleus': 0, 'glide': 0, 'initial': 1, 'final': 2}


def lire(nom, dossier=DONNEES):
    chemin = os.path.join(dossier, nom)
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def main():
    lecons = lire('lecons.csv')
    mots = {m['word_code']: m for m in lire('mots.csv')}
    sons = {s['sound_code']: s for s in lire('sons.csv')}
    tons = {t['tone_code']: t for t in lire('tons.csv')}
    paires = lire('paires_minimales.csv')
    voix = [v for v in lire('voix.csv') if v['status'] == 'active']
    audios = lire('audios.csv')
    images = {i['word_code']: i for i in lire('images.csv')}
    images_prov = {i['word_code']: i['emoji'] for i in lire('images_provisoires.csv', LECTEUR)}
    indications = {i['symbole']: i['indication'] for i in lire('indications_symboles.csv', LECTEUR)}

    # Audios validés : (référence, voix, débit) -> fichier
    fichiers_audio = {}
    for a in audios:
        if a.get('validated') == 'true':
            fichiers_audio[(a['item_ref'], a['voice'], a['speed'])] = a['file']

    def symbole(element):
        if element in tons:
            t = tons[element]
            return {'texte': t['pictogram'], 'couleur': t['color_hex'], 'nom': t['name_vi'],
                    'indication': 'ton ' + t['name_vi'] + ' : ' + t['contour_fr']}
        s = sons.get(element)
        if not s:
            raise SystemExit('Élément inconnu : ' + element)
        principal = s['ipa_main']
        return {'texte': '/' + principal + '/', 'couleur': '', 'nom': s['grapheme'],
                'indication': indications.get(principal, '')}

    def audio(ref):
        res = {}
        for v in voix:
            for d in DEBITS:
                f = fichiers_audio.get((ref, v['voice_code'], d))
                if f:
                    res.setdefault(v['voice_code'], {})[d] = f
        return res

    series = {}
    for p in paires:
        series.setdefault(p['series_code'], []).append(p)

    sortie_lecons = []
    for l in sorted(lecons, key=lambda x: int(x['sort_order'])):
        code = l['lesson_code']
        liste = []
        for sc, termes in series.items():
            if termes[0]['lesson_code'] != code:
                continue
            termes = sorted(termes, key=lambda t: int(t['position']))
            premier = termes[0]['element']
            groupe = 0 if premier in tons else ORDRE_POSITIONS.get(sons[premier]['position'], 3)
            sortie_termes = []
            for t in termes:
                m = mots.get(t['word_code']) if t['word_code'] else None
                invente = t['invented'] == 'true'
                image = ''
                if m and m['imageable'] == 'true' and not invente:
                    image = images_prov.get(m['word_code'], '')  # images.csv vide : emoji provisoire
                ref = t['word_code'] or t['written']
                sortie_termes.append({
                    'position': int(t['position']),
                    'ecrit': t['written'],          # jamais affiché si invente (R-LEX-06)
                    'sens': m['meaning_fr'].split(' / ')[0] if m else '',
                    'invente': invente,
                    'element': t['element'],
                    'symbole': symbole(t['element']),
                    'image': image,
                    'audio': audio(ref),
                })
            liste.append({'code': sc, 'type': termes[0]['contrast_type'], 'groupe': groupe,
                          'termes': sortie_termes})
        liste.sort(key=lambda s: (s['groupe'], s['code']))
        sortie_lecons.append({
            'code': code,
            'numero': int(l['sort_order']),
            'titre': l['family_fr'],
            'seuil': float(l['listen_threshold']),
            'tons': l['is_tone_lesson'] == 'true',
            'recyclage': l['is_recycling'] == 'true',
            'series': liste,
        })

    donnees = {
        'genere_le': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'parametres': PARAMETRES,
        'voix': [{'code': v['voice_code'], 'genre': v['gender'], **VOIX_PROVISOIRES.get(v['voice_code'], {})}
                 for v in voix],
        'debits': DEBITS,
        'lecons': sortie_lecons,
    }

    os.makedirs(SORTIE, exist_ok=True)
    js = 'window.DONNEES_LECTEUR = ' + json.dumps(donnees, ensure_ascii=False, indent=1) + ';\n'
    with open(os.path.join(SORTIE, 'donnees.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
    for nom in ['index.html', 'lecteur.css', 'lecteur.js']:
        shutil.copyfile(os.path.join(LECTEUR, nom), os.path.join(SORTIE, nom))
    # Audios validés copiés à côté du lecteur
    for f in set(fichiers_audio.values()):
        src = os.path.join(DONNEES, f)
        dst = os.path.join(SORTIE, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)

    # Version en un seul fichier
    with open(os.path.join(LECTEUR, 'index.html'), encoding='utf-8') as f:
        page = f.read()
    with open(os.path.join(LECTEUR, 'lecteur.css'), encoding='utf-8') as f:
        css = f.read()
    with open(os.path.join(LECTEUR, 'lecteur.js'), encoding='utf-8') as f:
        code = f.read()
    page = page.replace('<link rel="stylesheet" href="lecteur.css">', '<style>\n' + css + '\n</style>')
    page = page.replace('<script src="donnees.js"></script>', '<script>\n' + js + '</script>')
    page = page.replace('<script src="lecteur.js"></script>', '<script>\n' + code + '\n</script>')
    with open(os.path.join(SORTIE, 'lecteur_autonome.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)

    nb_series = sum(len(l['series']) for l in sortie_lecons)
    print(f"{len(sortie_lecons)} leçons, {nb_series} séries, {len(fichiers_audio)} audios validés -> {SORTIE}")


if __name__ == '__main__':
    main()
