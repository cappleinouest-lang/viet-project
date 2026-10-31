# -*- coding: utf-8 -*-
"""
VALIDATION DES AUDIOS PAR L'ÉCOUTE (R-AUD-01, DEC-0065)
=======================================================

À QUOI IL SERT
    Un audio de synthèse n'est utilisé par le lecteur qu'une fois ÉCOUTÉ et VALIDÉ (validated = true
    dans 04_DONNEES/audios.csv). Ce script fait les deux moitiés du travail :

    1. Sans option : il fabrique la page d'écoute 06_LIVRABLES/validation/validation_audios.html.
       Les audios y sont rangés par leçon, puis par mot (une carte = un mot, une syllabe, une suite
       ou une phrase, avec toutes ses voix et tous ses débits). On écoute, on marque « bon » ou
       « à refaire » (avec la raison), puis on clique « Exporter mes décisions » : le navigateur
       enregistre un fichier validations_audios_<date>.csv dans le dossier Téléchargements.

    2. --appliquer [fichier] : il lit ce fichier (par défaut le plus récent du dossier
       Téléchargements), en garde une copie dans 07_QUALITE/validations/, puis :
         - « bon »        -> validated = true dans audios.csv ;
         - « à refaire »  -> validated = false, et l'audio est inscrit dans
                             07_QUALITE/audios_a_refaire.csv (avec la raison).
       Une décision n'est appliquée que si le fichier audio n'a pas changé depuis la fabrication
       de la page (sinon on aurait validé un autre son que celui écouté).

    Les audios à refaire se regénèrent ensuite avec :
        .venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\generer_audio_fpt.py . --executer --refaire --liste 07_QUALITE\\audios_a_refaire.csv
    puis on refabrique la page : ils y reviennent « à écouter ».

QUELS AUDIOS SONT PROPOSÉS
    Seulement ceux que le plan de génération prévoit aujourd'hui (generer_audio_fpt.plan) : voix
    actives, voix d'écoute du type de leçon, voix modèle d'E4, page des tons. Les audios abandonnés
    (anciennes voix, essai « hai con… » de DEC-0060…) ne sont pas proposés : inutile de les écouter.

USAGE (depuis C:\\VIET_PROJECT)
    python 05_PRODUCTION\\tools\\valider_audios.py .                 -> fabrique la page
    python 05_PRODUCTION\\tools\\valider_audios.py . --appliquer     -> applique le dernier export
    python 05_PRODUCTION\\tools\\valider_audios.py . --appliquer C:\\chemin\\validations_audios_....csv
    Ouvrir ensuite 06_LIVRABLES\\validation\\validation_audios.html (double-clic).

Ce script n'utilise que Python standard. Il ne supprime aucun fichier.
"""
import csv
import datetime
import glob
import json
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import generer_audio_fpt as gen   # noqa: E402  (même plan que la génération : aucune divergence possible)

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
RACINE = ARGS[0] if ARGS else '.'
DONNEES = os.path.join(RACINE, '04_DONNEES')
QUALITE = os.path.join(RACINE, '07_QUALITE')
SORTIE = os.path.join(RACINE, '06_LIVRABLES', 'validation')
CHEMIN_AUDIOS = os.path.join(DONNEES, 'audios.csv')
CHEMIN_A_REFAIRE = os.path.join(QUALITE, 'audios_a_refaire.csv')
COLONNES_A_REFAIRE = ['audio_code', 'file', 'version', 'reason', 'date']
COLONNES_EXPORT = ['audio_code', 'file', 'version', 'decision', 'reason', 'date']
DEBITS = {'slow': 'lent', 'normal': 'normal', 'spaced': 'mots espacés'}
ORDRE_DEBITS = {'slow': 0, 'normal': 1, 'spaced': 2}


