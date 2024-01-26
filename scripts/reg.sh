#!/bin/bas

# Ce script permet de recaler des moving images sur des fixed images, le dossier de sortie est <output_folder>
# Transformation directe, il est préférable d'utiliser des images qui sont skull (cf skull_stripping.sh) que ce soit moving ou fixed 

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <fixed_folder> <moving_folder> <output_folder>"
    exit 1
fi

fixed_folder="$1"
moving_folder="$2"
output_folder="$3"

if [ -d "$fixed_folder" ]; then

    if [ ! -d "$output_folder" ]; then
        mkdir -p "$output_folder"
    fi

    for fixed_image in "$fixed_folder"/*.nii.gz; do
        if [ -f "$fixed_image" ]; then
            fixed_base=$(basename "$fixed_image" .nii.gz)

            for moving_image in "$moving_folder"/*.nii.gz; do
                if [ -f "$moving_image" ]; then
                    moving_base=$(basename "$moving_image" .nii.gz)

                    transform_file="$output_folder/${moving_base}_reg_${fixed_base}"

                    /home/thomas/Desktop/4TC/SIR/Registration_Ants/antsRegistration \
                       --dimensionality 3 \
                       --float 0 \
                       --output ["$transform_file", "$output_folder/${moving_base}_reg_${fixed_base}.nii.gz"] \
                       --interpolation Linear \
                       --use-histogram-matching 0 \
                       --winsorize-image-intensities [0.005,0.995] \
                       --initial-moving-transform ["$fixed_image","$moving_image",1] \
                       --transform Affine[0.1] \
                       --metric MI["$fixed_image","$moving_image",1,32,Regular,0.20] \
                       --convergence [1000x500x250x100,1e-6,20] \
                       --shrink-factors 8x4x2x1 \
                       --smoothing-sigmas 3x2x1x0mm

                    echo "$moving_image registered to $fixed_image completed"
                fi
            done
        fi
    done

else
    echo "Error: $fixed_folder is not a directory"
    exit 1
fi

