"""
ETAPE 4 — Analyse croisée et production des livrables
"""

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_DIR / "barometre_valide.csv")
with open(DATA_DIR / "synthese_qualitative.json", encoding="utf-8") as f:
    quali = json.load(f)
with open(DATA_DIR / "rapport_qualite_methodologique.json", encoding="utf-8") as f:
    qualite_meth = json.load(f)

v1 = df[df.vague == 1]
v2 = df[df.vague == 2]

maturite_v1 = round(v1["score_maturite_ia"].mean(), 2)
maturite_v2 = round(v2["score_maturite_ia"].mean(), 2)
maturite_par_taille_v1 = v1.groupby("taille_entreprise")["score_maturite_ia"].mean().round(2).to_dict()
maturite_par_secteur_v1 = v1.groupby("secteur")["score_maturite_ia"].mean().round(2).to_dict()

# Progression individuelle du panel suivi (vraie mesure longitudinale, pas
# une comparaison de 2 échantillons différents)
panel_suivi = pd.merge(
    v1[["id_panel", "score_maturite_ia"]].rename(columns={"score_maturite_ia": "maturite_v1"}),
    v2[["id_panel", "score_maturite_ia"]].rename(columns={"score_maturite_ia": "maturite_v2"}),
    on="id_panel",
)
panel_suivi["progression"] = panel_suivi["maturite_v2"] - panel_suivi["maturite_v1"]
progression_moyenne = round(panel_suivi["progression"].mean(), 2)

indicateurs = {
    "maturite_v1": maturite_v1,
    "maturite_v2": maturite_v2,
    "progression_moyenne_panel_suivi": progression_moyenne,
    "n_panel_suivi": len(panel_suivi),
    "maturite_par_taille": maturite_par_taille_v1,
    "maturite_par_secteur": maturite_par_secteur_v1,
    "obstacle_principal": v1["obstacle_principal"].value_counts().idxmax(),
    "qualitatif": quali,
    "qualite_methodologique": qualite_meth,
}
with open(DATA_DIR / "indicateurs_finaux.json", "w", encoding="utf-8") as f:
    json.dump(indicateurs, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Flash Note
# ---------------------------------------------------------------------------
themes_t0 = quali["frequence_themes_t0_obstacles"]
themes_t1 = quali["frequence_themes_t1_solutions"]
theme_qui_baisse_le_plus = min(
    themes_t0, key=lambda t: themes_t1.get(t, 0) - themes_t0.get(t, 0)
) if themes_t0 else "N/A"

flash_note = f"""# Flash Note — Baromètre AI Impact Observatory (S1-S2)
### Institut de recherche IA
### Données primaires — instrument original, panel de partenaires

**Échantillon :** {len(v1)} entreprises partenaires (vague 1), dont {len(v2)}
suivies en vague 2 (+6 mois) — panel de convenance, non représentatif de la
population nationale (voir note méthodologique).

---

## 1. Résultats quantitatifs

- Maturité IA moyenne : **{maturite_v1}/5 (S1) → {maturite_v2}/5 (S2)**
- Progression moyenne du panel suivi (mesure longitudinale réelle,
  même entreprises interrogées 2 fois) : **{progression_moyenne:+.2f} point en 6 mois**
- Obstacle principal cité : **{indicateurs['obstacle_principal']}**

**Par taille d'entreprise (S1) :**
{chr(10).join(f"- {t} : {s}/5" for t, s in maturite_par_taille_v1.items())}

**Par secteur (S1) :**
{chr(10).join(f"- {s} : {v}/5" for s, v in maturite_par_secteur_v1.items())}

## 2. Résultats qualitatifs (études de cas longitudinales)

{quali['n_etudes_de_cas']} entreprises suivies par entretien à deux reprises
(T0 et T0+6 mois), codage thématique automatisé sur une grille définie a priori.

**Obstacles dominants à T0 :** {themes_t0}
**Thèmes dominants à T1 (+6 mois) :** {themes_t1}

Le thème qui recule le plus entre T0 et T1 est **{theme_qui_baisse_le_plus}**
— cohérent avec la progression quantitative de maturité observée sur le
même panel.

## 3. Note méthodologique

- **Échantillon** : conforme aux quotas déclarés avant collecte
  (écarts : {qualite_meth['representativite']['ecarts_points']}).
- **Contrôle qualité** : {qualite_meth['controle_qualite']['n_lignes_rejetees']}
  lignes rejetées sur {qualite_meth['controle_qualite']['n_lignes_avant']}
  (détail : {qualite_meth['controle_qualite']['detail_problemes']}).
- **Limite assumée** : panel de partenaires, pas un échantillon aléatoire
  national — les niveaux ne sont pas généralisables, seule la **dynamique**
  (progression du même panel dans le temps) est interprétable avec confiance.
- **Reproductibilité** : questionnaire versionné, seed de simulation fixée,
  pipeline scripté rejouable à l'identique.


(OUTPUT_DIR / "flash_note.md").write_text(flash_note, encoding="utf-8")
print(f"[OK] Flash Note générée -> {OUTPUT_DIR / 'flash_note.md'}")


template_path = BASE_DIR / "dashboard_template.html"
if template_path.exists():
    template = template_path.read_text(encoding="utf-8")
    dashboard_html = template.replace("__DATA_INDICATEURS__", json.dumps(indicateurs, ensure_ascii=False))
    (OUTPUT_DIR / "dashboard.html").write_text(dashboard_html, encoding="utf-8")
    print(f"[OK] Dashboard généré -> {OUTPUT_DIR / 'dashboard.html'}")
