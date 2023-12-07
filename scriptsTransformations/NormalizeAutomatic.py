"""
Normalisation avec Freesurfer
à partir du dossier fixed_images contenant des .nii
Conversion en .mgz puis normalisation
Les fichier normalisés sont enregistrés dans le dossier normalize images

"""

# ------------------------------------------------------------------------------------
# Import

import os
import subprocess

# ------------------------------------------------------------------------------------
# Paramètres

input_folder = "fixed_images"
output_folder = "normalize_images"

os.makedirs(output_folder, exist_ok=True)

input_files = os.listdir(input_folder)

# ------------------------------------------------------------------------------------
# Convertir les .ni en .mgz pour Freesurfer

for input_file in input_files:
    if input_file.endswith(".nii"):

        output_file = input_file.replace('.nii', '.mgz')

        convert_command = f"mri_convert {input_folder}/{input_file} {input_folder}/{output_file}"
        subprocess.run(convert_command, shell=True)

# ------------------------------------------------------------------------------------
# Normaliser les .mgz

for input_file in input_files:
    if input_file.endswith(".mgz"):

        output_file = input_file.replace('.mgz', '_norm.mgz')

        convert_command = f"mri_normalize {input_folder}/{input_file} {output_folder}/{output_file}"
        subprocess.run(convert_command, shell=True)

# ------------------------------------------------------------------------------------
# Revenir en .nii

for input_file in os.listdir(output_folder):
    if input_file.endswith(".mgz"):

        output_file = input_file.replace('.mgz', '.nii')

        convert_command = f"mri_convert {output_folder}/{input_file} {output_folder}/{output_file}"
        subprocess.run(convert_command, shell=True)

print("Traitement terminé !")
