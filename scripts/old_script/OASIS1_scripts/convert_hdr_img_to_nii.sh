#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <chemin_du_dossier>"
    exit 1
fi

dossier="$1"

if [ ! -d "$dossier" ]; then
    echo "Le dossier $dossier n'existe pas."
    exit 1
fi

find "$dossier" -type f -iname "*.hdr" -exec sh -c '
    for fichier; do
        fslchfiletype NIFTI "$fichier"
    done
' sh {} +

echo "Conversion terminée."

