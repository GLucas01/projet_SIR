#!/bin/bash

# Définition des chemins
input_dir="IBSR_seg"
output_dir="IXI_seg_IBSR"
dataset_dir="dataset_brain"
reg_dir="dataset_brain_reg"

# Boucle sur les fichiers dans dataset_brain
for input_image in "${dataset_dir}"/*.nii.gz; do
    # Extraire le nom de l'image sans le chemin ni l'extension
    image_name=$(basename "${input_image}" .nii.gz)

    # Initialiser la variable d'itération
    i=1

    # Boucle sur les numéros d'IBSR
    while [ $i -le 18 ]; do
        # Formater le numéro avec un zéro devant s'il est inférieur à 10
        formatted_number=$(printf "%02d" $i)

        output_image="${output_dir}/${image_name}_seg_IBSR_${formatted_number}.nii.gz"
        reg_matrix="${reg_dir}/${image_name}_reg_IBSR_${formatted_number}_ana0GenericAffine.mat"

        # Commande d'enregistrement
        /home/julie/Software/antsApplyTransforms -d 3 \
            -i "${input_dir}/IBSR_${formatted_number}_seg_ana.nii.gz" \
            -r "${input_image}" \
            -o "${output_image}" \
            -t "[${reg_matrix}, 1]" \
            --interpolation NearestNeighbor

        echo "Fichier créé : ${output_image}"

        # Incrémenter la variable d'itération
        i=$((i + 1))
    done
done

