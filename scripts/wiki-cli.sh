#!/usr/bin/env bash
# Interactive CLI menu using the repos utility scripts.
# Settings (e.g. wiki name, first-setup flag) live in root dir/.wiki.conf
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF="$SCRIPT_DIR/../.wiki.conf"

load_conf() {
  WIKI_NAME="personal-llm-wiki"
  FIRST_SETUP_DONE=false
  if [ -f "$CONF" ]; then source "$CONF"; fi
}

save_conf() {
  cat > "$CONF" <<EOF
WIKI_NAME="$WIKI_NAME"
FIRST_SETUP_DONE=$FIRST_SETUP_DONE
EOF
}

banner() {
  echo "=================================="
  echo "        $WIKI_NAME"
  echo "=================================="
}

check_deps() {
  echo "Checking required tools..."
  local missing=0
  for tool in pdftotext pandoc python3; do
    if command -v "$tool" >/dev/null 2>&1; then
      echo "  [ok]      $tool"
    else
      echo "  [MISSING] $tool"
      missing=1
    fi
  done
  if command -v ocrmypdf >/dev/null 2>&1; then
    echo "  [ok]      ocrmypdf (optional, OCR for scanned PDFs)"
  else
    echo "  [missing] ocrmypdf (optional, OCR for scanned PDFs)"
  fi
  if [ "$missing" -eq 1 ]; then
    echo "Some required tools are missing. On Debian/Ubuntu (incl. WSL):"
    echo "  sudo apt install poppler-utils pandoc python3 ocrmypdf"
  fi
}

first_setup() {
  check_deps
  read -erp "Wiki name [personal-llm-wiki]: " name
  WIKI_NAME="${name:-personal-llm-wiki}"
  FIRST_SETUP_DONE=true
  save_conf
  echo "Saved. Wiki name set to '$WIKI_NAME'."
}

load_conf

while true; do
  banner
  if [ "$FIRST_SETUP_DONE" != "true" ]; then
    echo "[1] First setup"
    echo "[0] Exit"
    read -erp "> " choice
    case "$choice" in
      1) first_setup ;;
      0) exit 0 ;;
      *) echo "Invalid option." ;;
    esac
  else
    echo "[1] Flatten a directory"
    echo "[2] Convert raw/inbox to markdown"
    echo "[3] Revert converted files"
    echo "[4] Install git hooks"
    echo "[5] More options"
    echo "[0] Exit"
    read -erp "> " choice
    case "$choice" in
      1) read -erp "> Path to flatten: " p; "$SCRIPT_DIR/flatten-dir.sh" "$p" ;;
      2) read -erp "> Target subfolder under raw: " t; "$SCRIPT_DIR/convert-to-md.sh" "$t" ;;
      3) read -erp "> Path [raw/inbox]: " p; "$SCRIPT_DIR/revert-convert.sh" "${p:-raw/inbox}" ;;
      4) "$SCRIPT_DIR/install-hooks.sh" ;;
      5) echo "More options coming soon." ;;
      0) exit 0 ;;
      *) echo "Invalid option." ;;
    esac
  fi
  echo
done
