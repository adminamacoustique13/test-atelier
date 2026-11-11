# Relais, tâche B : fonctions de calcul sur les niveaux sonores et leurs tests

## Fait

Les trois fonctions sont dans `decibels/niveaux.py`, exportées par `decibels/__init__.py`. Les tests sont dans `tests/test_niveaux.py` : 47 tests, dont un par critère dans la classe `TestCriteres`.

| Critère | État | Test | Valeur obtenue |
|---|---|---|---|
| 1 | tenu | `test_critere_01_somme_de_60_et_60` | `63.01029995663981` |
| 2 | tenu | `test_critere_02_somme_de_60_et_70` | `70.41392685158225` |
| 3 | tenu | `test_critere_03_somme_de_dix_niveaux_de_50` | `60.0`, exactement |
| 4 | tenu | `test_critere_04_somme_d_un_seul_niveau` | `x`, exactement |
| 5 | tenu | `test_critere_05_moyenne_energetique_de_60_et_70` | `67.40362689494243` |
| 6 | tenu | `test_critere_06_moyenne_energetique_de_niveaux_egaux` | `x`, exactement |
| 7 | tenu | `test_critere_07_moyenne_arithmetique_de_60_et_70` | `65.0`, exactement |
| 8 | tenu, même sans la tolérance | `test_critere_08_moyenne_energetique_au_moins_egale_a_l_arithmetique` | voir le doute 1 |
| 9 | tenu | `test_critere_09_somme_de_niveaux_de_4000` | `4003.0102999566398` |
| 10 | tenu | `test_critere_10_somme_de_niveaux_de_moins_4000` | `-3996.9897000433602` |
| 11 | tenu, trois fonctions | `test_critere_11_generateur_parcouru_une_seule_fois` | |
| 12 | tenu, trois fonctions | `test_critere_12_entree_vide` | `ValueError` |
| 13 | tenu, trois fonctions | `test_critere_13_valeur_ni_int_ni_float` | `TypeError` |
| 14 | tenu, trois fonctions | `test_critere_14_booleen` | `TypeError` |
| 15 | tenu, trois fonctions | `test_critere_15_valeur_infinie` | `ValueError`, dans les deux sens |
| 16 | tenu, trois fonctions | `test_critere_16_valeur_nan` | `ValueError` |
| 17 | tenu | `test_critere_17_niveaux_negatifs` | `-6.9897000433601875` |
| 18 | tenu | les dix-sept tests ci-dessus, numérotés de 01 à 17 | |

Commandes lancées depuis la racine, toutes réussies :

- `python3 -m unittest discover -s tests -v` : 47 tests, OK, en moins d'une seconde (Python 3.13.18). Même résultat avec les Python 3.11.18 et 3.12.3 présents sur la machine.
- `ruff check --line-length 100 decibels tests` : All checks passed.
- `ruff format --check --line-length 100 decibels tests` : 3 files already formatted.

Preuves ajoutées aux critères :

- Valeurs de référence : je les ai toutes recalculées avec le module `decimal` à 60 chiffres, par la formule directe sans factorisation. Aucune ne me paraît fausse. Valeurs exactes : 63,0102999566 ; 70,4139268516 ; 67,4036268949 ; 4003,0102999566 ; -3996,9897000434 ; -6,9897000434.
- Les tests comparent aussi les trois fonctions à ce calcul décimal sur 720 listes tirées au hasard avec une graine fixe (tolérance 1e-9). Hors dépôt, sur 30 000 listes, l'écart le plus grand est de 2,3e-13 dB.
- Épreuve des tests par mutation, sur une copie hors du dépôt : 67 altérations du module (facteur 20, logarithme naturel, diviseur oublié ou mal placé, pas de factorisation, booléens acceptés, double parcours, etc.). 62 font échouer au moins un test. Les 5 autres passent parce qu'elles ne changent pas la formule : `sum` à la place de `math.fsum` (identique à partir de Python 3.12, détectée sous 3.11), `**` à la place de `math.pow` (identique sur cette machine), entiers non convertis en flottants (identique tant que l'entier a un flottant égal), multiplication par 0,1 et différence de deux logarithmes (écart au dernier chiffre seulement).
- Section de texte citée à côté du code : `chantier/CONTRAT.md`, rubrique « Ce que la bibliothèque fera », et la décision du journal sur la factorisation.
- Deux affirmations des commentaires du code ont été vérifiées dans le code source public de CPython 3.13, consulté en ligne sans rien installer : la conversion d'une fraction en flottant est arrondie correctement, et `math.pow` ne lève pas d'erreur quand le résultat est trop petit, alors que l'opérateur `**` s'en remet à la bibliothèque C.

