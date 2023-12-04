"""
 ___ _   _ _____ ___  
|_ _| \ | |  ___/ _ \ 
 | ||  \| | |_ | | | |
 | || |\  |  _|| |_| |
|___|_| \_|_|   \___/ 

Toute les informations sur une image .nii
"""

# Importation
import SimpleITK as sitk

# Charger l'image
image_path = "IXI dataset/IXI-PD/IXI002-Guys-0828-DUAL_TSES_-s256_-0601-00006-000001-01.nii"
flairImage = sitk.ReadImage(image_path)
flairImageArray = sitk.GetArrayFromImage(flairImage)

# taille de l'image
size = flairImage.GetSize()
print("Taille de l'image : ", size, "\n")

# espacement entre les pixels
spacing = flairImage.GetSpacing()
print("Espacement entre les pixels : ", spacing, "\n")

# intensité d'un voxel en x,y,z
intensityVoxel = flairImageArray[100][100][100]
print("Intensité du voxel : ", intensityVoxel, "\n")

# type de pixel 
pixelType = flairImage.GetPixelIDTypeAsString()
print("Type de pixel : ", pixelType, "\n")

# origine de l'image
origin = flairImage.GetOrigin()
print("Origine de l'image : ", origin, "\n")

# matrice de direction
direction = flairImage.GetDirection()
print("Matrice de direction : ")
for j in range(3):
    for i in range(3):
        print(round(direction[i*3+j],1), end='   ')
    print()
print()


metadata_keys = flairImage.GetMetaDataKeys()
for key in metadata_keys:
    print(f"Metadata - {key} : {flairImage.GetMetaData(key)}")





