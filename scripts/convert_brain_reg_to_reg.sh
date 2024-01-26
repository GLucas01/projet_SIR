#!/bin/bash

# Ce fichier permet à partir d'un dossier /brain_reg et du dossier /NG de la moving image, d'obtenir /reg en appliquant la matrice de tranformation (.mat)

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <brain_reg_folder> <reg_folder> <NG_mov_folder> <NG_fix_folder>"
    exit 1
fi

brain_reg_folder="$1"
reg_folder="$2"
NG_mov_folder="$3"
NG_fix_folder="$4"

if [ ! -d "$reg_folder" ]; then
    mkdir -p "$reg_folder"
fi

for transform_file in "$brain_reg_folder"/*_brain_reg_*.mat; do
    if [ -f "$transform_file" ]; then
        transform_base=$(basename "$transform_file" .mat)
        suffix=$(echo "$transform_base" | sed 's/.*_brain_reg_\(.*\)_brain0GenericAffine/\1/')
        prefix=$(echo "$transform_base" | sed 's/_brain_reg_.*$//')
        moving_image="$NG_mov_folder/${prefix}.nii.gz"
        fixed_image="$NG_fix_folder/${suffix}.nii.gz"
        output_file_name="${prefix}_reg_${suffix}.nii.gz"
        output_file="$reg_folder/$output_file_name"

        /home/julie/Software/antsApplyTransforms \
            -d 3 \
            -i "$moving_image" \
            -r "$fixed_image" \
            -o "$output_file" \
            -t "$transform_file"

        echo "Transformation applied for $moving_image using $transform_file"
        echo "Output file saved as $output_file"
    fi
done

echo "All transformations applied successfully."

