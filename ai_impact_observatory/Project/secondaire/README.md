# AI Impact Observatory — Démo "données primaires" (sources réelles)

Pipeline utilisant de **vraies données officielles publiées** (pas de
synthétique), avec Pandas pour le traitement et Plotly pour la restitution —
les deux outils cités dans ta présentation (slides 3 et 5).

## Sources utilisées

| Source | Producteur | Périmètre | Année |
|---|---|---|---|
| Baromètre France Num 2025 | DGE / CREDOC | TPE/PME 0-249 salariés (n=11 021) | 2025 |
| Enquête TIC Entreprises | Insee | Entreprises 10+ salariés | 2024 |

Toutes les valeurs viennent de communiqués et pages officielles publiés
(francenum.gouv.fr, insee.fr) — vérifiables indépendamment.

## Structure

```
secondaire/
├── data/
│   └── sources_reelles.py       # Agrégats officiels, sourcés (dur-codés)
├── pipeline/
│   ├── 01_chargement_donnees.py # Pandas : structuration en DataFrames
│   ├── 02_analyse_croisee.py    # Analyse critique : comparaison des 2 sources
│   └── 03_generer_livrables.py  # Flash Note + injection dashboard
├── dashboard_template.html       # Template Plotly.js
├── run_pipeline.py
└── output/
    ├── flash_note.md
    └── dashboard.html
```

## Le point fort à mettre en avant en entretien

**L'analyse critique croisée (`02_analyse_croisee.py`)** est le vrai
"plus" de cette démo : au lieu de juste afficher deux sources côte à côte,
le script identifie que France Num et Insee **ne couvrent pas le même
périmètre d'entreprises** (0-249 salariés vs 10+ salariés), et le prouve
concrètement : sur le seul secteur présent dans les deux enquêtes
(hébergement-restauration), l'écart atteint **15 points** (20% vs 5%) —
uniquement à cause de la différence de champ d'échantillonnage.


## Lancer la démo

```bash
python run_pipeline.py
# puis ouvrir output/dashboard.html dans un navigateur
```
