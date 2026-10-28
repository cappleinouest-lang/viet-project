# -*- coding: utf-8 -*-
# Build CARTE_DOCUMENTAIRE.md from the YAML headers of all .md files (rules DOC-30 to DOC-35).
# Usage: python build_doc_map.py <project_root>
import sys, os, re, datetime
import yaml

root = sys.argv[1] if len(sys.argv) > 1 else '.'
docs = {}
for d, _, files in os.walk(root):
    if '_ARCHIVES' in d or '.git' in d:
        continue
    for f in files:
        if not f.endswith('.md') or f == 'CARTE_DOCUMENTAIRE.md':
            continue
        p = os.path.join(d, f)
        t = open(p, encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---', t, re.S)
        if not m:
            docs[p] = None
            continue
        h = yaml.safe_load(m.group(1)) or {}
        h['_path'] = os.path.relpath(p, root).replace('\\', '/')
        docs[h.get('id', p)] = h

ids = {k for k, v in docs.items() if v}
def as_list(x):
    if not x: return []
    return x if isinstance(x, list) else [x]
def doc_refs(lst):
    out = []
    for x in as_list(lst):
        for part in str(x).split(','):
            part = part.strip()
            if re.match(r'^[A-Z]+-[A-Z0-9-]+$', part):
                out.append(part)
    return out

anom = []
edges = set()
for k, h in docs.items():
    if h is None:
        anom.append(f'`{k}` : en-tête absent')
        continue
    for req in ['id', 'titre', 'statut', 'version', 'date', 'resume']:
        if req not in h:
            anom.append(f'`{k}` : champ `{req}` absent')
    for o in doc_refs(h.get('sorties')):
        edges.add((k, o))
        if o not in ids:
            anom.append(f'`{k}` → `{o}` : document de sortie inexistant (à créer ?)')
        elif k not in doc_refs(docs[o].get('entrees')):
            anom.append(f'`{k}` → `{o}` : lien non réciproque (`{o}` ne cite pas `{k}` en entrée)')
    for i in doc_refs(h.get('entrees')):
        edges.add((i, k))
        if i not in ids:
            anom.append(f'`{k}` ← `{i}` : document d\'entrée inexistant')
        elif k not in doc_refs(docs[i].get('sorties')):
            anom.append(f'`{i}` → `{k}` : lien non réciproque (`{i}` ne cite pas `{k}` en sortie)')
isolated = [k for k in ids if not any(k in e for e in edges)]

def node(x): return x.replace('-', '_')
lines = ['```mermaid', 'graph LR']
for k in sorted(ids):
    lines.append(f'  {node(k)}["{k}<br/>{docs[k]["titre"]}"]')
for a, b in sorted(edges):
    if a in ids and b in ids:
        lines.append(f'  {node(a)} --> {node(b)}')
lines.append('```')

today = datetime.date.today().isoformat()
out = ['---', 'id: CARTE-DOC', 'titre: Carte documentaire', 'statut: VALIDE', 'version: 1.0', f'date: {today}',
       'resume: >', '  Carte générée automatiquement à partir des en-têtes des documents (DOC-33).',
       '  Ne pas modifier à la main : relancer 05_PRODUCTION/tools/build_doc_map.py.',
       'entrees: []', 'sorties: []', 'sources: []', '---', '',
       '# Carte documentaire', '', f'Générée le {today}. **Ne pas modifier à la main.**', '',
       '## 1. Schéma des liens', ''] + lines + ['', '## 2. Liste des documents', '',
       '| Identifiant | Titre | Statut | Version | Entrées | Sorties | Fichier |', '|---|---|---|---|---|---|---|']
for k in sorted(ids):
    h = docs[k]
    out.append(f"| {k} | {h['titre']} | {h['statut']} | {h['version']} | {', '.join(doc_refs(h.get('entrees'))) or '—'} | {', '.join(doc_refs(h.get('sorties'))) or '—'} | [{h['_path']}]({h['_path']}) |")
out += ['', '## 3. Anomalies', '']
out += [f'- {a}' for a in sorted(set(anom))] or ['Aucune.']
if isolated:
    out += ['', 'Documents sans aucun lien : ' + ', '.join(sorted(isolated))]
open(os.path.join(root, 'CARTE_DOCUMENTAIRE.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(ids), 'documents,', len(set(anom)), 'anomalies')
