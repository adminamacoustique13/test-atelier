# Relais A.1 : forme de l'exemple du mode d'emploi

## Fait
- Critère 1 (`ruff format --check .` réussit) : atteint. Avant : 1 fichier à reformater (`MODE_EMPLOI.md`). Après : « 22 files already formatted ». `ruff check .` : « All checks passed! ».
- Critère 2 (trois appels et trois résultats conservés) : atteint. Les lignes 26 à 28 contiennent `somme_niveaux([60, 60])` avec `63.01 dB`, `moyenne_energetique([60, 70])` avec `67.40 dB`, `moyenne_arithmetique([60, 70])` avec `65 dB`. Seul l'espacement avant `#` a changé (deux espaces).
- Critère 3 (aucune autre ligne changée) : atteint. `git diff --numstat` donne 3 ajouts et 3 suppressions, toutes dans le bloc d'exemple.

## Fichiers touchés
- `/home/user/test-atelier/MODE_EMPLOI.md` (3 lignes de l'exemple, via `ruff format`).
- `/home/user/test-atelier/chantier/relais/A.1.md` (cette fiche, créée).

## Contrats modifiés
Aucun.

## Reste à faire
Rien pour la tâche A.1. Aucun commit ni `git add` effectué, conformément à la consigne.

## Doutes et demandes
- `decibels/` et `tests/` sont restés non modifiés. Je n'ai lancé que `ruff format --check` sur l'ensemble du dépôt, et `ruff check .`, sans `ruff format` sur ces dossiers.
- Le dépôt contient aussi un `chantier/relais/B.md` non suivi par git, que je n'ai pas touché.
- Je n'ai pas exécuté les fonctions de `decibels` pour vérifier les valeurs en commentaire. Le critère 2 demande de les conserver telles quelles, ce que j'ai fait sans les modifier.
