"""
Pipeline complet — Données primaires (sources réelles)
==========================================================
Exécute les 3 étapes dans l'ordre :
  1. Chargement & structuration Pandas   -> 01_chargement_donnees.py
  2. Analyse critique croisée            -> 02_analyse_croisee.py
  3. Production des livrables            -> 03_generer_livrables.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "pipeline/01_chargement_donnees.py",
    "pipeline/02_analyse_croisee.py",
    "pipeline/03_generer_livrables.py",
]

for script in SCRIPTS:
    print("\n" + "=" * 70)
    print(f"  {script}")
    print("=" * 70)
    result = subprocess.run([sys.executable, str(BASE_DIR / script)])
    if result.returncode != 0:
        print(f"[ERREUR] {script} a échoué.")
        sys.exit(1)

print("\n" + "=" * 70)
print("  PIPELINE TERMINE")
print("=" * 70)
print("Livrables dans output/ :")
print("  - flash_note.md   (synthèse méthodologique)")
print("  - dashboard.html  (dashboard interactif Plotly)")
