#!/usr/bin/env bash
set -euo pipefail

# Converts raw/inbox/ files to Markdown 
# PDF: via OCR+pdftotext, DOCX/PPTX/ODT
# RTF/HTML: via pandoc, 
# XLSX:  via xlsx-to-md.py
# everything else (images, plain text, etc.) is copied through as-is. 

# Usage: ./scripts/convert-to-md.sh <target-subfolder-under-raw>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:?Usage: convert-to-md.sh <target-subfolder-under-raw>}"
mkdir -p "raw/$TARGET"
total=0
converted=0
failed=()
for f in raw/inbox/*; do
  [ -e "$f" ] || continue
  ext="${f##*.}"
  base="$(basename "${f%.*}")"
  total=$((total+1))
  ok=1

  case "${ext,,}" in
    pdf)
      # --skip-text leaves existing text layers alone, OCRs only scanned pages
      ocrmypdf --skip-text --language deu+eng "$f" "$f.ocr.pdf" 2>/dev/null || cp "$f" "$f.ocr.pdf"
      if pdftotext -layout "$f.ocr.pdf" "raw/$TARGET/$base.md"; then
        echo "converted: $f -> raw/$TARGET/$base.md"
      else
        echo "pdftotext failed on $f, convert manually"
        ok=0
      fi
      rm -f "$f.ocr.pdf"
      ;;
    docx|doc|pptx|ppt|odt|rtf|html|htm)
      if pandoc "$f" -o "raw/$TARGET/$base.md"; then
        echo "converted: $f -> raw/$TARGET/$base.md"
      else
        echo "pandoc failed on $f, convert manually"
        ok=0
      fi
      ;;
    xlsx)
      if python3 "$SCRIPT_DIR/xlsx-to-md.py" "$f" "raw/$TARGET/$base.md"; then
        echo "converted: $f -> raw/$TARGET/$base.md"
      else
        echo "xlsx conversion failed on $f, convert manually"
        ok=0
      fi
      ;;
    *)
      if cp "$f" "raw/$TARGET/$(basename "$f")"; then
        echo "copied: $f -> raw/$TARGET/$(basename "$f")"
      else
        ok=0
      fi
      ;;
  esac

  if [ "$ok" = 1 ]; then
    mv "$f" "raw/inbox/.converted-$base-$(date +%s).$ext"
    converted=$((converted+1))
  else
    failed+=("$(basename "$f")")
  fi
done

echo "Processed inbox -> raw/$TARGET/: $converted/$total files converted"
if [ "${#failed[@]}" -gt 0 ]; then
  echo "Not converted (left in raw/inbox/): ${failed[*]}"
fi
