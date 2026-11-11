# Profil du projet

## Nature du projet
Petite bibliothèque Python de calcul sur des niveaux sonores en décibels. Python 3.13, sans dépendance extérieure.

## Commandes
- Tests : `python3 -m unittest discover -s tests -v`
- Contrôle de forme : `ruff check .` puis `ruff format --check .`

Les tests utilisent `unittest`, qui fait partie de Python. `pytest` n'est pas installé dans la session, et installer une dépendance est une zone rouge.

## Mode de périmètre
Strict : un agent ne modifie rien hors des fichiers que sa tâche lui attribue.

## Règles propres au projet
- Code, noms de fonctions, commentaires et messages d'erreur en français, sans accent dans les identifiants.
- Aucun smiley ni émoji dans les fichiers.
- Les agents ne commitent jamais.
- Rien d'iOS ne se compile ni ne se teste ici.
