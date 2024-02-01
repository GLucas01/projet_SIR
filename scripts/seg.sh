#!/bin/bash

# Ce script permet d'obtenir la segmentation inverse de OASIS sur IBSR
# Les noms possibles à donner sont : IBSR, OASIS, Kirby, IXI

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fixed/seg folder> <moving_fixed/seg_inv folder> <moving/brain folder> <moving_fixed/reg_brain folder>"
    exit 1
fi

input_seg_folder="$1" # fixed/seg
output_folder="$2" # moving_fixed/seg_inv
brain_folder="$3" # moving/brain
brain_reg_folder="$4" # moving_fixed/reg_brain


for input_image in "${brain_folder}"/*.nii.gz; do
    moving_name=$(basename "${input_image}" .nii.gz)

    for seg_image in "${input_seg_folder}"/*.nii.gz; do
        seg_name=$(basename "${seg_image}")

        fixed_brain_name=$(echo "${seg_name}" | sed 's/_majority.nii.gz/_brain.nii.gz/')
        fixed_matrix_name=$(echo "${seg_name}" | sed 's/_majority.nii.gz/_brain0GenericAffine.mat/')

        output_image="${output_folder}/${moving_name}_seg_${seg_name}"
        reg_matrix="${brain_reg_folder}/${moving_name}_reg_${fixed_matrix_name}"
        
        if [ -e "$output_image" ]; then
            echo "Skipping transformation for $moving_name. Output file already exists: $output_image"
            
        else

            /media/emma/DALLE_BRAIN/SIR/script/ANTS/antsApplyTransforms -d 3 \
               -i "${seg_image}" \
               -r "${input_image}" \
               -o "${output_image}" \
               -t "[${reg_matrix}, 0]" \
               --interpolation NearestNeighbor

        echo "Fichier créé : ${output_image}"
    done
done

