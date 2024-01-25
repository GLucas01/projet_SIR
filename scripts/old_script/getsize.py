import SimpleITK as sitk
import numpy as np
import nibabel as nib

inputFilePath = "../data/IBSR/IBSR_01_ana.nii.gz"
image = sitk.ReadImage(inputFilePath)
size = image.GetSize()
#print (f"Taille IBSR: {size}\n")

inputFilePath1 = "../data/dataset_brain_reg/IXI035-IOP-0873-T2_brain_reg_IBSR_01_ana.nii.gz"
image1 = sitk.ReadImage(inputFilePath1)
size1 = image1.GetSize()
#print (f"Taille Transformé direct: {size1}\n")

inputFilePath2 = "../data/dataset_brain/IXI035-IOP-0873-T2_brain.nii.gz"
image2 = sitk.ReadImage(inputFilePath2)
size2 = image2.GetSize()
#print (f"Taille IXI: {size2}\n")

inputFilePath3 = "../data/IXI_seg_IBSR/IXI035-IOP-0873-T2_brain_seg_IBSR_01.nii.gz"
image3 = sitk.ReadImage(inputFilePath3)
size3 = image3.GetSize()
print (f"Taille Transformé inverse: {size3}\n")
arrayFixedImage1 = sitk.GetArrayFromImage(image3)
print (f"Taille array Transformé inverse: {arrayFixedImage1.shape}\n")
spacing3 = image3.GetSpacing()
#print(f"Résolution spatiale Transformé inverse: {spacing3}\n")

nifti_img = nib.load(inputFilePath3)
nifti_data = nifti_img.get_fdata()
print (f"Taille nib Transformé inverse: {nifti_data.shape}\n")


inputFilePath4 = "../data/IBSR_seg/IBSR_01_seg_ana.nii.gz"
image4 = sitk.ReadImage(inputFilePath4)
size4 = image4.GetSize()
print (f"Taille IBSR seg: {size4}\n")
arrayFixedImage = sitk.GetArrayFromImage(image4)
print (f"Taille array IBSR seg: {arrayFixedImage.shape}\n")
direction_matrix1 = image4.GetDirection()
#print(f"Matrice de direction IBSR seg :\n{direction_matrix1}")
spacing4 = image4.GetSpacing()
#print(f"Résolution spatiale IBSR seg: {spacing4}\n")

nifti_img1 = nib.load(inputFilePath4)
nifti_data1 = nifti_img1.get_fdata()
print (f"Taille nib IBSR seg: {nifti_data1.shape}\n")

