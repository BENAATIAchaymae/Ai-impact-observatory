"""
Pipeline complet — Baromètre AI Impact Observatory (données primaires)
==========================================================================
Exécute les 4 étapes dans l'ordre, en miroir exact des 4 points de la
mission 2 de l'offre visée :

  1. Concevoir et opérer le baromètre         -> 01_conception_et_deploiement.py
  2. Études de cas qualitatives longitudinales -> 02_etudes_cas_qualitatives.py
  3. Qualité, robustesse, reproductibilité     -> 03_controle_qualite.py
  4. Production des livrables                  -> 04_generer_livrables.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "pipeline/01_conception_et_deploiement.py",
    "pipeline/02_etudes_cas_qualitatives.py",
    "pipeline/03_controle_qualite.py",
    "pipeline/04_generer_livrables.py",
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
print("  - flash_note.md   (synthèse quanti + quali)")
print("  - dashboard.html  (dashboard interactif Plotly)")
