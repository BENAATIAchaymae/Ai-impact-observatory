# AI Impact Observatory — Demo Pipelines

Two small end-to-end Python pipelines demonstrating how to build data pipelines and dashboards for tracking AI adoption in businesses. Each folder is self-contained: run its `run_pipeline.py` to regenerate the flash note and dashboard.

## secondaire/ — Secondary data
Cross-analyzes two real, published surveys (France Num 2025, Insee 2024) on AI adoption in French companies. Shows how to combine external sources critically — comparing sector/size breakdowns and flagging where the two surveys aren't directly comparable (different company-size scope).

- `sources_reelles.py` — hard-coded published figures (sourced)
- `01_chargement_donnees.py` — load into DataFrames
- `02_analyse_croisee.py` — cross-source comparison and analysis
- `03_generer_livrables.py` — generate flash note + dashboard
- `dashboard.html` — interactive Plotly dashboard
- `flash_note.md` — generated summary

## primaire/ — Primary data
Simulates an original barometer: a questionnaire deployed twice (6 months apart) to a partner panel, plus qualitative interviews, to track how AI maturity evolves over time. Data is simulated since the instrument hasn't been deployed yet — a stand-in for a pilot test.

- `questionnaire.py` — survey design + sampling plan
- `01_conception_et_deploiement.py` — questionnaire design + simulated deployment (2 waves)
- `02_etudes_cas_qualitatives.py` — simulated interviews + thematic coding
- `03_controle_qualite.py` — data quality & sample representativeness checks
- `04_generer_livrables.py` — generate flash note + dashboard
- `dashboard.html` — interactive Plotly dashboard
- `flash_note.md` — generated summary

## Requirements
Python 3, `pandas`. No external data downloads.
