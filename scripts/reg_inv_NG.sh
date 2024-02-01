#!/bin/bash

# Ce script permet d'obtenir le recalage inverse en niveau de gris de OASIS (mobile) sur l'IBSR (fixe)

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <fixed_NG_folder> <moving_seg_folder> <moving_fixed_reg_inv_folder> <moving_fixed_reg_brain_folder>"
    exit 1
fi

fixed_NG_folder="$1"
moving_seg_folder="$2"
moving_fixed_reg_inv_folder="$3"
moving_fixed_reg_brain_folder="$4"

mkdir -p "$moving_fixed_reg_inv_folder"

for fixed_file in "$fixed_NG_folder"/*.nii.gz; do
    fixed_NG_name=$(basename "$fixed_file" | sed 's/\.nii\.gz$//')

    for moving_file in "$moving_seg_folder"/*_majority.nii.gz; do
        moving_seg_name=$(basename "$moving_file" | sed -E 's/_majority\.nii\.gz$//')

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



        output_file="$moving_fixed_reg_inv_folder/${fixed_NG_name}_reg_${moving_seg_name}_inv.nii.gz"

	transform_file="$moving_fixed_reg_brain_folder/${moving_seg_name}_reg_${fixed_NG_name}0GenericAffine.mat"

	if [ ! -f "$transform_file" ]; then
	    transform_file="$moving_fixed_reg_brain_folder/${moving_seg_name}_reg_${fixed_NG_name}_brain0GenericAffine.mat"
	fi

        # -t "[$transform_file, 1]" , 1 = inverse
        /home/julie/Software/antsApplyTransforms -d 3 \
            -r "$moving_file" \
            -i "$fixed_file" \
            -o "$output_file" \
            -t "[$transform_file, 1]" \
            --interpolation Linear

        echo "Fichier créé : $output_file"
    done
done