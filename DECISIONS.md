# Journal des décisions

Une ligne par décision : date | domaine | décision | raison | alternative écartée. Ajout seul, jamais de retouche.

2026-11-11 | tests | Tests écrits avec unittest | Fourni avec Python, aucune installation | Écarté : pytest, absent de la session et dont l'installation est une zone rouge
2026-11-11 | calcul | Trois fonctions : somme_niveaux, moyenne_energetique, moyenne_arithmetique | La moyenne énergétique est celle d'usage en acoustique ; l'arithmétique est fournie à part sous un nom explicite car certaines méthodes de mesure la demandent | Écarté : une seule fonction « moyenne » avec une option, source de confusion
2026-11-11 | calcul | Somme calculée en factorisant le niveau le plus élevé | Évite le dépassement de capacité pour des niveaux très grands ou très petits | Écarté : somme directe des 10^(L/10)
2026-11-11 | calcul | Les booléens, les valeurs infinies et NaN sont refusés | Un booléen passé par erreur ne doit pas compter pour 0 ou 1 dB ; un infini masque presque toujours une erreur en amont | Écarté : accepter moins l'infini comme « énergie nulle »
2026-11-11 | structure | Paquet `decibels/` à la racine, module `niveaux.py`, tests dans `tests/` | Disposition la plus simple pour une petite bibliothèque sans installation | Écarté : disposition `src/`
2026-11-11 | calcul | moyenne_energetique rend au moins la moyenne arithmétique exacte (plancher) | L'arrondi flottant pouvait la faire passer juste dessous pour des niveaux presque égaux ; le plancher ne peut que rapprocher de la vraie valeur (inégalité de Jensen) | Écarté : formule nue, avec une tolérance sur l'inégalité
2026-11-11 | calcul | Moyenne arithmétique calculée en fractions exactes, arrondie une seule fois | Résultat toujours égal au flottant le plus proche, aucun dépassement | Écarté : fsum divisé par n, deux fois plus rapide mais faux du dernier chiffre par endroits
2026-11-11 | calcul | Un entier trop grand pour un flottant lève ValueError ; un argument non itérable lève TypeError | Cohérence avec le refus des valeurs infinies | Écarté : laisser remonter l'erreur de Python, en anglais
2026-11-11 | calcul | Decimal et Fraction sont refusés ; les sous-classes de int et float sont acceptées, sauf bool | Lecture stricte de « ni int ni float » | Écarté : accepter tout nombre réel au sens de numbers.Real
