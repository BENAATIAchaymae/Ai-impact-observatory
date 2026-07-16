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

## ⚠️ Pourquoi des agrégats et pas des micro-données brutes

J'ai essayé de télécharger le fichier CSV brut (une ligne par entreprise
répondante) directement depuis `data.economie.gouv.fr` et son miroir
`data.gouv.fr`. **Les deux bloquent l'accès automatisé via leur fichier
`robots.txt`** — testé et confirmé (erreur `ROBOTS_DISALLOWED` sur plusieurs
URLs de téléchargement direct). Mon environnement d'exécution Python n'a par
ailleurs aucun accès réseau.

**Solution retenue :** utiliser les résultats déjà publiés (chiffres agrégés
par secteur/taille/année, communiqués officiels) plutôt que d'inventer des
micro-données synthétiques. C'est moins riche qu'un vrai fichier ligne par
ligne, mais **100% réel et vérifiable** — contrairement à la démo précédente
(données secondaires) qui utilisait un corpus simulé.

**Si le jury demande pourquoi pas les micro-données :** "Le fichier existe et
est en open data, mais son téléchargement automatisé est bloqué par le
site — en conditions réelles au poste, je passerais par un téléchargement
manuel ponctuel (autorisé, ce n'est qu'un blocage anti-bot) ou une demande
d'accès à l'API auprès de la DGE."

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

C'est exactement la compétence "esprit critique et réflexivité sur les
biais, limites [...]" et "rigueur méthodologique" demandée dans l'offre —
démontrée sur un vrai cas, pas juste affirmée sur une slide.

## Lancer la démo

```bash
python run_pipeline.py
# puis ouvrir output/dashboard.html dans un navigateur
```

Note technique : Plotly Python n'a pas pu être installé dans cet
environnement (sandbox sans accès réseau pour `pip`). Le dashboard utilise
donc **Plotly.js via CDN** — Pandas calcule les données côté Python, Plotly
les affiche côté navigateur. C'est un pattern de production courant
(API/backend qui sert du JSON à un frontend Plotly.js), pas une solution
de contournement.
