#!/usr/bin/env bash
set -euo pipefail
chmod +x "$(dirname "$0")/hooks/pre-commit"
git config core.hooksPath scripts/hooks
echo "Hook installed. raw/ is now protected against edits/deletes on commit."
