''''
 _   _                            _ _           _   _             
| \ | | ___  _ __ _ __ ___   __ _| (_)___  __ _| |_(_) ___  _ __  
|  \| |/ _ \| '__| '_ ` _ \ / _` | | / __|/ _` | __| |/ _ \| '_ \ 
| |\  | (_) | |  | | | | | | (_| | | \__ \ (_| | |_| | (_) | | | |
|_| \_|\___/|_|  |_| |_| |_|\__,_|_|_|___/\__,_|\__|_|\___/|_| |_|

Utilisation de l'algorithme de correction de bias pour la normalisation
                                                                  
'''

# ----------------------------------------------------------------------------------------

import time
import SimpleITK as sitk
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------

starttime = time.time()

# Charger l'image
image_path = "IXI dataset/IXI-PD/IXI002-Guys-0828-DUAL_TSES_-s256_-0601-00006-000001-01.nii"
flairImage = sitk.ReadImage(image_path, sitk.sitkFloat32)

# Filtre de morphologie binaire d'ouverture (érosion + dilatation)
openingFilter = sitk.BinaryMorphologicalOpeningImageFilter()
openingFilter.SetKernelRadius(4)
openingFilter.SetKernelType(sitk.sitkBall)

# Masque avec ouverture
maskImage = sitk.OtsuThreshold(flairImage, 0, 1, 50) # paramètre modifiable
openedMaskImage = openingFilter.Execute(maskImage)

#Correcteur de biais
corrector = sitk.N4BiasFieldCorrectionImageFilter()
corrector.SetMaximumNumberOfIterations([10]*4) # paramètre modifiable
corrector.SetConvergenceThreshold(1e-3) # paramètre modifiable
flairImageCorrected = corrector.Execute(flairImage, openedMaskImage)

# ----------------------------------------------------------------------------------------

# Afficher l'image d'origine
plt.figure(figsize=(8, 4))
plt.subplot(1, 3, 1)
plt.imshow(sitk.GetArrayFromImage(flairImage)[100, :, :], cmap='gray')
plt.title('Image d\'origine')
plt.axis('off')

# # Afficher l'image corrigée
plt.subplot(1, 3, 3)
plt.imshow(sitk.GetArrayFromImage(flairImageCorrected)[100, :, :], cmap='gray')
plt.title('Image corrigée')
plt.axis('off')

# Afficher la différence entre les deux images
plt.subplot(1, 3, 2)
plt.imshow(sitk.GetArrayFromImage(flairImageCorrected)[100, :, :] - sitk.GetArrayFromImage(flairImage)[100, :, :], cmap='gray')
plt.title('Différence')
plt.axis('off')

# Afficher le temps d'exécution minututes:secondes
print("Temps d'exécution : %d:%d" % (int((time.time() - starttime) / 60), int((time.time() - starttime) % 60)))

plt.show()