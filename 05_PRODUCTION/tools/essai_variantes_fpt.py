# -*- coding: utf-8 -*-
"""
Essai : trouver comment écrire le texte envoyé à FPT.TTS-pro pour que les mots
isolés ne soient pas « tronqués » (consonne de départ avalée), surtout avec les voix d'homme.

Fait prononcer un même mot sous plusieurs écritures, par chaque voix active de voix.csv.
Les fichiers vont dans 04_DONNEES/audio/_essais/ ; audios.csv n'est PAS modifié.

Usage (depuis C:\\VIET_PROJECT) :
    python 05_PRODUCTION\\tools\\essai_variantes_fpt.py .            -> liste des essais, rien n'est appelé
    python 05_PRODUCTION\\tools\\essai_variantes_fpt.py . --executer
    python 05_PRODUCTION\\tools\\essai_variantes_fpt.py . --executer --mot xen
    Autre modèle et autres voix (identifiants relevés dans Voice Studio, bouton View Code) :
    python 05_PRODUCTION\\tools\\essai_variantes_fpt.py . --executer --modele FPT.AI-VITs --voix voix1,voix2
    Vitesses (mot seul, voix actives avec leur modèle de voix.csv) :
    python 05_PRODUCTION\\tools\\essai_variantes_fpt.py . --executer --variantes 1 --vitesses 0.7,0.6,0.5
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generer_audio_fpt as g   # même appel au service, même clé (FPT_MKP_API_KEY)

# (code court pour le nom du fichier, gabarit du texte envoyé)
VARIANTES = [
    ('1-brut',      '{m}'),          # comme aujourd'hui
    ('2-point',     '{m}.'),         # point final
    ('3-majuscule', '{M}.'),         # majuscule + point
    ('4-virgule',   ', {m}.'),       # virgule devant : petite pause avant le mot
    ('5-points',    '... {m} ...'),  # pause avant et après
    ('6-double',    '{m}, {m}.'),    # mot répété (à découper ensuite si c'est la seule solution)
]


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true')
    a.add_argument('--mot', default='xem')
    a.add_argument('--modele', help='nom du modèle FPT (par défaut : celui de chaque voix dans voix.csv)')
    a.add_argument('--vitesses', default='1.0', help='valeurs de speed séparées par des virgules (par défaut 1.0)')
    a.add_argument('--voix', help="identifiants FPT des voix, séparés par des virgules (par défaut : voix actives de voix.csv)")
    a.add_argument('--variantes', default='1,2,6', help='numéros des variantes à essayer (par défaut 1,2,6)')
    args = a.parse_args()

    donnees = os.path.join(args.racine, '04_DONNEES')
    voix = {v['voice_code']: (v['provider_voice'], v.get('provider_model') or g.MODELE)
            for v in g.lire(os.path.join(donnees, 'voix.csv'))
            if v['status'] == 'active' and v['provider'] == g.FOURNISSEUR}
    if args.voix:
        voix = {v.strip(): (v.strip(), args.modele or g.MODELE) for v in args.voix.split(',') if v.strip()}
    elif args.modele:
        voix = {c: (v, args.modele) for c, (v, _) in voix.items()}
    vitesses = [float(s) for s in args.vitesses.split(',') if s.strip()]
    choisies = [v for v in VARIANTES if v[0].split('-')[0] in args.variantes.split(',')]
    dossier = os.path.join(donnees, 'audio', '_essais', args.modele.replace('/', '_') if args.modele else 'vitesses')
    mot = args.mot
    essais = [(code_v, nom_v, modele, vit, code, gabarit.format(m=mot, M=mot[:1].upper() + mot[1:]))
              for code_v, (nom_v, modele) in voix.items() for vit in vitesses for code, gabarit in choisies]
    print(f"{len(essais)} essais pour « {mot} », dossier {dossier}")
    for code_v, _, modele, vit, code, texte in essais:
        print(f"   {code_v} ({modele}) vitesse {vit} {code:12s} texte envoyé : « {texte} »")
    if not args.executer:
        print("Liste seulement. Ajoutez --executer pour lancer les essais.")
        return
    cle = os.environ.get('FPT_MKP_API_KEY')
    if not cle:
        sys.exit("La variable FPT_MKP_API_KEY n'est pas définie.")
    os.makedirs(dossier, exist_ok=True)
    base = 'S-' + g.telex(mot)
    for n, (code_v, nom_v, modele, vit, code, texte) in enumerate(essais, 1):
        fichier = os.path.join(dossier, f'{base}-{code_v}-v{vit}-{code}.mp3')
        print(f"[{n}/{len(essais)}] {code_v} vitesse {vit} « {texte} » … ", end='', flush=True)
        try:
            contenu = g.synthetiser(texte, cle, nom_v, vit, modele)
            with open(fichier, 'wb') as f:
                f.write(contenu)
            print('ok')
        except Exception as e:
            print('erreur :', e)
            if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                sys.exit('Arrêt : problème de clé ou de solde.')
        time.sleep(g.DELAI_ENTRE_APPELS)
    print(f"Terminé. Écoutez les fichiers de {dossier}")


if __name__ == '__main__':
    main()
