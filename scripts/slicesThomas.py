""" 
Auteur : Thomas
Récuprérer des informations sur une coupe d'une image résutlantes :

- Le type de l'image mobile (FLAIR, T1, T2)
- L'image fixe utilisée (IBSR_01, IBSR_02, etc.)
- Les niveaux de gris de la segmentation pour chaque coupe et sur chaque axe (sagittal, coronal, axial)

"""

# --------------------------------------------------------------------------------
# Import

import sys
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------
# Récupérer l'argument

if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFile>")
    sys.exit(1)

inputFile = sys.argv[1]

# --------------------------------------------------------------------------------
# Lire l'image

image = sitk.ReadImage(inputFile)

# --------------------------------------------------------------------------------
# Informations sur l'image

size = image.GetSize()

if "FLAIR" in inputFile:
    typeIRM = "FLAIR"
elif "OAS" in inputFile:
    typeIRM = "T1"
elif "T2" in inputFile:
    typeIRM = "T2"
else :
    typeIRM = "none"

for i in range(1,19):
    if i < 10:
        i = "0" + str(i)
    else:
        i = str(i)
    if f"IBSR_{i}_" in inputFile:
        fixedImagePath = f"../Data/IBSR_fixed_images/seg/IBSR_{i}_seg_ana.nii.gz"

fixedImage = sitk.ReadImage(fixedImagePath)
arrayFixedImage = sitk.GetArrayFromImage(fixedImage)

# --------------------------------------------------------------------------------
# Afficher informations image
    
print(f"type de l'IRM : {typeIRM}")
print(f"Image fixe : {fixedImagePath}")

# --------------------------------------------------------------------------------
# Afficher informations coupes

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

print(sliceArray)


