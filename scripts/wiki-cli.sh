#!/usr/bin/env bash
# Interactive CLI menu using the repos utility scripts.
# Settings (e.g. wiki name, first-setup flag) live in root dir/.wiki.conf
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF="$SCRIPT_DIR/../.wiki.conf"

load_conf() {
  WIKI_NAME="personal-llm-wiki"
  FIRST_SETUP_DONE=false
  LIFE_AREAS="arbeit,alltag,schule,studium,projekte,ideen,home,archive"
  if [ -f "$CONF" ]; then source "$CONF"; fi
}

save_conf() {
  cat > "$CONF" <<EOF
WIKI_NAME="$WIKI_NAME"
FIRST_SETUP_DONE=$FIRST_SETUP_DONE
LIFE_AREAS="$LIFE_AREAS"
EOF
}

banner() {
  local title="${1:-$WIKI_NAME}"
  echo "=================================="
  echo "        $title"
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

add_life_area() {
  read -erp "New life-area name (lowercase, kebab-case): " name
  if ! [[ "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
    echo "Invalid name — use lowercase letters, digits, hyphens, starting with a letter."
    return
  fi
  IFS=',' read -ra areas <<< "$LIFE_AREAS"
  for a in "${areas[@]}"; do
    if [ "$a" = "$name" ]; then
      echo "'$name' already exists in LIFE_AREAS."
      return
    fi
  done
  LIFE_AREAS="$LIFE_AREAS,$name"
  save_conf
  echo "Added '$name'. LIFE_AREAS is now: $LIFE_AREAS"
  echo "Remember to commit .wiki.conf."
}

more_options_menu() {
  while true; do
    banner "More options"
    echo "[1] Install git hooks"
    echo "[2] Check software install state"
    echo "[3] Add a life-area"
    echo "[0] Back"
    read -erp "> " choice
    case "$choice" in
      1) "$SCRIPT_DIR/install-hooks.sh" ;;
      2) check_deps ;;
      3) add_life_area ;;
      0) return ;;
      *) echo "Invalid option." ;;
    esac
  done
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
    echo "[4] More options"
    echo "[0] Exit"
    read -erp "> " choice
    case "$choice" in
      1) read -erp "> Path to flatten: " p; "$SCRIPT_DIR/flatten-dir.sh" "$p" ;;
      2) read -erp "> Target subfolder under raw: " t; "$SCRIPT_DIR/convert-to-md.sh" "$t" ;;
      3) read -erp "> Path [raw/inbox]: " p; "$SCRIPT_DIR/revert-convert.sh" "${p:-raw/inbox}" ;;
      4) more_options_menu ;;
      0) exit 0 ;;
      *) echo "Invalid option." ;;
    esac
  fi
  echo
done
