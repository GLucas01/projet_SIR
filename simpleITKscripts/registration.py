"""
 ____                _                  
|  _ \ ___  ___ __ _| | __ _  __ _  ___ 
| |_) / _ \/ __/ _` | |/ _` |/ _` |/ _ \#
|  _ <  __/ (_| (_| | | (_| | (_| |  __/
|_| \_\___|\___\__,_|_|\__,_|\__, |\___|
                             |___/      
Appliquer l'agorithme de recalage fait par elastix (result.mhd) sur une image .nii
"""
# ----------------------------------------------------------------------------------------

import SimpleITK as sitk
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------

# Image d'origine
imagePath =  "IXI dataset/IXI-PD/IXI002-Guys-0828-DUAL_TSES_-s256_-0601-00006-000001-01.nii"
image = sitk.ReadImage(imagePath)
RegistrationImageArray = sitk.GetArrayFromImage(image)

# Image recalée avec elastix
registrationImagePath = "elastix/outputDir/result/result.mhd"
registrationImage = sitk.ReadImage(registrationImagePath)
imageArray = sitk.GetArrayFromImage(registrationImage)

# ----------------------------------------------------------------------------------------

# Afficher les images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(imageArray[100, :, :], cmap="gray")
plt.title("Image d'origine")

plt.subplot(1, 2, 2)
plt.imshow(RegistrationImageArray[100, :, :], cmap="gray")
plt.title("Image recalée")

plt.show()
