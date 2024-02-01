#!/bin/bash

# Ce script permet d'effectuer le recalage inverse en niveau de gris 
# en utiliser les fichiers de transformation .mat du dossier /brain_reg
# fixed_NG_folder : dossier contenant les images fixes en niveau de gris du recalage direct
# moving_NG_folder : dossier contenant les images mobiles en niveau de gris du recalage direct
# moving_fixed_reg_inv_folder : dossier de sortie
# moving_fixed_reg_brain_folder : dossier contenant les fichiers de transformation .mat du recalage direct

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fixed_NG_folder> <moving_seg_folder> <moving_fixed_reg_inv_folder> <moving_fixed_reg_brain_folder>"
    exit 1
fi

fixed_NG_folder="$1"
moving_seg_folder="$2"
moving_fixed_reg_inv_folder="$3"
moving_fixed_reg_brain_folder="$4"

# crée le dossier de sortie s'il n'existe pas encore.
mkdir -p "$moving_fixed_reg_inv_folder"

# Parcours chaque image fixe dans le dossier fixed_NG_folder.
for fixed_file in "$fixed_NG_folder"/*.nii.gz; do
    fixed_NG_name=$(basename "$fixed_file" | sed 's/\.nii\.gz$//')

    # Parcours chaque image mobile dans le dossier moving_seg_folder.
    for moving_file in "$moving_seg_folder"/*_majority.nii.gz; do
        moving_seg_name=$(basename "$moving_file" | sed -E 's/_majority\.nii\.gz$//')

        # Réorganise les noms d'image mobile pour correspondre aux noms du dossier brain_reg.
        if [[ "$moving_seg_name" == OAS1* ]]; then
            id_moving=$(echo "$moving_seg_name" | cut -d '_' -f 2)
            moving_seg_name="OAS1_${id_moving}_MR1_mpr-1_anon_rot_brain"
        elif [[ "$moving_seg_name" == KKI2009* ]]; then
            id_moving=$(echo "$moving_seg_name" | cut -d '-' -f 2)
            moving_seg_name="KKI2009-${id_moving}-FLAIR_brain"
        elif [[ "$moving_seg_name" == IBSR* ]]; then
            id_moving=$(echo "$moving_seg_name" | cut -d '_' -f 2)
            moving_seg_name="IBSR_${id_moving}_ana"
	    elif [[ "$moving_seg_name" == IXI* ]]; then
            id_moving=$(echo "$moving_seg_name" | cut -d '-' -f 1-4)
            moving_seg_name="${id_moving}"
        fi

        # Construit le chemin du fichier de sortie pour le recalage inverse.
        output_file="$moving_fixed_reg_inv_folder/${fixed_NG_name}_reg_${moving_seg_name}_inv.nii.gz"

        # Construit le chemin du fichier de transformation pour le recalage direct.
	    transform_file="$moving_fixed_reg_brain_folder/${moving_seg_name}_reg_${fixed_NG_name}0GenericAffine.mat"

        # Si le fichier de transformation n'existe pas avec le suffixe 0GenericAffine, essaye avec le suffixe _brain0GenericAffine.
        if [ ! -f "$transform_file" ]; then
            transform_file="$moving_fixed_reg_brain_folder/${moving_seg_name}_reg_${fixed_NG_name}_brain0GenericAffine.mat"
        fi

        # Vérifie si le fichier de sortie existe déjà
        if [ -e "$output_file" ]; then
            echo "Skipping transformation for $fixed_file to $moving_file. Output file already exists: $output_file"
        else
            # Applique la transformation inverse.
            # -t "[$transform_file, 1]" , 1 = inverse
            /home/julie/Software/antsApplyTransforms -d 3 \
                -r "$moving_file" \
                -i "$fixed_file" \
                -o "$output_file" \
                -t "[$transform_file, 1]" \
                --interpolation Linear

            echo "Fichier créé : $output_file"
        fi
    done
done