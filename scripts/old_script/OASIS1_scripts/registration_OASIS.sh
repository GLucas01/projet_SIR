#!/bin/bash

# Il faut installer ANTs sur son pc pour le lancer

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <fixed_image> <moving_folder>"
    exit 1
fi

fixed_image="$1"
moving_image_or_folder="$2"
output_prefix="$1"

fixed_base=$(basename "$fixed_image" .nii)

if [ -d "$moving_image_or_folder" ]; then
    find "$moving_image_or_folder" -type f -name '*_rot.nii.gz' | while read -r moving_image; do
        if [ -f "$moving_image" ]; then
            moving_base=$(basename "$moving_image" _rot.nii.gz)

            output_folder=$(dirname "$moving_image")
            output_folder="${output_folder}/output"

            if [ ! -d "$output_folder" ]; then
                mkdir -p "$output_folder"
            fi

            /chemin_vers_fichier/ants/antsRegistration \
               --dimensionality 3 \
               --float 0 \
               --output ["output/matrices/output","$(dirname "$moving_image")/${moving_base}_reg_${fixed_base}.nii.gz"] \
               --interpolation Linear \
               --use-histogram-matching 0 \
               --winsorize-image-intensities [0.005,0.995] \
               --initial-moving-transform ["$fixed_image","$moving_image",1] \
               --transform Affine[0.1] \
               --metric MI["$fixed_image","$moving_image",1,32,Regular,0.20] \
               --convergence [1000x500x250x100,1e-6,20] \
               --shrink-factors 8x4x2x1 \
               --smoothing-sigmas 3x2x1x0mm

            echo "$moving_image recalé sur $fixed_image terminé"
        fi
    done
else
    echo "Error: $moving_image_or_folder is not a valid directory."
    exit 1
fi
