"""Test de reconnaissance vocale (PhoWhisper) - étape 2 : transcrire et comparer.

Passe chaque enregistrement dans PhoWhisper (exécuté sur ce PC, hors ligne
après le premier téléchargement du modèle) et compare le texte reconnu :
  - prise JUSTE : réussite si le mot visé est reconnu ;
  - prise FAUX  : réussite si le mot visé n'est PAS reconnu (la machine
    refuse le ton faux). Si elle reconnaît quand même le mot visé, elle est
    « indulgente » : c'est le défaut que l'on cherche à mesurer.

Lancement (depuis C:\\VIET_PROJECT) :
  .\\.venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\test_asr\\transcrire.py
Option : ajouter  --modele vinai/PhoWhisper-base  (plus rapide, moins précis)
"""
import argparse
import csv
import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import soundfile as sf

ICI = Path(__file__).resolve().parent
DOSSIER = ICI / "enregistrements"


def normaliser(texte: str) -> list[str]:
    t = unicodedata.normalize("NFC", texte).lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return t.split()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--modele", default="vinai/PhoWhisper-small")
    args = p.parse_args()

    print(f"Chargement de {args.modele} (le premier lancement télécharge le modèle)...")
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", model=args.modele, device="cpu")

    with open(ICI / "liste_test.csv", encoding="utf-8-sig") as f:
        items = list(csv.DictReader(f, delimiter=";"))

    lignes = []
    for it in items:
        vise = unicodedata.normalize("NFC", it["mot_vise"]).lower()
        faux = unicodedata.normalize("NFC", it["mot_faux"]).lower()
        for prise in ("juste", "faux"):
            chemin = DOSSIER / f"{it['item']}_{prise}.wav"
            if not chemin.exists():
                print(f"  manquant : {chemin.name}")
                continue
            audio, sr = sf.read(chemin, dtype="float32")
            t0 = time.time()
            try:
                out = asr({"raw": audio, "sampling_rate": sr},
                          generate_kwargs={"language": "vietnamese", "task": "transcribe"})
            except Exception:
                out = asr({"raw": audio, "sampling_rate": sr})
            texte = out["text"].strip()
            mots = normaliser(texte)
            if vise in mots:
                reconnu = "mot_vise"
            elif faux in mots:
                reconnu = "mot_faux"
            else:
                reconnu = "autre"
            ok = (reconnu == "mot_vise") if prise == "juste" else (reconnu != "mot_vise")
            lignes.append({
                "item": it["item"], "prise": prise, "mot_vise": it["mot_vise"],
                "mot_faux": it["mot_faux"], "texte_reconnu": texte,
                "reconnu_comme": reconnu, "reussite": "oui" if ok else "non",
                "secondes": f"{time.time() - t0:.1f}",
            })
            print(f"  {it['item']} {prise:5}  attendu « {it['mot_vise']} »"
                  f"{'' if prise == 'juste' else ' refusé'}  ->  « {texte} »  "
                  f"[{'OK' if ok else 'ÉCHEC'}]")

    fichier = ICI / f"resultats_{datetime.now():%Y%m%d_%H%M}.csv"
    with open(fichier, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(lignes)

    def bilan(prise: str) -> str:
        sel = [l for l in lignes if l["prise"] == prise]
        n = sum(l["reussite"] == "oui" for l in sel)
        return f"{n}/{len(sel)}"

    indulgent = sum(1 for l in lignes if l["prise"] == "faux" and l["reconnu_comme"] == "mot_vise")
    print("\n=== BILAN ===")
    print(f"Prises justes reconnues          : {bilan('juste')}")
    print(f"Prises fausses refusées          : {bilan('faux')}")
    print(f"  dont acceptées à tort (indulgent) : {indulgent}")
    print(f"Détail : {fichier}")


if __name__ == "__main__":
    main()
