#!/usr/bin/env bash
set -euo pipefail

# Converts raw/inbox/ files to Markdown, moves them into the target subfolder.
# Usage: ./scripts/convert-pdf.sh <target-subfolder-under-raw>

TARGET="${1:?Usage: convert-pdf.sh <target-subfolder-under-raw>}"
mkdir -p "raw/$TARGET"
for f in raw/inbox/*; do
  [ -e "$f" ] || continue
  ext="${f##*.}"
  base="$(basename "${f%.*}")"

  if [[ "${ext,,}" == "pdf" ]]; then
    # OCR pass: adds text layer if missing
    ocrmypdf --skip-text --language deu+eng "$f" "$f.ocr.pdf" 2>/dev/null || cp "$f" "$f.ocr.pdf"
    pdftotext -layout "$f.ocr.pdf" "raw/$TARGET/$base.md" \
      && echo "converted: $f -> raw/$TARGET/$base.md" \
      || echo "pdftotext failed on $f, convert manually"
    rm -f "$f.ocr.pdf"
  else
    pandoc "$f" -o "raw/$TARGET/$base.md" \
      && echo "converted: $f -> raw/$TARGET/$base.md" \
      || echo "pandoc failed on $f, convert manually"
  fi

  mv "$f" "raw/inbox/.converted-$base-$(date +%s).$ext"
done
echo "Converted inbox -> raw/$TARGET/"
