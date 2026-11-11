# Relais, tâche A : squelette du paquet `decibels`

## Fait

1. `pyproject.toml` se lit avec `tomllib` sans erreur. Vérifié par la commande prescrite.
2. Projet `decibels`, version `0.1.0`, `requires-python = ">=3.11"`. Vérifié à la lecture du fichier parsé.
3. Aucune dépendance : `dependencies = []`.
4. Ruff lit `line-length = 100`. Vérifié : `ruff check --show-settings pyproject.toml` affiche `linter.line_length = 100`. Le grep de `line-length` de la consigne ne rend rien car ruff affiche le réglage sous le nom `line_length`.
5. `.gitignore` contient `__pycache__/` et `*.pyc`.
6. `MODE_EMPLOI.md` nomme les trois fonctions et décrit chacune : somme énergétique, moyenne énergétique, moyenne arithmétique, avec leurs formules.
7. `MODE_EMPLOI.md` donne la commande `python3 -m unittest discover -s tests -v`.
8. Exemple chiffré : `somme_niveaux([60, 60])` donne 63.01 dB, `moyenne_energetique([60, 70])` donne 67.40 dB, `moyenne_arithmetique([60, 70])` donne 65 dB. Les trois valeurs ont été recalculées avec Python avant écriture.

Aucun smiley ni émoji dans les fichiers. Aucun test lancé, conformément à la consigne (les dossiers `decibels/` et `tests/` n'existent pas encore et ne relèvent pas de mon périmètre). Rien installé, rien commité, rien poussé.

## Fichiers touchés

- `/home/user/test-atelier/pyproject.toml` (créé)
- `/home/user/test-atelier/.gitignore` (créé)
- `/home/user/test-atelier/MODE_EMPLOI.md` (créé)
- `/home/user/test-atelier/chantier/relais/A.md` (créé, cette fiche)

## Contrats modifiés

Aucun. Le `pyproject.toml` déclare `readme = "MODE_EMPLOI.md"` et `[tool.setuptools.packages.find] include = ["decibels*"]`, ce qui suppose que le paquet vit bien dans `decibels/` à la racine, comme décidé.

## Reste à faire

Rien de mon côté. Pour l'orchestrateur : `pip install -e .` n'a pas été testé (pas d'installation autorisée). Le build setuptools reste à vérifier une fois `decibels/` présent.

## Doutes et demandes

- Le `.ruff_cache/` créé par la commande ruff de contrôle apparaîtra peut-être dans `git status`. Je n'ai pas pu le supprimer (zone rouge : suppression de fichiers). Je n'ai pas ajouté `.ruff_cache/` au `.gitignore` car il ne figure pas dans mon périmètre explicite de rédaction ; à trancher par l'orchestrateur.
- La consigne demandait de « ne pas tester les dossiers `decibels/` et `tests/` » : je m'y suis tenu, donc la commande `unittest` de `MODE_EMPLOI.md` n'a pas été exécutée.
