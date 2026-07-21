#!/usr/bin/env bash
# Restores .converted-* files to visible names with extension detected
# via file magic bytes (the original extension was lost on hide).
# Usage: ./revert-converted.sh [path]   (defaults to raw/inbox)
set -euo pipefail

target_dir="${1:-raw/inbox}"
target_dir="$(cd "$target_dir" 2>/dev/null && pwd)" || {
  echo "Error: '$target_dir' is not a valid directory."
  exit 1
}

shopt -s nullglob
found=0

for f in "$target_dir"/.converted-*; do
  [ -f "$f" ] || continue
  found=1
  fname="$(basename "$f")"

  # Parse: .converted-<base>-<epoch-timestamp>[.ext]
  if [[ "$fname" =~ ^\.converted-(.+)-([0-9]{10,})\.([a-zA-Z0-9]+)$ ]]; then
    base="${BASH_REMATCH[1]}"
    ext="${BASH_REMATCH[3]}"
  elif [[ "$fname" =~ ^\.converted-(.+)-([0-9]{10,})$ ]]; then
    base="${BASH_REMATCH[1]}"
    # older hides had no extension — detect real type via magic bytes
    mime="$(file --mime-type -b "$f")"
    case "$mime" in
      application/pdf) ext="pdf" ;;
      image/jpeg) ext="jpg" ;;
      image/png) ext="png" ;;
      text/plain) ext="txt" ;;
      application/vnd.openxmlformats-officedocument.wordprocessingml.document) ext="docx" ;;
      application/vnd.openxmlformats-officedocument.presentationml.presentation) ext="pptx" ;;
      *)
        echo "warning: unrecognized type ($mime) for $fname, restoring without extension"
        ext=""
        ;;
    esac
  else
    echo "skip (unexpected name pattern): $fname"
    continue
  fi

  dest="$target_dir/$base"
  [ -n "$ext" ] && dest="$dest.$ext"

  if [ -e "$dest" ]; then
    echo "skip (target already exists): $dest"
    continue
  fi

  mv "$f" "$dest"
  echo "restored: $fname -> $dest"
done

[ "$found" -eq 0 ] && echo "No .converted-* files found in $target_dir"