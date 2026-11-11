#!/usr/bin/env bash
# Au démarrage de chaque session : branche le contrôle d'avant enregistrement (.githooks/pre-commit).
# Ne fait que régler ce dépôt ; rien n'est installé sur la machine.
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null
exit 0
