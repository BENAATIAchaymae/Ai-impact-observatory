"""
ETAPE 3 — Production des livrables
=====================================
Génère la Flash Note (Markdown) et injecte les indicateurs réels dans le
template du dashboard (Plotly.js, chargé via CDN — le calcul des données
est fait en Python/Pandas, le rendu graphique en Plotly côté navigateur).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "indicateurs.json", encoding="utf-8") as f:
    ind = json.load(f)

fn = ind["evolution_globale"][0] if ind["evolution_globale"][0]["source"] == "France Num" else ind["evolution_globale"][1]
insee = ind["evolution_globale"][1] if ind["evolution_globale"][1]["source"] == "Insee" else ind["evolution_globale"][0]

secteur_top_fn = max(
    [d for d in ind["adoption_par_secteur"] if d["source"] == "France Num 2025"],
    key=lambda d: d["taux_adoption_ia_pct"]
)
secteur_top_insee = max(
    [d for d in ind["adoption_par_secteur"] if d["source"] == "Insee 2024"],
    key=lambda d: d["taux_adoption_ia_pct"]
)

comp = ind["secteurs_comparables_deux_sources"][0] if ind["secteurs_comparables_deux_sources"] else None

flash_note = f"""# Flash Note — AI Impact Observatory
### Institut de recherche IA
### Données primaires — sources officielles croisées

**Sources :**
- {ind['sources']['france_num']['nom']} — {ind['sources']['france_num']['perimetre']} (n={ind['sources']['france_num']['echantillon']})
- {ind['sources']['insee']['nom']} — {ind['sources']['insee']['perimetre']}

---

## 1. L'essentiel

L'adoption de l'IA en entreprise a **doublé en un an** sur les deux sources
disponibles, malgré des périmètres différents :
- France Num : {fn['taux_debut_pct']}% ({fn['annee_debut']}) → {fn['taux_fin_pct']}% ({fn['annee_fin']}) — ×{fn['multiplicateur']}
- Insee : {insee['taux_debut_pct']}% ({insee['annee_debut']}) → {insee['taux_fin_pct']}% ({insee['annee_fin']}) — ×{insee['multiplicateur']}

## 2. Secteurs en tête

- **France Num (TPE/PME)** : {secteur_top_fn['secteur']} ({secteur_top_fn['taux_adoption_ia_pct']}%)
- **Insee (entreprises 10+ salariés)** : {secteur_top_insee['secteur']} ({secteur_top_insee['taux_adoption_ia_pct']}%)

Les deux enquêtes convergent sur un même constat : les secteurs du
numérique / de l'information-communication sont largement en tête de
l'adoption de l'IA, loin devant les secteurs plus traditionnels
(agriculture, hébergement-restauration, construction).

## 3. Écart de maturité par taille d'entreprise (Insee)

{chr(10).join(f"- {d['taille']} : {d['taux_adoption_ia_pct']}%" for d in ind['adoption_par_taille'])}

Écart de **{ind['ecart_maturite_taille_points']} points** entre les plus
petites et les plus grandes entreprises.

## 4. Point méthodologique — à ne pas ignorer

{ind['note_methodologique']}

**Illustration concrète** : sur le seul secteur présent dans les deux
enquêtes ({comp['secteur'] if comp else 'N/A'}), l'écart est de
**{comp['ecart_points']:+.1f} points** ({comp['taux_france_num_pct']}% France Num
vs {comp['taux_insee_pct']}% Insee) — un rappel que le périmètre
d'échantillonnage (TPE/PME 0-249 salariés vs entreprises 10+ salariés)
change fortement le niveau mesuré, même sur un intitulé de secteur identique.

## 5. Recommandation pour le prochain baromètre de l'Observatoire

Documenter systématiquement le périmètre exact (taille, secteur, année)
de toute source secondaire mobilisée, et éviter les comparaisons brutes
de niveaux entre enquêtes à périmètres différents — comparer plutôt les
**dynamiques** (taux de croissance, hiérarchie sectorielle), qui sont
plus robustes aux différences de champ.

---
*Note générée automatiquement à partir d'agrégats officiels publiés —
démonstration technique. Pas de micro-données individuelles utilisées
(voir README pour le détail de cette limitation).*
"""

flash_note_path = OUTPUT_DIR / "flash_note.md"
flash_note_path.write_text(flash_note, encoding="utf-8")
print(f"[OK] Flash Note générée -> {flash_note_path}")

template_path = BASE_DIR / "dashboard_template.html"
dashboard_out_path = OUTPUT_DIR / "dashboard.html"
template = template_path.read_text(encoding="utf-8")
dashboard_html = template.replace("__DATA_INDICATEURS__", json.dumps(ind, ensure_ascii=False))
dashboard_out_path.write_text(dashboard_html, encoding="utf-8")
print(f"[OK] Dashboard généré -> {dashboard_out_path}")
