"""
Le questionnaire du "Baromètre AI Impact Observatory" — instrument original
================================================================================
Ceci est la conception méthodologique elle-même (mission : "Contribuer à la
conception méthodologique des dispositifs d'enquête"). Chaque question a une
justification de recherche, pas juste un intitulé.

Structure inspirée des standards de baromètres d'adoption technologique
(type France Num, Insee TIC) mais conçue spécifiquement pour le besoin de
l'Observatoire : mesurer la MATURITÉ, pas seulement l'usage binaire.
"""

QUESTIONNAIRE = [
    {
        "id": "Q1_perimetre",
        "libelle": "Secteur d'activité principal de l'entreprise",
        "type": "choix_unique",
        "modalites": ["Banque & Assurance", "Industrie", "Retail", "Santé", "Conseil", "Énergie", "Public"],
        "justification": "Variable de stratification — permet l'analyse sectorielle demandée par l'offre.",
    },
    {
        "id": "Q2_taille",
        "libelle": "Taille de l'entreprise (effectif)",
        "type": "choix_unique",
        "modalites": ["PME (10-249 sal.)", "ETI (250-4999 sal.)", "Grand groupe (5000+ sal.)"],
        "justification": "Variable de stratification — l'effet taille est un résultat structurant de la littérature (cf. France Num, Insee).",
    },
    {
        "id": "Q3_usage_actuel",
        "libelle": "Votre entreprise utilise-t-elle actuellement au moins un outil d'IA en production (hors phase de test) ?",
        "type": "binaire",
        "modalites": ["Oui", "Non"],
        "justification": "Question filtre — distingue adoption réelle (production) de la simple expérimentation, contrairement aux baromètres qui ne mesurent que l'intention.",
    },
    {
        "id": "Q4_maturite",
        "libelle": "Sur une échelle de 1 (aucune maturité) à 5 (IA intégrée au pilotage stratégique), où situez-vous votre organisation ?",
        "type": "echelle_likert_5",
        "justification": "Indicateur composite central du baromètre — permet un suivi longitudinal comparable d'une vague à l'autre.",
    },
    {
        "id": "Q5_types_ia",
        "libelle": "Quels types d'IA sont déployés ? (plusieurs réponses possibles)",
        "type": "choix_multiple",
        "modalites": ["IA générative", "Machine learning prédictif", "Automatisation (RPA)", "Vision par ordinateur", "NLP / traitement documentaire"],
        "justification": "Permet de croiser avec la grille multi-dimensionnelle de la veille (mission 1) — même typologie utilisée des deux côtés.",
    },
    {
        "id": "Q6_fonction",
        "libelle": "Quelle fonction de l'entreprise est la plus transformée par l'IA aujourd'hui ?",
        "type": "choix_unique",
        "modalites": ["RH", "Marketing & Ventes", "Production / Supply chain", "Finance", "Juridique & Conformité", "R&D"],
        "justification": "Complète la grille multi-dimensionnelle — donnée primaire venant confirmer/contredire les tendances observées en veille.",
    },
    {
        "id": "Q7_budget",
        "libelle": "Quel pourcentage du budget IT est alloué à l'IA cette année ?",
        "type": "numerique_pct",
        "justification": "Indicateur d'investissement réel — plus robuste qu'une simple déclaration d'intérêt.",
    },
    {
        "id": "Q8_obstacle",
        "libelle": "Quel est le principal frein à l'adoption de l'IA dans votre organisation ?",
        "type": "choix_unique",
        "modalites": [
            "Manque de compétences internes", "Budget limité",
            "Gouvernance des données insuffisante", "Résistance au changement",
            "Incertitude réglementaire (AI Act)", "ROI difficile à démontrer",
        ],
        "justification": "Question ouverte à l'origine dans la conception, fermée ici après un pré-test (voir note reproductibilité) pour fiabiliser le codage.",
    },
    {
        "id": "Q9_accompagnement",
        "libelle": "Accepteriez-vous de participer à un entretien qualitatif de suivi dans 6 mois ?",
        "type": "binaire",
        "modalites": ["Oui", "Non"],
        "justification": "Sert de recrutement pour le volet qualitatif longitudinal (mission 2, 2e point) — panel suivi dans le temps, pas un échantillon jetable.",
    },
]

# ---------------------------------------------------------------------------
# Méthodologie d'échantillonnage (déclarée avant collecte — bonne pratique
# de reproductibilité : le plan d'échantillonnage ne doit jamais être
# ajusté après avoir vu les résultats)
# ---------------------------------------------------------------------------
PLAN_ECHANTILLONNAGE = {
    "population_cible": "Entreprises partenaires de l'école et de son écosystème (Chaire IA, réseau alumni entreprises, partenaires corporate)",
    "methode": "Échantillonnage stratifié par quotas (secteur x taille), non probabiliste (panel de partenaires, pas de base de sondage aléatoire disponible)",
    "taille_cible": 80,
    "quotas": {
        "PME (10-249 sal.)": 0.40,
        "ETI (250-4999 sal.)": 0.35,
        "Grand groupe (5000+ sal.)": 0.25,
    },
    "limite_declaree": (
        "Échantillon de convenance (partenaires) : pas représentatif de "
        "la population des entreprises françaises dans son ensemble, contrairement "
        "à France Num ou l'enquête Insee. Limite à mentionner explicitement dans "
        "tout livrable — c'est un panel de suivi, pas une enquête nationale."
    ),
    "frequence": "Semestrielle (S1 : mars, S2 : septembre)",
    "reproductibilite": "Questionnaire versionné (v1.0 ci-dessus) et gelé avant chaque vague — aucune modification de formulation en cours de collecte pour garantir la comparabilité inter-vagues.",
}
