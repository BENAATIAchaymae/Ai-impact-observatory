# Baromètre AI Impact Observatory — Démo "données primaires"

Cette démo suit **exactement** les 4 points de la mission 2 de l'offre visée,
un script par point :

| Point de l'offre | Script |
|---|---|
| "Concevoir et opérer les baromètres... auprès des entreprises partenaires" | `01_conception_et_deploiement.py` |
| "Mener des études de cas qualitatives longitudinales... (trajectoires, obstacles, solutions déployées)" | `02_etudes_cas_qualitatives.py` |
| "Garantir la qualité, la robustesse méthodologique et la reproductibilité" | `03_controle_qualite.py` |
| Livrables (rapport, dashboard) | `04_generer_livrables.py` |

## Pourquoi c'est simulé — et pourquoi c'est normal ici

Contrairement à la démo précédente (réutilisation du Baromètre France Num,
qui relève en réalité de la mission 1 "données secondaires"), **ce baromètre
est un instrument original de l'Observatoire, jamais encore déployé.** Il
n'existe par définition aucune vraie donnée à récupérer : la génération
simulée est ici la méthode correcte (équivalent d'un pilote/pré-test avant
un vrai terrain), pas un pis-aller lié à une contrainte technique.

## Ce qui distingue cette démo d'une simulation "gadget"

1. **Le questionnaire est un vrai instrument de recherche** (`data/questionnaire.py`)
   — chaque question a une justification méthodologique écrite, pas juste un intitulé.
2. **Le plan d'échantillonnage est déclaré AVANT la génération des données**
   — quotas figés (secteur × taille), limite de représentativité assumée
   explicitement (panel de convenance, pas une enquête nationale).
3. **Le suivi est réellement longitudinal** : la vague 2 fait progresser
   individuellement chaque entreprise du panel à partir de son propre score
   en vague 1 (avec attrition réaliste de 18%) — ce n'est pas un deuxième
   tirage indépendant qui ressemblerait au premier par hasard.
4. **Le contrôle qualité est isolé dans son propre script**, avec 3 familles
   de vérifications distinctes (validité des données, représentativité de
   l'échantillon vs quotas déclarés, reproductibilité du processus) — pas
   juste "on a nettoyé les doublons".
5. **Le codage qualitatif est automatisé mais vérifiable** : classification
   par grille de mots-clés déclarée a priori (pas un LLM boîte noire) —
   directement remplaçable par un modèle NLP fine-tuné en production, sans
   changer la logique du pipeline.

## Structure

```
primaire/
├── data/
│   └── questionnaire.py            # Instrument + plan d'échantillonnage
├── pipeline/
│   ├── 01_conception_et_deploiement.py
│   ├── 02_etudes_cas_qualitatives.py
│   ├── 03_controle_qualite.py
│   └── 04_generer_livrables.py
├── dashboard_template.html
├── run_pipeline.py
└── output/
    ├── flash_note.md
    └── dashboard.html
```

## Comment le présenter en entretien

Le point le plus fort à mettre en avant : **la cohérence entre quantitatif
et qualitatif sur le même panel**. La maturité IA progresse de +0.28 point
en 6 mois (mesure quantitative), et le thème qui recule le plus dans les
verbatims d'entretien sur la même période est justement "Preuve de valeur
(ROI)" — les deux se confirment mutuellement, ce qui est exactement l'intérêt
d'articuler quanti et quali plutôt que de les traiter en silos.

## Lancer la démo

```bash
python run_pipeline.py
# puis ouvrir output/dashboard.html dans un navigateur
```
