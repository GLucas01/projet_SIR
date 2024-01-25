#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <dataset_brain_reg_folder> <dataset_folder> <dataset_reg_folder>"
    exit 1
fi

brain_reg_folder="$1"
dataset_folder="$2"
dataset_reg_folder="$3"

if [ ! -d "$dataset_reg_folder" ]; then
    mkdir -p "$dataset_reg_folder"
fi

for transform_file in "$brain_reg_folder"/*_brain_reg_*.mat; do
    if [ -f "$transform_file" ]; then
        transform_base=$(basename "$transform_file" .mat)
        id_IBSR=$(echo "$transform_file" | sed -n 's/.*_brain_reg_IBSR_\([0-9]\+\)_ana0GenericAffine\.mat/\1/p')
        prefix=$(echo "$transform_base" | sed 's/_brain_reg_.*$//')
        moving_image="$dataset_folder/${prefix}.nii.gz"
        fixed_image="IBSR/IBSR_${id_IBSR}_ana.nii.gz"
        output_file_name="${prefix}_reg_$(basename "$fixed_image" .nii.gz).nii.gz"
        output_file="$dataset_reg_folder/$output_file_name"

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