def lire(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def ecrire(chemin, colonnes, lignes):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=colonnes, delimiter=';', lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        w.writerows(lignes)


def version(fichier):
    """Empreinte du fichier audio : sa date de modification (change si l'audio est refait)."""
    chemin = os.path.join(DONNEES, fichier)
    return str(int(os.path.getmtime(chemin))) if os.path.exists(chemin) else ''


def nom_voix(v):
    note = v.get('note', '')
    for sep in (' (', ' :', ' ;'):
        note = note.split(sep)[0]
    return note.strip() or v['voice_code']


# ---------------------------------------------------------------------------
# 1. Fabrication de la page
# ---------------------------------------------------------------------------
def fabriquer_page():
    lecons = sorted(lire(os.path.join(DONNEES, 'lecons.csv')), key=lambda l: int(l['sort_order']))
    mots = {m['word_code']: m for m in lire(os.path.join(DONNEES, 'mots.csv'))}
    comptage = {x['item_code']: x for x in lire(os.path.join(DONNEES, 'comptage.csv'))}
    voix = {v['voice_code']: v for v in lire(os.path.join(DONNEES, 'voix.csv'))}
    audios = {a['file']: a for a in lire(CHEMIN_AUDIOS)}
    a_refaire = {x['audio_code']: x for x in lire(CHEMIN_A_REFAIRE)}

    # Leçon de chaque fichier : la première leçon dont le plan le prévoit ; sinon page des tons.
    lecon_de, ordre, items = {}, {}, {}
    for l in lecons:
        for i in gen.plan(DONNEES, l['lesson_code'])[0]:
            f = gen.nom_fichier(i)
            if f not in lecon_de:
                lecon_de[f] = l['lesson_code']
                ordre[f] = len(ordre)
                items[f] = i
    for i in gen.plan(DONNEES)[0]:
        f = gen.nom_fichier(i)
        if f not in lecon_de:
            lecon_de[f] = 'TONS'
            ordre[f] = len(ordre)
            items[f] = i

    def description(i):
        ref, t = i['ref'], i['type']
        if t == 'word':
            m = mots.get(ref, {})
            return m.get('written', i['ecrit']), m.get('meaning_fr', '').split(' / ')[0], 'mot'
        if t == 'invented':
            return i['ecrit'], '', 'syllabe inventée'
        if t == 'syllable':
            return i['ecrit'], '', 'syllabe hors corpus'
        if ref.startswith('K-'):
            m = mots.get(ref[2:], {})
            return i['ecrit'], m.get('meaning_fr', '').split(' / ')[0], 'classificateur + nom'
        x = comptage.get(ref, {})
        if x.get('kind') == 'phrase':
            return x.get('written', i['ecrit']), x.get('note', ''), 'phrase « Combien de fois ? »'
        return x.get('written', i['ecrit']), '', 'suite « Combien de fois ? »'

    cartes, absents, non_declares = {}, 0, 0
    for f in sorted(lecon_de, key=lambda f: ordre[f]):
        a = audios.get(f)
        if not a:
            non_declares += 1          # prévu mais pas encore généré
            continue
        v = version(f)
        if not v:
            absents += 1
            continue
        i = items[f]
        cle = lecon_de[f] + '|' + i['ref']
        if cle not in cartes:
            ecrit, sens, nature = description(i)
            cartes[cle] = {'lecon': lecon_de[f], 'ref': i['ref'], 'ecrit': ecrit, 'sens': sens,
                           'nature': nature, 'audios': []}
        r = a_refaire.get(a['audio_code'])
        etat = 'valide' if a['validated'] == 'true' else (
            'a_refaire' if r and r.get('version') == v else '')
        cartes[cle]['audios'].append({
            'code': a['audio_code'], 'fichier': f, 'version': v, 'voix': i['voix'],
            'nom_voix': nom_voix(voix.get(i['voix'], {'voice_code': i['voix']})),
            'debit': i['debit'], 'debit_fr': DEBITS.get(i['debit'], i['debit']), 'etat': etat,
            'raison': r.get('reason', '') if etat == 'a_refaire' else ''})
    for c in cartes.values():
        c['audios'].sort(key=lambda x: (x['voix'], ORDRE_DEBITS.get(x['debit'], 9)))

    titres = {l['lesson_code']: f"{l['lesson_code'][-3:]} · {l['family_fr']}" for l in lecons}
    titres['TONS'] = 'Page « Les 6 tons »'
    donnees = {'genere_le': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
               'lecons': [{'code': c, 'titre': t} for c, t in titres.items()],
               'cartes': list(cartes.values())}
    with open(os.path.join(ICI, 'validation_audios.html'), encoding='utf-8') as f:
        page = f.read()
    page = page.replace('/*DONNEES*/null', json.dumps(donnees, ensure_ascii=False))
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, 'validation_audios.html')
    with open(chemin, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)

    tous = [x for c in cartes.values() for x in c['audios']]
    print(f"{len(tous)} audios à écouter ou déjà jugés, en {len(cartes)} cartes :")
    print(f"  validés : {sum(x['etat'] == 'valide' for x in tous)} ; "
          f"à refaire : {sum(x['etat'] == 'a_refaire' for x in tous)} ; "
          f"à écouter : {sum(x['etat'] == '' for x in tous)}")
    hors_plan = len([f for f in audios if f not in lecon_de])
    print(f"  non proposés (abandonnés, hors du plan actuel) : {hors_plan}")
    if non_declares or absents:
        print(f"  prévus mais pas encore générés : {non_declares} ; déclarés mais fichier absent : {absents}")
    print('Page :', chemin)
    print('Elle lit les audios dans 04_DONNEES\\audio : ne pas la déplacer.')


