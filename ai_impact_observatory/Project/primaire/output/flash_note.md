# Flash Note — Baromètre AI Impact Observatory (S1-S2)
### Institut de recherche IA
### Données primaires — instrument original, panel de partenaires

**Échantillon :** 80 entreprises partenaires (vague 1), dont 66
suivies en vague 2 (+6 mois) — panel de convenance, non représentatif de la
population nationale (voir note méthodologique).

---

## 1. Résultats quantitatifs

- Maturité IA moyenne : **2.69/5 (S1) → 2.91/5 (S2)**
- Progression moyenne du panel suivi (mesure longitudinale réelle,
  même entreprises interrogées 2 fois) : **+0.28 point en 6 mois**
- Obstacle principal cité : **Budget limité**

**Par taille d'entreprise (S1) :**
- ETI (250-4999 sal.) : 2.79/5
- Grand groupe (5000+ sal.) : 3.72/5
- PME (10-249 sal.) : 1.96/5

**Par secteur (S1) :**
- Banque & Assurance : 3.0/5
- Conseil : 3.01/5
- Industrie : 2.48/5
- Public : 2.66/5
- Retail : 2.69/5
- Santé : 1.91/5
- Énergie : 2.9/5

## 2. Résultats qualitatifs (études de cas longitudinales)

12 entreprises suivies par entretien à deux reprises
(T0 et T0+6 mois), codage thématique automatisé sur une grille définie a priori.

**Obstacles dominants à T0 :** {'Montée en compétences': 3, 'Preuve de valeur (ROI)': 6, 'Gouvernance des données': 2, 'Résistance au changement': 2, 'Dépendance fournisseur': 2}
**Thèmes dominants à T1 (+6 mois) :** {'Montée en compétences': 3, 'Preuve de valeur (ROI)': 3, 'Gouvernance des données': 2, 'Résistance au changement': 2, 'Dépendance fournisseur': 2}

Le thème qui recule le plus entre T0 et T1 est **Preuve de valeur (ROI)**
— cohérent avec la progression quantitative de maturité observée sur le
même panel.

## 3. Note méthodologique

- **Échantillon** : conforme aux quotas déclarés avant collecte
  (écarts : {'PME (10-249 sal.)': 0.0, 'ETI (250-4999 sal.)': 0.0, 'Grand groupe (5000+ sal.)': 0.0}).
- **Contrôle qualité** : 0
  lignes rejetées sur 146
  (détail : {'maturite_hors_bornes': 0, 'budget_negatif': 0, 'doublons_panel_vague': 0, 'incoherence_usage_sans_type_ia': 0}).
- **Limite assumée** : panel de partenaires, pas un échantillon aléatoire
  national — les niveaux ne sont pas généralisables, seule la **dynamique**
  (progression du même panel dans le temps) est interprétable avec confiance.
- **Reproductibilité** : questionnaire versionné, seed de simulation fixée,
  pipeline scripté rejouable à l'identique.

---
*Note générée automatiquement — démonstration technique. Instrument de
recherche original (baromètre + études de cas), données simulées car non
encore déployé (voir README).*
