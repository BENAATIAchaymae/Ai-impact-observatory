"""
ETAPE 1 — Concevoir et opérer le baromètre
================================================
Mission :
Concevoir et opérer les baromètres annuels ou semestriels auprès
des entreprises partenaires et de leurs écosystèmes.
"""

import random
import sys

from pathlib import Path

import pandas as pd

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "data"))
from questionnaire import PLAN_ECHANTILLONNAGE, QUESTIONNAIRE  # noqa: E402

DATA_DIR = BASE_DIR / "data"

SECTEURS = ["Banque & Assurance", "Industrie", "Retail", "Santé", "Conseil", "Énergie", "Public"]
TYPES_IA = ["IA générative", "Machine learning prédictif", "Automatisation (RPA)", "Vision par ordinateur", "NLP / traitement documentaire"]
FONCTIONS = ["RH", "Marketing & Ventes", "Production / Supply chain", "Finance", "Juridique & Conformité", "R&D"]
OBSTACLES = [
    "Manque de compétences internes", "Budget limité", "Gouvernance des données insuffisante",
    "Résistance au changement", "Incertitude réglementaire (AI Act)", "ROI difficile à démontrer",
]

MATURITE_BASE = {"PME (10-249 sal.)": 2.0, "ETI (250-4999 sal.)": 2.7, "Grand groupe (5000+ sal.)": 3.5}


def tirer_echantillon_par_quotas(n_total, quotas):
    """Applique le plan d'échantillonnage stratifié déclaré dans questionnaire.py
    — les quotas sont fixés AVANT la simulation, pas ajustés après coup."""
    tailles = []
    for taille, part in quotas.items():
        n = round(n_total * part)
        tailles.extend([taille] * n)
    random.shuffle(tailles)
    return tailles[:n_total]


def simuler_repondant(id_panel, taille, vague, maturite_precedente=None):
    secteur = random.choice(SECTEURS)

    if maturite_precedente is None:
        # Première vague : maturité de base + bruit
        maturite = MATURITE_BASE[taille] + random.gauss(0, 0.6)
    else:
        # Deuxième vague (suivi longitudinal) : progression modérée, pas un tirage indépendant
        # -> simule une vraie dynamique de panel plutôt que 2 échantillons non liés
        progression = random.gauss(0.3, 0.25)
        maturite = maturite_precedente + progression

    maturite = round(max(1, min(5, maturite)), 1)
    usage_actuel = maturite >= 2.2  # seuil de "franchissement" vers l'usage en production

    return {
        "id_panel": id_panel,
        "vague": vague,
        "secteur": secteur,
        "taille_entreprise": taille,
        "usage_actuel": usage_actuel,
        "score_maturite_ia": maturite,
        "types_ia": random.sample(TYPES_IA, k=random.randint(1, 2)) if usage_actuel else [],
        "fonction_principale": random.choice(FONCTIONS) if usage_actuel else None,
        "budget_ia_pct_it": round(max(0, random.gauss(2 + maturite * 1.8, 1.5)), 1),
        "obstacle_principal": random.choice(OBSTACLES),
        "accepte_suivi_qualitatif": random.random() < 0.35,
    }


if __name__ == "__main__":
    tailles_echantillon = tirer_echantillon_par_quotas(
        PLAN_ECHANTILLONNAGE["taille_cible"], PLAN_ECHANTILLONNAGE["quotas"]
    )

    # --- Vague 1 (S1) ---
    vague1 = [
        simuler_repondant(f"panel_{i:03d}", taille, vague=1)
        for i, taille in enumerate(tailles_echantillon)
    ]
    df_vague1 = pd.DataFrame(vague1)

    # --- Vague 2 (S2), 6 mois plus tard : suivi longitudinal du MÊME panel ---
    # Attrition réaliste : tout le monde ne répond pas à la vague 2
    taux_reponse_v2 = 0.82
    panel_suivi = df_vague1.sample(frac=taux_reponse_v2, random_state=1)

    vague2 = [
        simuler_repondant(
            row["id_panel"], row["taille_entreprise"], vague=2,
            maturite_precedente=row["score_maturite_ia"]
        )
        for _, row in panel_suivi.iterrows()
    ]
    df_vague2 = pd.DataFrame(vague2)

    df_toutes_vagues = pd.concat([df_vague1, df_vague2], ignore_index=True)

    
    df_toutes_vagues.to_csv(DATA_DIR / "barometre_2_vagues.csv", index=False)

    print(f"[OK] Vague 1 (S1) : {len(df_vague1)} répondants déployés selon quotas :")
    print(df_vague1["taille_entreprise"].value_counts().to_string())
    print(f"\n[OK] Vague 2 (S2) : {len(df_vague2)} répondants suivis "
          f"(taux de réponse au suivi : {taux_reponse_v2:.0%})")
    
    print(f"\n[OK] Fichier consolidé -> {DATA_DIR / 'barometre_2_vagues.csv'}")
    print(f"\nMaturité moyenne V1 : {df_vague1['score_maturite_ia'].mean():.2f} / 5")
    print(f"Maturité moyenne V2 : {df_vague2['score_maturite_ia'].mean():.2f} / 5 (même panel, 6 mois après)")
