"""
ETAPE 3 — Garantir la qualité, la robustesse méthodologique et la
             reproductibilité des travaux
=====================================================================
C'est un point de la mission 2 à part entière, souvent négligé dans les
démos techniques — donc volontairement isolé ici plutôt que noyé dans le
script de collecte.

Trois familles de contrôles :
1. Qualité des données (validité, doublons, cohérence interne)
2. Robustesse méthodologique (représentativité de l'échantillon vs quotas déclarés)
3. Reproductibilité (traçabilité de la version du questionnaire et des seeds)
"""

import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
sys.path.insert(0, str(DATA_DIR))

from questionnaire import PLAN_ECHANTILLONNAGE  # noqa: E402

df = pd.read_csv(DATA_DIR / "barometre_2_vagues.csv")


def controle_qualite_donnees(df):
    """Validité et cohérence — rejette ce qui ne respecte pas les bornes
    déclarées du questionnaire (Q4 : échelle 1-5 ; Q7 : pourcentage >= 0)."""
    n_avant = len(df)
    problemes = {}

    hors_bornes_maturite = ~df["score_maturite_ia"].between(1, 5)
    problemes["maturite_hors_bornes"] = int(hors_bornes_maturite.sum())

    budget_negatif = df["budget_ia_pct_it"] < 0
    problemes["budget_negatif"] = int(budget_negatif.sum())

    doublons = df.duplicated(subset=["id_panel", "vague"])
    problemes["doublons_panel_vague"] = int(doublons.sum())

    # Cohérence interne : usage_actuel=True doit avoir au moins un type d'IA renseigné
    df_types = df.copy()
    df_types["n_types_ia"] = df_types["types_ia"].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)
    incoherent = df_types["usage_actuel"] & (df_types["n_types_ia"] == 0)
    problemes["incoherence_usage_sans_type_ia"] = int(incoherent.sum())

    df_propre = df[~hors_bornes_maturite & ~budget_negatif & ~doublons]
    n_apres = len(df_propre)

    return df_propre, {
        "n_lignes_avant": n_avant,
        "n_lignes_rejetees": n_avant - n_apres,
        "n_lignes_conservees": n_apres,
        "detail_problemes": problemes,
    }


def controle_representativite(df, quotas_declares):
    """Vérifie que l'échantillon RÉEL (après nettoyage) respecte encore les
    quotas déclarés dans le plan d'échantillonnage — sinon il faut pondérer
    ou documenter l'écart, pas l'ignorer."""
    vague1 = df[df.vague == 1]
    repartition_reelle = (vague1["taille_entreprise"].value_counts(normalize=True) * 100).round(1).to_dict()
    repartition_cible = {k: round(v * 100, 1) for k, v in quotas_declares.items()}

    ecarts = {
        taille: round(repartition_reelle.get(taille, 0) - repartition_cible.get(taille, 0), 1)
        for taille in quotas_declares
    }
    return {
        "repartition_cible_pct": repartition_cible,
        "repartition_reelle_pct": repartition_reelle,
        "ecarts_points": ecarts,
        "conforme": all(abs(e) <= 5 for e in ecarts.values()),
    }


def rapport_reproductibilite():
    """Documente ce qui garantit qu'une future vague pourra être comparée
    à celle-ci — pas un contrôle sur les données, mais sur le PROCESSUS."""
    return {
        "version_questionnaire": "v1.0 — gelé avant collecte (data/questionnaire.py)",
        "seed_simulation": 42,
        "regle_de_non_modification": (
            "Aucune reformulation de question autorisée en cours de collecte. "
            "Toute évolution du questionnaire donne lieu à une nouvelle version "
            "documentée (v1.1, v2.0) avec table de correspondance, comme le fait "
            "France Num d'une année sur l'autre."
        ),
        "code_source_versionne": "Pipeline scripté (pas de traitement manuel Excel) — rejouable à l'identique.",
    }


if __name__ == "__main__":
    df_propre, rapport_qualite = controle_qualite_donnees(df)
    rapport_repr = controle_representativite(df_propre, PLAN_ECHANTILLONNAGE["quotas"])
    rapport_repro = rapport_reproductibilite()

    rapport_complet = {
        "controle_qualite": rapport_qualite,
        "representativite": rapport_repr,
        "reproductibilite": rapport_repro,
    }

    with open(DATA_DIR / "rapport_qualite_methodologique.json", "w", encoding="utf-8") as f:
        json.dump(rapport_complet, f, ensure_ascii=False, indent=2)

    df_propre.to_csv(DATA_DIR / "barometre_valide.csv", index=False)

    print("[OK] Contrôle qualité des données :")
    print(json.dumps(rapport_qualite, ensure_ascii=False, indent=2))
    print("\n[OK] Contrôle de représentativité (échantillon vs quotas déclarés) :")
    print(json.dumps(rapport_repr, ensure_ascii=False, indent=2))
    print("\n[OK] Rapport de reproductibilité :")
    print(json.dumps(rapport_repro, ensure_ascii=False, indent=2))
