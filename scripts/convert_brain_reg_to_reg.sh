#!/bin/bash
# Ce fichier permet à partir d'un dossier /brain_reg, du dossier /NG_mov de la moving image et du dossier /NG_fix de la fixed image, 
# d'obtenir /reg en appliquant la matrice de tranformation (.mat)


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

    moving_image="$NG_mov_folder/${prefix}.nii.gz"
    fixed_image="$NG_fix_folder/${suffix}.nii.gz"
    output_file_name="${prefix}_reg_${suffix}.nii.gz"
    output_file="$reg_folder/$output_file_name"

    # ATTENTION : modifier chemin d'accès à antsApplyTransforms
    /home/julie/Software/antsApplyTransforms \
        -d 3 \
        -i "$moving_image" \
        -r "$fixed_image" \
        -o "$output_file" \
        -t "$transform_file"

    echo "Transformation applied for $moving_image using $transform_file"
    echo "Output file saved as $output_file"
}

for transform_file in "$brain_reg_folder"/*reg*.mat; do
    if [ -f "$transform_file" ]; then
        apply_transform "$transform_file"
    fi
done

echo "All transformations applied successfully."
