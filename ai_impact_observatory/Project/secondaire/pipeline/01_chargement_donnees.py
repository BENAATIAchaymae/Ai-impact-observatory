"""
ETAPE 1 — Chargement et structuration (Pandas)
==================================================
Transforme les agrégats officiels (dict Python en dur, cf. data/sources_reelles.py)
en DataFrames Pandas propres, avec la source et le périmètre attachés à chaque
ligne — pour ne jamais perdre la traçabilité methodologique pendant l'analyse.
"""

import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "data"))
from sources_reelles import DONNEES_FRANCE_NUM_2025, DONNEES_INSEE_2024  # noqa: E402

DATA_DIR = BASE_DIR / "data"


def construire_df_secteur():
    lignes = []
    for secteur, (taux, evol) in DONNEES_FRANCE_NUM_2025["adoption_ia_par_secteur_2025"].items():
        lignes.append({
            "source": "France Num 2025",
            "perimetre": "TPE/PME 0-249 sal.",
            "secteur": secteur,
            "taux_adoption_ia_pct": taux,
            "evolution": evol,
        })
    for secteur, (taux, evol) in DONNEES_INSEE_2024["adoption_ia_par_secteur_2024"].items():
        lignes.append({
            "source": "Insee 2024",
            "perimetre": "Entreprises 10+ sal.",
            "secteur": secteur,
            "taux_adoption_ia_pct": taux,
            "evolution": evol,
        })
    return pd.DataFrame(lignes)


def construire_df_taille():
    lignes = [
        {"source": "Insee 2024", "taille": taille, "taux_adoption_ia_pct": taux}
        for taille, taux in DONNEES_INSEE_2024["adoption_ia_par_taille_2024"].items()
    ]
    return pd.DataFrame(lignes)


def construire_df_evolution():
    lignes = []
    for annee, taux in DONNEES_FRANCE_NUM_2025["adoption_ia_globale"].items():
        lignes.append({"source": "France Num", "perimetre": "TPE/PME 0-249 sal.", "annee": annee, "taux_pct": taux})
    for annee, taux in DONNEES_INSEE_2024["adoption_ia_globale"].items():
        lignes.append({"source": "Insee", "perimetre": "Entreprises 10+ sal.", "annee": annee, "taux_pct": taux})
    return pd.DataFrame(lignes).sort_values(["source", "annee"])


if __name__ == "__main__":
    df_secteur = construire_df_secteur()
    df_taille = construire_df_taille()
    df_evolution = construire_df_evolution()

    df_secteur.to_csv(DATA_DIR / "adoption_par_secteur.csv", index=False)
    df_taille.to_csv(DATA_DIR / "adoption_par_taille.csv", index=False)
    df_evolution.to_csv(DATA_DIR / "adoption_evolution.csv", index=False)

    print("[OK] 3 DataFrames construits à partir des agrégats officiels :")
    print(f"\n--- Adoption IA par secteur (2 sources croisées) ---\n{df_secteur.to_string(index=False)}")
    print(f"\n--- Adoption IA par taille (Insee uniquement) ---\n{df_taille.to_string(index=False)}")
    print(f"\n--- Évolution 2023-2025 (2 sources) ---\n{df_evolution.to_string(index=False)}")
