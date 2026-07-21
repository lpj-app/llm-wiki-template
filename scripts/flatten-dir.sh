#!/usr/bin/env bash
# Flattens subdirectories into the top level, skipping .mp4 files.
# Collisions get prefixed with the parent folder name.
# Usage: ./flatten-dir.sh <path>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <path>"
  exit 1
fi

target_dir="$(cd "$1" 2>/dev/null && pwd)" || {
  echo "Error: '$1' is not a valid directory."
  exit 1
}

find "$target_dir" -mindepth 2 -type f ! -iname "*.mp4" -print0 | while IFS= read -r -d '' file; do
  filename="$(basename "$file")"
  parent="$(basename "$(dirname "$file")")"
  dest="$target_dir/$filename"

  if [ -e "$dest" ]; then
    # collision: prefix with parent folder name
    dest="$target_dir/${parent}_${filename}"
    counter=1
    while [ -e "$dest" ]; do
      dest="$target_dir/${parent}_${counter}_${filename}"
      counter=$((counter + 1))
    done
  fi

  mv "$file" "$dest"
  echo "moved: $file -> $dest"
done

# remove now-empty dirs (mp4-containing ones survive)
find "$target_dir" -mindepth 1 -type d -empty -delete

echo "Done. Everything is now flat in $target_dir (mp4 files left untouched in place)."