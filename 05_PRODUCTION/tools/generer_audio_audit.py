# -*- coding: utf-8 -*-
"""
Audit des locuteurs FPT (MOD-C17, DEC-0076) — premier passage rapide.

Produit une batterie courte pour juger chaque voix sur 4 dimensions :
  1. voyelles seules (ê, o, i)
  2. syllabe CV sans sens (te)
  3. syllabe VC sans sens avec finale -m (em)
  4. ralenti (mêmes items ci-dessus, débit lent)
  5. espacement (1 phrase courte de comptage.csv : « Tôi ăn nem. », mots espacés)

Voix testées (9) : F1, F3, F4, H1, H2, H3, H4, H5, H6.
  - F2 : aucun provider_model dans voix.csv, non générable.
  - E1 : voix d'enfant, aucun fournisseur, non générable (DEC-0023).
  - F4 Ultra et H6 Ultra : débit « slow » redirigé vers F1 et H4 (slow_from, DEC-0067).

Les audios sortent dans 07_QUALITE/audit_locuteurs/audio/, indexés dans
07_QUALITE/audit_locuteurs/audios_audit.csv (validated = false, à écouter).

Clé d'accès : variable d'environnement FPT_MKP_API_KEY (comme generer_audio_fpt.py).

Usage (depuis C:\\VIET_PROJECT) :
  .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_audit.py .
      -> plan seulement (gratuit)
  .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_audit.py . --executer
      -> lance la génération (coût : voir le plan)
  .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_audit.py . --executer --debit normal
      -> seulement les ~45 audios en débit normal (triage très rapide)
  .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_audit.py . --executer --voix F4,H6
      -> seulement F4 et H6

Peut être arrêté (Ctrl+C) et relancé : les fichiers déjà présents sont sautés.
"""
import argparse
import csv
import os
import sys
import time

# Même dossier que generer_audio_fpt.py : réutilisation directe.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generer_audio_fpt as g

# --- Batterie d'audit ---------------------------------------------------------

