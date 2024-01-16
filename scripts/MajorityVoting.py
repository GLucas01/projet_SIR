import SimpleITK as sitk

img1 = sitk.ReadImage('/media/julie/KINGSTON/SIR/projet_SIR/data/IBSR/skull_stripped/IBSR_01_ana.nii.gz', sitk.sitkFloat32)
img2 = sitk.ReadImage('/media/julie/KINGSTON/SIR/projet_SIR/data/IBSR/skull_stripped/IBSR_02_ana.nii.gz', sitk.sitkFloat32)
img3 = sitk.ReadImage('/media/julie/KINGSTON/SIR/projet_SIR/data/IBSR/skull_stripped/IBSR_03_ana.nii.gz', sitk.sitkFloat32)
img1 = sitk.Cast(img1, sitk.sitkUInt8)
img2 = sitk.Cast(img2, sitk.sitkUInt8)
img3 = sitk.Cast(img3, sitk.sitkUInt8)


label_voting_filter = sitk.LabelVotingImageFilter()

label_voting_filter.SetLabelForUndecidedPixels(0)
result_image = label_voting_filter.Execute(img1, img2, img3)

sitk.WriteImage(result_image, '/media/julie/KINGSTON/SIR/projet_SIR/data/IBSR/skull_stripped/result_image.nii.gz')