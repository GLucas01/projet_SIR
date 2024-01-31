#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <dossier>"
    exit 1
fi

dossier=$1

if [ ! -d "$dossier" ]; then
    echo "Le dossier spécifié n'existe pas."
    exit 1
fi

for fichier in "$dossier"/*; do
    if [[ "$fichier" == *.nii.gz ]]; then
        echo "Suppression du fichier $fichier"
        rm "$fichier"
    fi
done

echo "Opération terminée."

