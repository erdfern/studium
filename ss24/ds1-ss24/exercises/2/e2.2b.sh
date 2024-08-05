#!/usr/bin/env bash
# TODO small display bug: there's an extra '/' after the first directory :(

list_directory_tree() {
  local current_dir="$1"
  local indent="$2"

  for item in "$current_dir"/*; do
    if [ -d "$item" ]; then
        echo "${indent}Directory: $item"
        list_directory_tree "$item" "$indent  " # Recurse into subdirectory, add two spaces to indent
    elif [ -f "$item" ]; then
        echo "${indent}File: $item"
    fi
  done
}

# Validate input and start listing
if [ $# -eq 1 ]; then
  if [ -d "$1" ]; then
    list_directory_tree "$1" "" 
  else
    echo "Error: Invlid directory path provided."
  fi
else
  echo "Usage: $0 [DIR]"
fi
