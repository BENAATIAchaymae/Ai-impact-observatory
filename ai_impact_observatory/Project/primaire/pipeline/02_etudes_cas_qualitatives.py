"""
ETAPE 2 — Études de cas qualitatives longitudinales
========================================================
Mission : "Mener des études de cas qualitatives longitudinales en entreprise
(trajectoires, obstacles, solutions déployées)" + "Contribuer à la conception
méthodologique des dispositifs d'enquête et à leur automatisation par l'IA."
"""

import json

import random
from pathlib import Path

import pandas as pd

random.seed(11)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

df = pd.read_csv(DATA_DIR / "barometre_2_vagues.csv")

# Panel qualitatif : entreprises ayant répondu aux 2 vagues ET accepté le suivi
ids_v1 = set(df[df.vague == 1]["id_panel"])
ids_v2 = set(df[df.vague == 2]["id_panel"])
ids_communs = ids_v1 & ids_v2
accepte_v1 = df[(df.vague == 1) & (df.id_panel.isin(ids_communs)) & (df.accepte_suivi_qualitatif)]

PANEL_QUALITATIF = accepte_v1["id_panel"].tolist()[:12]  # 12 études de cas, taille réaliste pour du qualitatif

# ---------------------------------------------------------------------------
# Grille de codage thématique (définie a priori, avant les "entretiens" —
# bonne pratique méthodologique : coder sur une grille théorique déclarée,
# quitte à l'enrichir en cours d'analyse, plutôt que de coder à l'aveugle)
# ---------------------------------------------------------------------------
GRILLE_THEMATIQUE = {
    "Montée en compétences": ["formation", "recrutement", "compétence", "apprentissage"],
    "Gouvernance des données": ["gouvernance", "qualité des données", "conformité", "RGPD"],
    "Résistance au changement": ["résistance", "réticence", "culture", "adhésion"],
    "Preuve de valeur (ROI)": ["retour sur investissement", "roi", "rentabilité", "pilote"],
    "Dépendance fournisseur": ["fournisseur", "prestataire", "dépendance", "vendor lock"],
}

# Verbatims synthétiques réalistes (2 temps par entreprise : trajectoire)
VERBATIMS_T0 = [
    "On a lancé un pilote mais on manque cruellement de compétences en interne pour le généraliser.",
    "La direction hésite à cause du retour sur investissement qui reste difficile à prouver sur ce type de projet.",
    "Le vrai frein c'est la gouvernance des données, on n'a pas encore la qualité nécessaire pour industrialiser.",
    "Il y a une vraie résistance culturelle des équipes, qui craignent pour leur emploi.",
    "On dépend beaucoup d'un seul prestataire, ce qui nous inquiète pour la suite.",
]
VERBATIMS_T1 = [
    "Depuis la formation qu'on a mise en place, les équipes montent en compétence rapidement.",
    "On a enfin des chiffres de rentabilité qui commencent à convaincre le comité de direction.",
    "La gouvernance des données s'est améliorée, on peut enfin passer certains projets en production.",
    "La résistance s'est atténuée depuis qu'on a impliqué les équipes dès la conception du projet.",
    "On a diversifié nos prestataires pour limiter la dépendance, ça a rassuré la direction.",
]


def coder_verbatim(texte):
    """Codage automatique par correspondance de mots-clés — transparent et
    vérifiable, contrairement à un LLM en boîte noire. En production, cette
    fonction serait remplacée par un modèle NLP fine-tuné, avec le même
    principe de sortie (thème + citation source pour audit)."""
    texte_low = texte.lower()
    themes_detectes = []
    for theme, mots_cles in GRILLE_THEMATIQUE.items():
        if any(mot in texte_low for mot in mots_cles):
            themes_detectes.append(theme)
    return themes_detectes or ["Non classé"]


if __name__ == "__main__":
    etudes_de_cas = []
    for i, id_panel in enumerate(PANEL_QUALITATIF):
        verbatim_t0 = VERBATIMS_T0[i % len(VERBATIMS_T0)]
        verbatim_t1 = VERBATIMS_T1[i % len(VERBATIMS_T1)]
        etudes_de_cas.append({
            "id_panel": id_panel,
            "verbatim_t0": verbatim_t0,
            "themes_t0": coder_verbatim(verbatim_t0),
            "verbatim_t1_6mois": verbatim_t1,
            "themes_t1": coder_verbatim(verbatim_t1),
        })

    df_qualitatif = pd.DataFrame(etudes_de_cas)
    df_qualitatif.to_json(DATA_DIR / "etudes_cas_qualitatives.json", orient="records", force_ascii=False, indent=2)

    # Fréquence des thèmes à T0 vs T1 : la trajectoire "obstacle -> solution"
    from collections import Counter
    themes_t0 = Counter(t for row in etudes_de_cas for t in row["themes_t0"])
    themes_t1 = Counter(t for row in etudes_de_cas for t in row["themes_t1"])

    synthese = {
        "n_etudes_de_cas": len(etudes_de_cas),
        "grille_thematique": list(GRILLE_THEMATIQUE.keys()),
        "frequence_themes_t0_obstacles": dict(themes_t0),
        "frequence_themes_t1_solutions": dict(themes_t1),
    }
    with open(DATA_DIR / "synthese_qualitative.json", "w", encoding="utf-8") as f:
        json.dump(synthese, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(etudes_de_cas)} études de cas qualitatives longitudinales codées")
    print(f"\nThèmes dominants à T0 (obstacles initiaux) : {dict(themes_t0)}")
    print(f"Thèmes dominants à T1, +6 mois (dynamique de résolution) : {dict(themes_t1)}")
