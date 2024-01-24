import SimpleITK as sitk
import numpy as np
import os
import csv

# Charger le fichier NII
file_path = '/home/lgirardet/SIR/Seg/IBSR_01_seg_ana.nii'
image = sitk.ReadImage(file_path)


image_array = sitk.GetArrayFromImage(image)


chosen_axis = 'z'  # Remplacez par 'x' ou 'y' selon la coupe 

# Déterminer les positions des coupes 2D
num_slices = 10
if chosen_axis == 'x':
    slice_positions = np.linspace(0, image.GetWidth(), num_slices, endpoint=False, dtype=int)
elif chosen_axis == 'y':
    slice_positions = np.linspace(0, image.GetHeight(), num_slices, endpoint=False, dtype=int)
elif chosen_axis == 'z':
    slice_positions = np.linspace(0, image.GetDepth(), num_slices, endpoint=False, dtype=int)
else:
    raise ValueError("L'axe de coupe choisi doit être 'x', 'y' ou 'z'.")

# Effectuer le comptage pour chaque coupe 2D
for pos in slice_positions:
    if chosen_axis == 'x':
        slice_2d = image_array[:, pos, :]
    elif chosen_axis == 'y':
        slice_2d = image_array[pos, :, :]
    elif chosen_axis == 'z':
        slice_2d = image_array[pos, :, :]

    # Enregistrez la coupe 2D au format NIfTI
    output_folder_slices = 'coupes_2d'
    os.makedirs(output_folder_slices, exist_ok=True)
    output_path_slice = os.path.join(output_folder_slices, f'slice_{chosen_axis}_{pos}.nii')
    sitk.WriteImage(sitk.GetImageFromArray(slice_2d), output_path_slice)
    print(f"La coupe 2D a été enregistrée à : {output_path_slice}")

    # Obtenez les niveaux de gris uniques et les compteurs
    unique_values, counts = np.unique(slice_2d, return_counts=True)

    # Créez un tableau pour stocker les résultats du comptage
    resultats_comptage = list(zip(unique_values, counts))

    # Enregistrez les résultats du comptage dans un fichier CSV
    output_folder_comptage = 'comptage_niveaux_de_gris'
    os.makedirs(output_folder_comptage, exist_ok=True)
    csv_output_path = os.path.join(output_folder_comptage, f'comptage_niveaux_de_gris_{chosen_axis}_{pos}.csv')
    with open(csv_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Écrivez l'en-tête
        writer.writerow(["Niveau de gris", "Nombre de pixels"])
        # Écrivez les données
        for niveau, nombre_pixels in resultats_comptage:
            writer.writerow([niveau, nombre_pixels])

    print(f"Les résultats du comptage pour la coupe {chosen_axis}={pos} ont été enregistrés dans le fichier CSV : {csv_output_path}")
