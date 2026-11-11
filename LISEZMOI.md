# test-atelier

Essai de la méthode d'orchestration dans une session cloud de Claude Code, lancée depuis le téléphone.

- `CLAUDE.md` : le rôle de l'orchestrateur et la table de dosage.
- `.claude/skills/orchestrateur-chantier/` : la méthode (contrat, découpage, vérification, escalade, journal).
- `.claude/agents/` : un agent par combinaison de modèle et d'effort, seize ouvriers et neuf vérificateurs.

Pour lancer un chantier : ouvrir une session Claude Code sur ce dépôt, en modèle le plus capable et effort élevé, et donner l'objectif.
- La chaîne d'hygiène : `ruff.toml`, `.claude/settings.json` et `.claude/hooks/`, `.githooks/pre-commit`, `.github/workflows/controles.yml`.
