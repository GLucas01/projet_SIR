import nibabel as nib
import numpy as np

# Load the NIfTI file
nifti_file_path_seg = "../data/IBSR_seg/IBSR_01_seg_ana.nii.gz"
nifti_img_seg = nib.load(nifti_file_path_seg)

nifti_file_path = "../data/dataset_brain_reg/IXI035-IOP-0873-T2_brain_reg_IBSR_01_ana.nii.gz"
nifti_img = nib.load(nifti_file_path)

# Get the NIfTI data array
nifti_data_seg = nifti_img_seg.get_fdata()
slice_data_seg = nifti_data_seg[int(nifti_data_seg.shape[0]/2), :, :] # sagittal plane
new_nifti_img_seg = nib.Nifti1Image(slice_data_seg, affine=nifti_img_seg.affine)
output_nifti_path_seg = 'sagittal_slice_seg.nii.gz'
nib.save(new_nifti_img_seg, output_nifti_path_seg)
print(nifti_img_seg.header.get_zooms())

nifti_data = nifti_img.get_fdata()
slice_data = nifti_data[int(nifti_data.shape[0]/2), :, :] # sagittal plane
new_nifti_img = nib.Nifti1Image(slice_data, affine=nifti_img.affine)
output_nifti_path = 'sagittal_slice.nii.gz'
nib.save(new_nifti_img, output_nifti_path)
print(nifti_img.header.get_zooms())


# for slice_index in range(nifti_data.shape[0]):
#     # Extract the 2D slice from the 3D volume
#     slice_data = nifti_data[slice_index, :, :] # sagittal plane

#     # Create a new NIfTI image with the extracted slice
#     new_nifti_img = nib.Nifti1Image(slice_data, affine=nifti_img.affine)

#     # Save the new NIfTI image
#     output_nifti_path = f'sagittal_slice_{slice_index}.nii.gz'
#     nib.save(new_nifti_img, output_nifti_path)

#     # Print unique values in the segment of the extracted slice
#     unique_values = np.unique(slice_data)
#     #print("Unique values in the segment of the slice:")
#     #print(unique_values)

# for slice_index in range(nifti_data.shape[1]):
#     # Extract the 2D slice from the 3D volume
#     slice_data = nifti_data[:, slice_index, :] # coronal plane

#     # Create a new NIfTI image with the extracted slice
#     new_nifti_img = nib.Nifti1Image(slice_data, affine=nifti_img.affine)

#     # Save the new NIfTI image
#     output_nifti_path = f'coronal_slice_{slice_index}.nii.gz'
#     #nib.save(new_nifti_img, output_nifti_path)

#     # Print unique values in the segment of the extracted slice
#     unique_values = np.unique(slice_data)
#     #print("Unique values in the segment of the slice:")
#     #print(unique_values)

# for slice_index in range(nifti_data.shape[2]):
#     # Extract the 2D slice from the 3D volume
#     slice_data = nifti_data[:, :, slice_index] # axial plane

#     # Create a new NIfTI image with the extracted slice
#     new_nifti_img = nib.Nifti1Image(slice_data, affine=nifti_img.affine)

#     # Save the new NIfTI image
#     output_nifti_path = f'axial_slice_{slice_index}.nii.gz'
#     #nib.save(new_nifti_img, output_nifti_path)

#     # Print unique values in the segment of the extracted slice
#     unique_values = np.unique(slice_data)
#     #print("Unique values in the segment of the slice:")
#     #print(unique_values)