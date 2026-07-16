"""
ETAPE 2 — Analyse critique et croisement méthodologique
============================================================
Ce n'est pas juste "afficher les chiffres" : le vrai travail de recherche
consiste à identifier ce que les deux sources permettent — ou ne permettent
pas — de conclure ensemble, étant donné qu'elles ne couvrent pas le même
périmètre d'entreprises.

C'est exactement la compétence "esprit critique et réflexivité sur les
biais, limites [...] de l'IA" et "rigueur méthodologique" demandée dans
l'offre visée — appliquée ici aux données elles-mêmes, pas seulement à l'IA.
"""

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

df_secteur = pd.read_csv(DATA_DIR / "adoption_par_secteur.csv")
df_taille = pd.read_csv(DATA_DIR / "adoption_par_taille.csv")
df_evolution = pd.read_csv(DATA_DIR / "adoption_evolution.csv")

# ---------------------------------------------------------------------------
# 1. Secteurs présents dans les DEUX sources (comparaison directe possible)
# ---------------------------------------------------------------------------
secteurs_fn = set(df_secteur[df_secteur["source"] == "France Num 2025"]["secteur"])
secteurs_insee = set(df_secteur[df_secteur["source"] == "Insee 2024"]["secteur"])
secteurs_communs = secteurs_fn & secteurs_insee

comparaison_secteurs_communs = []
for secteur in secteurs_communs:
    taux_fn = df_secteur[(df_secteur.source == "France Num 2025") & (df_secteur.secteur == secteur)]["taux_adoption_ia_pct"].iloc[0]
    taux_insee = df_secteur[(df_secteur.source == "Insee 2024") & (df_secteur.secteur == secteur)]["taux_adoption_ia_pct"].iloc[0]
    comparaison_secteurs_communs.append({
        "secteur": secteur,
        "taux_france_num_pct": float(taux_fn),
        "taux_insee_pct": float(taux_insee),
        "ecart_points": round(float(taux_fn) - float(taux_insee), 1),
    })

# ---------------------------------------------------------------------------
# 2. Croissance relative de l'adoption (les deux sources s'accordent-elles
#    sur la DYNAMIQUE, même si le NIVEAU diffère à cause du périmètre ?)
# ---------------------------------------------------------------------------
croissance = []
for source in df_evolution["source"].unique():
    sous_df = df_evolution[df_evolution.source == source].sort_values("annee")
    taux_debut = sous_df.iloc[0]["taux_pct"]
    taux_fin = sous_df.iloc[-1]["taux_pct"]
    croissance.append({
        "source": source,
        "annee_debut": int(sous_df.iloc[0]["annee"]),
        "annee_fin": int(sous_df.iloc[-1]["annee"]),
        "taux_debut_pct": float(taux_debut),
        "taux_fin_pct": float(taux_fin),
        "multiplicateur": round(float(taux_fin) / float(taux_debut), 2),
    })

# ---------------------------------------------------------------------------
# 3. Écart de maturité par taille d'entreprise (Insee) — lecture
# ---------------------------------------------------------------------------
ecart_taille = df_taille["taux_adoption_ia_pct"].max() - df_taille["taux_adoption_ia_pct"].min()

# ---------------------------------------------------------------------------
# 4. Synthèse pour le dashboard + note méthodologique explicite
# ---------------------------------------------------------------------------
indicateurs = {
    "sources": {
        "france_num": {
            "nom": "Baromètre France Num 2025 (DGE/CREDOC)",
            "perimetre": "TPE/PME françaises, 0-249 salariés",
            "echantillon": 11021,
        },
        "insee": {
            "nom": "Enquête TIC Entreprises 2024 (Insee)",
            "perimetre": "Entreprises françaises 10+ salariés",
        },
    },
    "evolution_globale": croissance,
    "adoption_par_secteur": df_secteur.to_dict(orient="records"),
    "adoption_par_taille": df_taille.to_dict(orient="records"),
    "secteurs_comparables_deux_sources": comparaison_secteurs_communs,
    "ecart_maturite_taille_points": round(float(ecart_taille), 1),
    "note_methodologique": (
        "France Num (0-249 salariés, taux 2025 plus élevés) et Insee "
        "(10+ salariés uniquement, taux 2024 plus bas) ne couvrent pas le "
        "même périmètre d'entreprises et portent sur des années différentes "
        "(2025 vs 2024) : les niveaux ne sont donc pas directement comparables. "
        "En revanche, les deux sources s'accordent sur la DYNAMIQUE : "
        "doublement de l'adoption de l'IA en un an, et sur-représentation "
        "du secteur Numérique / Information-Communication en tête des usages."
    ),
}

out_path = DATA_DIR / "indicateurs.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(indicateurs, f, ensure_ascii=False, indent=2)

print(f"[OK] Analyse croisée terminée -> {out_path}\n")
print("Secteurs présents dans les deux sources (comparaison directe) :")
for c in comparaison_secteurs_communs:
    print(f"  - {c['secteur']}: France Num {c['taux_france_num_pct']}% vs Insee {c['taux_insee_pct']}% (écart {c['ecart_points']:+.1f} pts)")
print("\nDynamique d'adoption (les deux sources doublent en 1 an) :")
for c in croissance:
    print(f"  - {c['source']}: {c['taux_debut_pct']}% ({c['annee_debut']}) -> {c['taux_fin_pct']}% ({c['annee_fin']}) — x{c['multiplicateur']}")
print(f"\nÉcart de maturité IA entre PME (<50 sal.) et grandes entreprises (250+): {ecart_taille:.1f} points")
