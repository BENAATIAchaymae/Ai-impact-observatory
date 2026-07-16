"""
Données primaires — sources réelles et sourcées
===================================================
Ces données sont des AGRÉGATS OFFICIELS DÉJÀ PUBLIÉS (pas de micro-données
individuelles — voir README pour l'explication : accès bloqué par robots.txt
sur data.economie.gouv.fr / data.gouv.fr depuis un environnement automatisé).

Chaque valeur ci-dessous est vérifiable à sa source. Aucune valeur n'est
inventée ou extrapolée sans le dire explicitement.

SOURCE 1 — Baromètre France Num 2025
  Producteur : Direction Générale des Entreprises (DGE) / CREDOC
  Champ : TPE et PME françaises (0 à 249 salariés)
  Échantillon : 11 021 entreprises répondantes (3 043 PME + 7 978 TPE)
  Publication : 15 septembre 2025
  URL : https://www.francenum.gouv.fr/barometre-france-num

SOURCE 2 — Enquête TIC Entreprises 2024 (Insee)
  Producteur : Insee
  Champ : entreprises françaises de 10 salariés ou plus
         (hors secteurs agricole, financier, assurance)
  Publication : Insee Première n°2061, juillet 2025
  URL : https://www.insee.fr/fr/statistiques/8616837

ATTENTION — Point méthodologique important à souligner en entretien :
Les deux sources ne couvrent PAS le même périmètre d'entreprises
(TPE/PME 0-249 salariés vs entreprises 10+ salariés). Les taux ne sont
donc pas directement comparables terme à terme — c'est un vrai exemple
de la vigilance méthodologique attendue par l'offre visée ("rigueur
méthodologique", "esprit critique sur les biais et limites").
"""

DONNEES_FRANCE_NUM_2025 = {
    "source": "Baromètre France Num 2025 (DGE/CREDOC)",
    "perimetre": "TPE/PME françaises, 0 à 249 salariés",
    "echantillon": 11021,
    "url": "https://www.francenum.gouv.fr/barometre-france-num",
    "adoption_ia_globale": {
        2024: 13.0,
        2025: 26.0,
    },
    "adoption_ia_par_secteur_2025": {
        # secteur: (taux 2025 %, évolution vs 2024)
        "Numérique (NTIC)": (51.0, "+11 pts"),
        "Services spécialisés & techniques": (41.0, "+19 pts"),
        "Services à la personne": (29.0, "x3,2"),
        "Hébergement-restauration": (20.0, "x2,5"),
        "Industrie agro-alimentaire": (15.0, "x2,5"),
        "Agriculture": (9.0, "x2,3"),
    },
}

DONNEES_INSEE_2024 = {
    "source": "Enquête TIC Entreprises 2024 (Insee)",
    "perimetre": "Entreprises françaises de 10 salariés ou plus (hors agricole/financier/assurance)",
    "url": "https://www.insee.fr/fr/statistiques/8616837",
    "adoption_ia_globale": {
        2023: 6.0,
        2024: 10.0,
    },
    "adoption_ia_par_taille_2024": {
        "< 50 salariés": 9.0,
        "50-249 salariés": 15.0,
        "250 salariés ou plus": 33.0,
    },
    "adoption_ia_par_secteur_2024": {
        "Information & communication": (42.0, "+12 pts"),
        "Act. spécialisées, scientifiques, techniques": (17.0, None),
        "Commerce": (10.0, "x2,5 (vs 4% en 2023)"),
        "Activités immobilières": (14.0, "vs 7% en 2023"),
        "Transport & entreposage": (5.0, None),
        "Hébergement-restauration": (5.0, None),
        "Construction": (3.0, None),
    },
    "types_technologies_ia_2024": {
        "Analyse de langage écrit (NLP)": 44.0,
        "Machine learning (analyse de données)": 41.0,
    },
}
