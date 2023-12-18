#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dossier>"
    exit 1
fi

dossier="$1"

if [ ! -d "$dossier" ]; then
    echo "Erreur: '$dossier' n'est pas un dossier valide."
    exit 1
fi

while IFS= read -r -d '' fichier; do
    echo "Traitement du fichier : $fichier"

    mri_convert "$fichier" "${fichier%.*}_norm.mgz"
    mri_nu_correct.mni --i "${fichier%.*}_norm.mgz" --o "${fichier%.*}_norm.mgz" --n 2
    mri_normalize -g 1 -mprage "${fichier%.*}_norm.mgz" "${fichier%.*}_norm.mgz"
    mri_convert "${fichier%.*}_norm.mgz" "${fichier%.*}_norm.nii"
done < <(find "$dossier" -type f -name "*IBSR_01_ana.nii.gz" -print0)

