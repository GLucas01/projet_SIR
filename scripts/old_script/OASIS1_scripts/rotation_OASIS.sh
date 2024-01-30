#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

directory=$1

if [ ! -d "$directory" ]; then
  echo "Error: $directory is not a valid directory."
  exit 1
fi

find "$directory" -type f \( -name "*sbj_111.nii" -o -name "*anon.nii" \) -exec bash -c '
  for file do
    output_file="${file%.*}_rot.nii"
    fslswapdim "$file" z -x y "$output_file"
    echo "Processed: $file -> $output_file"
  done
' bash {} +

find "$directory" -type f -name "*t88_gfc.nii" -exec bash -c '
  for file do
    output_file="${file%.*}_rot.nii"
    fslswapdim "$file" -x -y z "$output_file"
    echo "Processed: $file -> $output_file"
  done
' bash {} +
