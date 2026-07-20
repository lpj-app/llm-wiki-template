#!/usr/bin/env bash
set -euo pipefail
# Converts everything in raw/inbox/ to Markdown and moves it into the target raw/ subfolder.
# Usage: ./scripts/convert-pdf.sh <target-subfolder-under-raw>
TARGET="${1:?Usage: convert-pdf.sh <target-subfolder-under-raw>}"
mkdir -p "raw/$TARGET"
for f in raw/inbox/*; do
  [ -e "$f" ] || continue
  base="$(basename "${f%.*}")"
  pandoc "$f" -o "raw/$TARGET/$base.md" || echo "pandoc failed on $f, convert manually"
  mv "$f" "raw/inbox/.converted-$base-$(date +%s)"
done
echo "Converted inbox -> raw/$TARGET/"
