# decibels : mode d'emploi

`decibels` est une petite bibliothèque Python, sans dépendance, qui combine des niveaux sonores exprimés en décibels (dB). Elle exige Python 3.11 ou plus.

## Les trois fonctions

Toutes trois s'importent ainsi :

```python
from decibels import somme_niveaux, moyenne_energetique, moyenne_arithmetique
```

Chacune prend un itérable de nombres (niveaux en dB) et rend un `float`.

- `somme_niveaux(niveaux)` : somme énergétique de plusieurs sources. Elle calcule L = 10·log10(Σ 10^(Li/10)). Deux sources de même niveau ne donnent pas le double en dB : elles donnent environ 3 dB de plus.
- `moyenne_energetique(niveaux)` : moyenne des énergies. Elle calcule L = 10·log10((1/n)·Σ 10^(Li/10)). C'est la moyenne d'usage en acoustique.
- `moyenne_arithmetique(niveaux)` : simple moyenne des valeurs en dB, calculée comme (Σ Li)/n. Elle ne tient pas compte de l'énergie : à utiliser avec prudence pour des niveaux sonores.

Une entrée vide, infinie ou NaN lève `ValueError`. Une valeur non numérique, ou un booléen, lève `TypeError`.

## Exemple

```python
from decibels import somme_niveaux, moyenne_energetique, moyenne_arithmetique

somme_niveaux([60, 60])           # 63.01 dB
moyenne_energetique([60, 70])     # 67.40 dB
moyenne_arithmetique([60, 70])    # 65 dB
```

Les valeurs arrondies à deux décimales sont celles de l'exemple. La fonction rend le résultat exact en `float`.

## Tester

Depuis la racine du dépôt, lancer :

```
python3 -m unittest discover -s tests -v
```

Aucun outil externe n'est nécessaire : seule la bibliothèque standard de Python est utilisée.
