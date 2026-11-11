#!/usr/bin/env bash
# Premier contrôle de la chaîne d'hygiène : après chaque fichier écrit ou modifié par Claude,
# on le met en forme et on le corrige. Ce qui reste à corriger est renvoyé à Claude (code 2).
# Python : Ruff. Rust : rustfmt (clippy passe au commit et sur GitHub, il demande tout le projet).

fichier=$(python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' 2>/dev/null)
[ -n "$fichier" ] && [ -f "$fichier" ] || exit 0

case "$fichier" in
  *.py)
    command -v ruff >/dev/null || exit 0
    ruff format --quiet "$fichier"
    if ! sortie=$(ruff check --fix --quiet "$fichier" 2>&1); then
      echo "Ruff signale des problèmes dans $fichier, à corriger avant de continuer :" >&2
      echo "$sortie" >&2
      exit 2
    fi
    ;;
  *.rs)
    command -v rustfmt >/dev/null || exit 0
    rustfmt --edition 2021 "$fichier" 2>/dev/null || true
    ;;
esac
exit 0
