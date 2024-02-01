#!/bin/bash

# Ce script permet d'obtenir la segmentation inverse de OASIS sur IBSR
# Les noms possibles à donner sont : IBSR, OASIS, Kirby, IXI

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fixed/seg folder> <moving_fixed/seg_inv folder> <moving/brain folder> <moving_fixed/reg_brain folder>"
    exit 1
fi

input_seg_folder="$1" # moving/seg
output_folder="$2" # moving_fixed/seg_inv
brain_folder="$3" # fixed/brain
brain_reg_folder="$4" # moving_fixed/reg_brain

#nb_file=0
for input_image in "${brain_folder}"/*.nii.gz; do
    fixed_name=$(basename "${input_image}" .nii.gz)
    #echo "${fixed_name}"

    for seg_image in "${input_seg_folder}"/*.nii.gz; do
        seg_name=$(basename "${seg_image}" .nii.gz)
        #echo "${seg_name}"

        moving_reg_name=$(echo "${seg_name}" | sed 's/_seg_ana/_ana/')
        #echo "${moving_reg_name}"
        matrix_name="${fixed_name}0GenericAffine.mat"
        #echo "${matrix_name}"

        output_image="${output_folder}/${moving_reg_name}_seg_${fixed_name}.nii.gz"
        reg_matrix="${brain_reg_folder}/${moving_reg_name}_reg_${matrix_name}"
        #echo "${reg_matrix}"
        #nb_file=$((nb_file + 1))
        
        if [ -e "$output_image" ]; then
            echo "Skipping transformation for $moving_name. Output file already exists: $output_image"
            
        else

            /home/emma/Documents/SIR/script/ANTS/antsApplyTransforms -d 3 \
               -i "${seg_image}" \
               -r "${input_image}" \
               -o "${output_image}" \
               -t "[${reg_matrix}, 0]" \
               --interpolation NearestNeighbor

        echo "Fichier créé : ${output_image}"
        fi
    done
done
#echo "$nb_file"

