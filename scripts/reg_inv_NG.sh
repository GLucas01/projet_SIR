#!/bin/bash

# Ce script permet d'effectuer le recalage inverse en niveau de gris 
# en utiliser les fichiers de transformation .mat du dossier /brain_reg
# fixed_NG_folder : dossier contenant les images fixes en niveau de gris du recalage direct
# moving_NG_folder : dossier contenant les images mobiles en niveau de gris du recalage direct
# moving_fixed_reg_brain_folder : dossier contenant les fichiers de transformation .mat du recalage direct
# moving_fixed_reg_inv_folder : dossier de sortie

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fixed_NG_folder> <moving_NG_folder> <moving_fixed_reg_brain_folder> <moving_fixed_reg_inv_folder>"
    exit 1
fi

fixed_NG_folder="$1"
moving_NG_folder="$2"
moving_fixed_reg_brain_folder="$3"
moving_fixed_reg_inv_folder="$4"

apply_transform() {
    local transform_file="$1"
    local moving_image
    local fixed_image
    local output_file_name
    local output_file

    transform_base=$(basename "$transform_file" .mat)

    if echo "$transform_base" | grep -q '_brain_reg_'; then
        suffix=$(echo "$transform_base" | sed 's/.*_brain_reg_\(.*\)_brain0GenericAffine/\1/')
        prefix=$(echo "$transform_base" | sed 's/_brain_reg_.*$//')
    elif echo "$transform_base" | grep -q '_reg_' && ! echo "$transform_base" | grep -q '_brain_reg_'; then
        suffix=$(echo "$transform_base" | sed 's/.*_reg_\(.*\)_brain0GenericAffine/\1/')
        prefix=$(echo "$transform_base" | sed 's/_reg_.*$//')
    else
        echo "Unrecognized naming convention in $transform_file"
        return
    fi

    moving_image="$moving_NG_folder/${prefix}.nii.gz"
    fixed_image="$fixed_NG_folder/${suffix}.nii.gz"
    output_file_name="${suffix}_reg_${prefix}_inv.nii.gz"
    output_file="$moving_fixed_reg_inv_folder/$output_file_name"

    # ATTENTION : modifier chemin d'accès à antsApplyTransforms
    /home/julie/Software/antsApplyTransforms -d 3 \
        -r "$moving_image" \
        -i "$fixed_image" \
        -o "$output_file" \
        -t "[$transform_file, 1]" \ # 1 = inverse
        --interpolation Linear

    echo "Fichier créé : $output_file"
}

for transform_file in "$moving_fixed_reg_brain_folder"/*reg*.mat; do
    if [ -f "$transform_file" ]; then
        apply_transform "$transform_file"
    fi
done

echo "All transformations applied successfully."