## Fichiers touchés

- `decibels/__init__.py` (créé)
- `decibels/niveaux.py` (créé)
- `tests/test_niveaux.py` (créé)
- `chantier/relais/B.md` (créé, cette fiche)

Rien d'autre n'a été modifié. Rien installé, rien commité, rien poussé, aucun fichier supprimé. La commande de test a créé des dossiers `__pycache__` dans `decibels/` et `tests/` : le `.gitignore` les écarte, je ne les ai pas supprimés.

## Contrats modifiés

Aucun. `from decibels import somme_niveaux, moyenne_energetique, moyenne_arithmetique` fonctionne ; chaque fonction prend un itérable de nombres réels et rend un `float`.

## Reste à faire

Rien dans mon périmètre.

Hors de mon périmètre, constaté sans y toucher : la commande de forme du profil, `ruff format --check .`, échoue sur `MODE_EMPLOI.md` (tâche A). Cette version de ruff vérifie aussi les blocs Python des fichiers Markdown et veut exactement deux espaces avant les commentaires de l'exemple, au lieu de l'alignement actuel. `ruff check .` passe.

## Doutes et demandes

Choix que la consigne ne tranchait pas. Les quatre premiers mériteraient une ligne au journal si vous les gardez.

1. Plancher dans `moyenne_energetique` (critère 8). Le critère dit « pour toute liste ». Or le calcul direct, même juste, peut rendre le flottant situé juste sous la moyenne arithmétique quand les niveaux sont presque égaux. Exemple : `[100000000.00000001, 100000000.00000003]` donne 100000000.00000001 contre une moyenne arithmétique de 100000000.00000003, soit un écart de 1,5e-8, supérieur à 1e-9. À des niveaux réalistes le même effet existe, mais il vaut 7e-15 dB et la tolérance le couvre. J'ai donc ajouté une ligne : la fonction rend le plus grand des deux, calcul direct ou moyenne arithmétique. C'est démontrable (inégalité de Jensen) et le résultat ne peut que se rapprocher de la vraie valeur. Le critère 8 tient alors sans tolérance, pour tous les flottants. Si vous préférez la formule nue, il faut retirer cette ligne et adapter trois tests ; le critère 8 ne tiendrait plus qu'en dessous de 8 millions de décibels environ.
2. Moyenne arithmétique exacte. Elle est calculée en fractions et arrondie une seule fois : c'est ce qui rend le plancher rigoureux, et cela supprime tout dépassement de capacité. Le prix est la vitesse : pour un million de valeurs, environ 0,3 s pour la somme, 0,5 s pour la moyenne énergétique, 0,4 s pour la moyenne arithmétique. Avec `math.fsum(v) / n`, la moyenne arithmétique irait environ deux fois plus vite, mais ce calcul se trompe parfois du dernier chiffre et déborde près de 1e308.
3. Critère 13, test du type par `isinstance`. Les sous-classes de `int` et de `float` sont acceptées, sauf `bool`. Conséquence de la lettre du critère : `Decimal` et `Fraction` sont refusés. Pour numpy, qui n'est pas installé ici, donc non vérifié : `numpy.float64` hérite de `float` et serait accepté, `numpy.float32` et `numpy.int64` seraient refusés.
4. Un entier trop grand pour un flottant, par exemple `10**400`, lève `ValueError`, par cohérence avec les valeurs infinies. Un argument qui n'est pas un itérable, par exemple `somme_niveaux(60)`, lève `TypeError`. Les deux ont un message en français.
5. Les entiers sont convertis en flottants à l'entrée. Au-delà de 2^53, un entier n'a pas toujours de flottant égal : `somme_niveaux([2**53 + 1])` rend 9007199254740992.0. Le critère 4 ne peut pas tenir à 1e-9 près pour de tels entiers, puisque le contrat impose de rendre un `float`.
6. Un objet `bytes` est un itérable d'entiers : il passe (`somme_niveaux(b"<<")` donne 63,01). Je ne l'ai pas refusé, la consigne ne le demandant pas. À trancher.
7. Pour parcourir un générateur une seule fois, les valeurs sont recopiées dans une liste : la mémoire croît avec le nombre de niveaux.
8. La consigne ne désigne aucune norme. Je n'ai pas cité de clause de norme de mémoire, faute de pouvoir la vérifier ici, et je ne connais pas de cas de référence officiels pour ces formules : les références sont celles de la consigne, recalculées indépendamment.

Demande : dites-moi si le plancher du point 1 et le choix `ValueError` du point 4 vous conviennent.
