""" 

Récuprérer des informations sur une coupe des images résutlantes à partir d'un dossier contenant des images au format nii.gz. :

- Le type de l'image mobile (FLAIR, T1, T2)
- L'image fixe utilisée (IBSR_01, IBSR_02, etc.)
- Les niveaux de gris de la segmentation pour chaque coupe et sur chaque axe (sagittal, coronal, axial)

"""

# --------------------------------------------------------------------------------
# Import

import csv
import sys
import os
import numpy as np
import SimpleITK as sitk

# --------------------------------------------------------------------------------
# Récupérer l'argument

if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

# --------------------------------------------------------------------------------
# Liste des fichiers dans le dossier

inputFiles = [f for f in os.listdir(inputFolder) if f.endswith('.nii.gz')]

# --------------------------------------------------------------------------------
# Traitement de chaque fichier dans le dossier

for inputFile in inputFiles:

    inputFilePath = os.path.join(inputFolder, inputFile)
    image = sitk.ReadImage(inputFilePath)
    size = image.GetSize()

    if "FLAIR" in inputFile:
        typeIRM = "FLAIR"
    elif "OAS" in inputFile:
        typeIRM = "T1"
    elif "T2" in inputFile:
        typeIRM = "T2"
    else:
        typeIRM = "none"

    for i in range(1, 19):
        if i < 10:
            i = "0" + str(i)
        else:
            i = str(i)
        
        if f"IBSR_{i}" in inputFile or f"IBSR_{i}_" in inputFile:
            fixedImagePath = f"/Users/Admin/Documents/4TC/SIR/seg/IBSR_{i}_seg_ana.nii.gz"

    fixedImage = sitk.ReadImage(fixedImagePath)
    arrayFixedImage = sitk.GetArrayFromImage(fixedImage)

    sagittal_len = size[0]
    coronal_len = size[1]
    axial_len = size[2]

    sliceArray = []

    for i in range(coronal_len):
        image_slice = arrayFixedImage[i, :, :]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values, counts))
        sliceArray.append(["Coronal", i, resultats_comptage])

    for i in range(axial_len):
        image_slice = arrayFixedImage[:, i, :]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values, counts))
        sliceArray.append(["Axial", i, resultats_comptage])

    for i in range(sagittal_len):
        image_slice = arrayFixedImage[:, :, i]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values, counts))
        sliceArray.append(["Sagittal", i, resultats_comptage])

        
    # Obtenir le voxel size de l'image
    voxel_size = fixedImage.GetSpacing()

    # Ajouter le voxel size à chaque ligne de sliceArray
    for i in range(len(sliceArray)):
        sliceArray[i].append(voxel_size)

    # Enregistrer au format CSV
    csv_file = os.path.join(inputFolder, f"{inputFile[:-7]}.csv")

    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(sliceArray)

    print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")