ITEMS_SIMPLES = [
    # (ref, texte envoyé à FPT, nature)
    ('AUD-V-ee', 'ê',  'voyelle'),
    ('AUD-V-o',  'o',  'voyelle'),
    ('AUD-V-i',  'i',  'voyelle'),
    ('AUD-S-te', 'te', 'syllabe-CV'),
    ('AUD-S-em', 'em', 'syllabe-VC-m'),
]
PHRASE = {
    'ref': 'AUD-P-toi-an-nem',
    'texte_normal': 'Tôi ăn nem.',
    'texte_espace': 'Tôi, ăn, nem.',    # mots espacés par virgules (DEC-0067)
    'source': 'P-L01-01 (comptage.csv)',
}
VOIX_AUDIT = ['F1', 'F3', 'F4', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']
DEBITS_SIMPLES = ['normal', 'slow']
DEBIT_PHRASE = 'spaced'
VITESSE_DEFAUT_SLOW = 0.8
VITESSE_NORMALE = 1.0

COLONNES_AUDIT = [
    'audio_code', 'item_ref', 'nature', 'voice_requested', 'voice_actual',
    'debit', 'speed_fpt', 'text_sent', 'file', 'validated', 'note',
]


# --- Plan ---------------------------------------------------------------------

def vitesse_pour(voix_info, debit):
    if debit == 'slow':
        if voix_info.get('provider_speed_slow'):
            return float(voix_info['provider_speed_slow'])
        return VITESSE_DEFAUT_SLOW
    return VITESSE_NORMALE


def plan_audit(donnees):
    toutes = {v['voice_code']: v for v in g.lire(os.path.join(donnees, 'voix.csv'))}
    items = []
    exclues = []

    for v in VOIX_AUDIT:
        info = toutes.get(v)
        if not info:
            exclues.append((v, 'absente de voix.csv'))
            continue
        has_slow_from = bool(info.get('slow_from'))
        has_own_model = bool(info.get('provider_model'))
        # Vérifs : si pas de provider_model, et pas de slow_from vers une voix avec un provider_model, inutilisable.
        if not has_own_model and not (has_slow_from and toutes.get(info['slow_from'], {}).get('provider_model')):
            exclues.append((v, 'ni provider_model, ni slow_from utilisable'))
            continue

        # Items simples au débit normal
        if has_own_model:
            for ref, texte, nature in ITEMS_SIMPLES:
                items.append({
                    'ref': ref, 'texte': texte, 'nature': nature,
                    'voix_voulue': v, 'voix_reelle': v,
                    'debit': 'normal',
                    'provider_voice': info['provider_voice'],
                    'provider_model': info['provider_model'],
                    'vitesse_fpt': vitesse_pour(info, 'normal'),
                })

        # Items simples au débit slow (avec redirection slow_from si besoin)
        voix_slow = info['slow_from'] if has_slow_from else v
        info_slow = toutes.get(voix_slow)
        if info_slow and info_slow.get('provider_model'):
            for ref, texte, nature in ITEMS_SIMPLES:
                items.append({
                    'ref': ref, 'texte': texte, 'nature': nature,
                    'voix_voulue': v, 'voix_reelle': voix_slow,
                    'debit': 'slow',
                    'provider_voice': info_slow['provider_voice'],
                    'provider_model': info_slow['provider_model'],
                    'vitesse_fpt': vitesse_pour(info_slow, 'slow'),
                })

        # Phrase espacée (débit spaced = vitesse normale, DEC-0058/DEC-0067)
        if has_own_model:
            items.append({
                'ref': PHRASE['ref'], 'texte': PHRASE['texte_espace'],
                'nature': 'phrase-espacement',
                'voix_voulue': v, 'voix_reelle': v,
                'debit': DEBIT_PHRASE,
                'provider_voice': info['provider_voice'],
                'provider_model': info['provider_model'],
                'vitesse_fpt': VITESSE_NORMALE,
            })

    # Déduplication : si deux (voix_voulue) différentes retombent sur la même
    # (ref, voix_reelle, debit), on ne garde qu'une occurrence et on note les voix voulues couvertes.
    uniques = {}
    for i in items:
        cle = (i['ref'], i['voix_reelle'], i['debit'])
        if cle not in uniques:
            uniques[cle] = dict(i, voix_voulues=[i['voix_voulue']])
        else:
            if i['voix_voulue'] not in uniques[cle]['voix_voulues']:
                uniques[cle]['voix_voulues'].append(i['voix_voulue'])

    return list(uniques.values()), exclues


def nom_fichier(item):
    return f"{item['ref']}-{item['voix_reelle']}-{item['debit']}.mp3"


# --- Exécution ----------------------------------------------------------------

def main():
    a = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    a.add_argument('racine', nargs='?', default='.')
    a.add_argument('--executer', action='store_true',
                   help='appeler FPT (sinon : plan seulement)')
    a.add_argument('--voix', help='filtrer sur certaines voix voulues, par ex. F4,H6')
    a.add_argument('--item', help='filtrer sur certaines refs, par ex. AUD-V-ee,AUD-S-te')
    a.add_argument('--debit', help='filtrer sur certains débits : normal, slow, spaced')
    args = a.parse_args()

    donnees = os.path.join(args.racine, '04_DONNEES')
    sortie = os.path.join(args.racine, '07_QUALITE', 'audit_locuteurs')
    audio_dir = os.path.join(sortie, 'audio')
    index_csv = os.path.join(sortie, 'audios_audit.csv')

    items, exclues = plan_audit(donnees)

    if args.voix:
        voulues = set(args.voix.split(','))
        items = [i for i in items if any(vv in voulues for vv in i['voix_voulues'])]
    if args.item:
        refs = set(args.item.split(','))
        items = [i for i in items if i['ref'] in refs]
    if args.debit:
        debits = set(args.debit.split(','))
        items = [i for i in items if i['debit'] in debits]

    existants = set()
    if os.path.exists(index_csv):
        for r in g.lire(index_csv):
            existants.add(r['file'])
    def chemin_relatif(i):
        return os.path.join('07_QUALITE', 'audit_locuteurs', 'audio', nom_fichier(i)).replace('\\', '/')
    manquants = [i for i in items
                 if chemin_relatif(i) not in existants
                 and not os.path.exists(os.path.join(audio_dir, nom_fichier(i)))]

    caracteres = sum(len(i['texte']) for i in manquants)
    print(f"Batterie d'audit (MOD-C17, DEC-0076)")
    print(f"Items prévus : {len(items)}  |  déjà présents : {len(items) - len(manquants)}  |  "
          f"à créer : {len(manquants)}  (~{caracteres} caractères envoyés à FPT)")
    print(f"Sortie : {audio_dir}")
    if exclues:
        print(f"Voix exclues : " + ', '.join(f'{v} ({r})' for v, r in exclues))
    print()
    for i in manquants[:20]:
        vv = ','.join(i['voix_voulues'])
        suffix = f" via {i['voix_reelle']}" if i['voix_reelle'] not in i['voix_voulues'] else ""
        print(f"  {i['ref']:16s} {i['texte']:14s} {vv:8s}{suffix:12s} {i['debit']:7s} "
              f"({i['provider_model']} @ {i['vitesse_fpt']}) -> {nom_fichier(i)}")
    if len(manquants) > 20:
        print(f"  ... et {len(manquants) - 20} autres")

    if not args.executer:
        print("\nPlan seulement. Ajoutez --executer pour lancer la génération.")
        return

    # --- Exécution réelle ---
    print('\nVérification https :', g.VERIFICATION)
    try:
        import numpy, soundfile    # noqa: F401
    except ImportError:
        sys.exit("numpy et soundfile sont nécessaires. Lancez avec .venv-asr\\Scripts\\python.exe.")
    cle = os.environ.get('FPT_MKP_API_KEY')
    if not cle:
        sys.exit("La variable FPT_MKP_API_KEY n'est pas définie (voir 05_PRODUCTION/03_audio.md).")

    os.makedirs(audio_dir, exist_ok=True)
    nouveau_index = not os.path.exists(index_csv) or os.path.getsize(index_csv) == 0
    crees = erreurs = 0
    with open(index_csv, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';', lineterminator='\n')
        if nouveau_index:
            w.writerow(COLONNES_AUDIT)
        for n, i in enumerate(manquants, 1):
            fichier = nom_fichier(i)
            destination = os.path.join(audio_dir, fichier)
            etiquette = ','.join(i['voix_voulues'])
            print(f"[{n}/{len(manquants)}] {i['texte']} · {etiquette} · {i['debit']} ... ",
                  end='', flush=True)
            try:
                g.produire(i['texte'], cle, i['provider_voice'], i['vitesse_fpt'],
                           destination, i['provider_model'])
                base = fichier[:-4]
                w.writerow([
                    'A-' + base, i['ref'], i['nature'],
                    etiquette, i['voix_reelle'], i['debit'],
                    f"{i['vitesse_fpt']:.2f}", i['texte'],
                    chemin_relatif(i), 'false', '',
                ])
                f.flush()
                crees += 1
                print('ok')
            except Exception as e:
                erreurs += 1
                print('erreur :', e)
                if 'HTTP 401' in str(e) or 'HTTP 402' in str(e):
                    sys.exit('Arrêt : clé ou solde FPT problématique.')
                if erreurs >= 5 and crees == 0:
                    sys.exit('Cinq erreurs sans aucun succès : arrêt.')
            time.sleep(g.DELAI_ENTRE_APPELS)
    print(f"\nTerminé : {crees} audio(s) créé(s), {erreurs} erreur(s).")
    print(f"Index : {index_csv}")


if __name__ == '__main__':
    main()
