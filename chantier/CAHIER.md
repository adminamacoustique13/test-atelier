# Cahier des charges — bibliothèque de niveaux sonores

Contrat : `chantier/CONTRAT.md`, validé le 2026-11-11. Enveloppe : 6 agents, 3 tentatives par tâche, 2 montées en gamme.

Agents lancés à ce jour : 0 sur 6.

## Sous-plan unique : la bibliothèque `decibels`

Disposition :

- `pyproject.toml`, `.gitignore`, `MODE_EMPLOI.md` : tâche A
- `decibels/__init__.py`, `decibels/niveaux.py`, `tests/test_niveaux.py` : tâche B

Les deux périmètres sont disjoints et aucune tâche n'a besoin des fichiers de l'autre pour être prouvée : elles peuvent tourner en même temps.

## Tâche A — Squelette du paquet

- État : à lancer
- Dosage : `ouvrier-mecanique` (Haiku, faible), vérifié par `verificateur-sonnet`
- Périmètre : `pyproject.toml`, `.gitignore`, `MODE_EMPLOI.md`, `chantier/relais/A.md`
- Dépendances : aucune
- Contrats : attend de B les fonctions `somme_niveaux`, `moyenne_energetique`, `moyenne_arithmetique` importables depuis `decibels`. Fournit la configuration de ruff que B respecte (longueur de ligne 100).

Critères :

1. `pyproject.toml` se lit avec `tomllib` sans erreur.
2. Il déclare le projet `decibels`, version `0.1.0`, `requires-python = ">=3.11"`.
3. Il ne déclare aucune dépendance (liste `dependencies` vide ou absente).
4. Il règle ruff sur une longueur de ligne de 100.
5. `.gitignore` écarte `__pycache__/` et `*.pyc`.
6. `MODE_EMPLOI.md` nomme les trois fonctions et dit pour chacune ce qu'elle calcule.
7. `MODE_EMPLOI.md` donne la commande de test du profil.
8. Son exemple chiffré est juste : somme de 60 et 60 dB = 63,01 dB ; moyenne énergétique de 60 et 70 dB = 67,40 dB ; moyenne arithmétique de 60 et 70 dB = 65 dB.

Preuve : lecture du fichier par `tomllib`, `ruff check .` qui accepte la configuration, relecture des chiffres par le vérificateur.

## Tâche B — Fonctions de calcul et tests

- État : à lancer
- Dosage : `ouvrier-physique` (Fable, max), vérifié par `verificateur-fable-max`
- Périmètre : `decibels/__init__.py`, `decibels/niveaux.py`, `tests/test_niveaux.py`, `chantier/relais/B.md`
- Dépendances : aucune
- Contrats : fournit les trois fonctions, importables par `from decibels import ...`. Chacune prend un itérable de nombres réels et rend un `float`.

Critères :

1. `somme_niveaux([60, 60])` vaut 63,0103 à 1e-4 près.
2. `somme_niveaux([60, 70])` vaut 70,41393 à 1e-5 près.
3. `somme_niveaux` de dix niveaux de 50 dB vaut 60,0 à 1e-9 près.
4. `somme_niveaux([x])` vaut `x` à 1e-9 près, pour un seul niveau.
5. `moyenne_energetique([60, 70])` vaut 67,40363 à 1e-5 près.
6. `moyenne_energetique` de niveaux tous égaux à `x` vaut `x` à 1e-9 près.
7. `moyenne_arithmetique([60, 70])` vaut 65,0.
8. Pour toute liste, la moyenne énergétique est supérieure ou égale à la moyenne arithmétique (à 1e-9 près).
9. `somme_niveaux([4000, 4000])` vaut 4003,0103 à 1e-4 près, sans erreur de dépassement.
10. `somme_niveaux([-4000, -4000])` vaut -3996,9897 à 1e-4 près.
11. Les trois fonctions acceptent un générateur, parcouru une seule fois.
12. Une entrée vide lève `ValueError`.
13. Une valeur qui n'est ni `int` ni `float` lève `TypeError`.
14. Un booléen lève `TypeError`.
15. Une valeur infinie lève `ValueError`.
16. Une valeur NaN lève `ValueError`.
17. Les niveaux négatifs sont acceptés : `somme_niveaux([-10, -10])` vaut -6,9897 à 1e-4 près.
18. Chaque critère de 1 à 17 a au moins un test dans `tests/test_niveaux.py`.

Preuve : la commande de test du profil passe ; le vérificateur recalcule les valeurs de référence indépendamment et éprouve les tests sur une copie hors du dépôt.

## Suivi

| Tâche | État | Agent | Tentatives | Montées | Preuve |
|---|---|---|---|---|---|
| A | à lancer | ouvrier-mecanique | 0 | 0 | |
| B | à lancer | ouvrier-physique | 0 | 0 | |
