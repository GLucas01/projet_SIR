import SimpleITK as sitk

def calculate_mutual_information(img1_path, img2_path):
    img1 = sitk.ReadImage(img1_path, sitk.sitkFloat32)
    img2 = sitk.ReadImage(img2_path, sitk.sitkFloat32)

    registration_method = sitk.ImageRegistrationMethod()

    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=64)

    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
    registration_method.SetInterpolator(sitk.sitkLinear)

    mutual_information = registration_method.MetricEvaluate(img1, img2)
    return mutual_information

img1_path = '/media/julie/KINGSTON/SIR/projet_SIR/data/IBSR/skull_stripped/IBSR_07_ana.nii.gz'
img2_path = '/media/julie/KINGSTON/SIR/projet_SIR/data/T1/registred_me/OAS1_0001_MR1_mpr_n4_anon_111_t88_gfc_reg_IBSR_07_ana.nii.gz'

mutual_info_value = calculate_mutual_information(img1_path, img2_path)
print(img1_path)
print(f"Mutual information: {mutual_info_value}")

