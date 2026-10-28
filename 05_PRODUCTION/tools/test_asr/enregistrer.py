"""Test de reconnaissance vocale (PhoWhisper) - étape 1 : enregistrer.

Pour chaque ligne de liste_test.csv, enregistre deux fichiers WAV
(16 kHz, mono) dans le dossier enregistrements/ :
  NN_juste.wav : le mot visé, prononcé avec son ton correct ;
  NN_faux.wav  : le même mot, prononcé volontairement avec le ton faux
                 (ce qui donne le « mot faux » de la liste).
Rien n'est envoyé sur Internet.

Lancement (depuis C:\\VIET_PROJECT) :
  .\\.venv-asr\\Scripts\\python.exe 05_PRODUCTION\\tools\\test_asr\\enregistrer.py
"""
import csv
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

SR = 16000          # fréquence d'échantillonnage attendue par Whisper
DUREE = 2.5         # secondes enregistrées par prise
ICI = Path(__file__).resolve().parent
SORTIE = ICI / "enregistrements"

NOMS_TONS = {
    "ngang": "ngang (plat)", "sac": "sắc (montant)", "huyen": "huyền (descendant)",
    "hoi": "hỏi (descend puis remonte)", "nga": "ngã (cassé, montant)",
    "nang": "nặng (bas, court, arrêt)",
}


def enregistrer(chemin: Path, consigne: str) -> None:
    while True:
        print("\n" + consigne)
        input("  Appuyez sur Entrée, puis parlez quand « PARLEZ » s'affiche...")
        print("  3...", end="", flush=True); time.sleep(0.6)
        print(" 2...", end="", flush=True); time.sleep(0.6)
        print(" 1...", end="", flush=True); time.sleep(0.6)
        print("  >>> PARLEZ <<<", flush=True)
        audio = sd.rec(int(DUREE * SR), samplerate=SR, channels=1, dtype="float32")
        sd.wait()
        niveau = float(np.max(np.abs(audio)))
        if niveau < 0.02:
            print("  ! Son très faible : le micro a-t-il bien capté votre voix ?")
        print("  Réécoute...")
        sd.play(audio, SR); sd.wait()
        rep = input("  Entrée = garder ; r = recommencer : ").strip().lower()
        if rep != "r":
            sf.write(chemin, audio, SR, subtype="PCM_16")
            print(f"  Enregistré : {chemin.name}")
            return


def main() -> None:
    SORTIE.mkdir(exist_ok=True)
    with open(ICI / "liste_test.csv", encoding="utf-8-sig") as f:
        items = list(csv.DictReader(f, delimiter=";"))
    print(f"{len(items)} mots, 2 prises chacun. Micro utilisé : {sd.query_devices(kind='input')['name']}")
    print("Si un fichier existe déjà, il est sauté (supprimez-le pour le refaire).")
    for it in items:
        n = it["item"]
        juste = SORTIE / f"{n}_juste.wav"
        faux = SORTIE / f"{n}_faux.wav"
        if not juste.exists():
            enregistrer(juste, f"[{n}] JUSTE : dites « {it['mot_vise']} » "
                               f"avec le ton {NOMS_TONS[it['ton_vise']]}")
        if not faux.exists():
            enregistrer(faux, f"[{n}] FAUX : au lieu de « {it['mot_vise']} », dites "
                              f"« {it['mot_faux']} » (ton {NOMS_TONS[it['ton_faux']]})")
    print("\nTerminé. Lancez ensuite transcrire.py.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu. Relancez : les prises déjà gardées sont conservées.")
        sys.exit(1)