# ---------------------------------------------------------------------------
# 2. Application d'un export
# ---------------------------------------------------------------------------
def dernier_export():
    dossier = os.path.join(os.path.expanduser('~'), 'Downloads')
    fichiers = glob.glob(os.path.join(dossier, 'validations_audios_*.csv'))
    if not fichiers:
        sys.exit(f"Aucun fichier validations_audios_*.csv dans {dossier}.\n"
                 "Indiquez son chemin : valider_audios.py . --appliquer C:\\chemin\\du\\fichier.csv")
    return max(fichiers, key=os.path.getmtime)


def appliquer():
    i = sys.argv.index('--appliquer')
    source = sys.argv[i + 1] if len(sys.argv) > i + 1 and not sys.argv[i + 1].startswith('--') else dernier_export()
    if source == RACINE and len(ARGS) < 2:
        source = dernier_export()
    print('Fichier lu :', source)
    decisions = lire(source)
    if not decisions or 'decision' not in decisions[0]:
        sys.exit("Ce fichier ne ressemble pas à un export de la page de validation.")
    copie = os.path.join(QUALITE, 'validations', os.path.basename(source))
    os.makedirs(os.path.dirname(copie), exist_ok=True)
    if os.path.abspath(source) != os.path.abspath(copie):
        shutil.copyfile(source, copie)

    lignes = lire(CHEMIN_AUDIOS)
    par_code = {l['audio_code']: l for l in lignes}
    a_refaire = {x['audio_code']: x for x in lire(CHEMIN_A_REFAIRE)}
    bons = refus = changes = inconnus = 0
    for d in decisions:
        l = par_code.get(d['audio_code'])
        if not l:
            inconnus += 1
            continue
        if version(l['file']) != d['version']:
            changes += 1        # audio refait depuis l'écoute : décision ignorée
            continue
        if d['decision'] == 'ok':
            l['validated'] = 'true'
            a_refaire.pop(d['audio_code'], None)
            bons += 1
        elif d['decision'] == 'ko':
            l['validated'] = 'false'
            a_refaire[d['audio_code']] = {'audio_code': d['audio_code'], 'file': l['file'],
                                          'version': d['version'], 'reason': d.get('reason', ''),
                                          'date': d.get('date', '')}
            refus += 1
    ecrire(CHEMIN_AUDIOS, gen.COLONNES_AUDIOS, lignes)
    ecrire(CHEMIN_A_REFAIRE, COLONNES_A_REFAIRE, sorted(a_refaire.values(), key=lambda x: x['audio_code']))
    total = sum(l['validated'] == 'true' for l in lignes)
    print(f"Appliqué : {bons} bon(s), {refus} à refaire.")
    if changes:
        print(f"  {changes} décision(s) ignorée(s) : l'audio a été refait depuis l'écoute.")
    if inconnus:
        print(f"  {inconnus} audio(s) inconnu(s) de audios.csv, ignoré(s).")
    print(f"audios.csv : {total} audio(s) validé(s) sur {len(lignes)}.")
    print(f"À refaire : {len(a_refaire)} (liste : {CHEMIN_A_REFAIRE}) ; copie de l'export : {copie}")


if __name__ == '__main__':
    if '--appliquer' in sys.argv:
        appliquer()
    else:
        fabriquer_page()
