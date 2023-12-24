# source : https://medium.com/@alexandro.ramr777/how-to-do-bias-field-correction-with-python-156b9d51dd79

import SimpleITK as sitk
import time
import os
import argparse

parser = argparse.ArgumentParser(description='Bias Correction')

parser.add_argument('input_dir', type=str, help='The input directory containing the images to be normalised.')
parser.add_argument('output_dir', type=str, help='The output directory containing the normalised images')


start_time = time.time()

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

#input_dir = "/home/julie/Documents/SIR/projet_SIR/data/toNormalise_images"
#output_dir = "/home/julie/Documents/SIR/projet_SIR/data/normalise_images"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".nii"):
        input_path = os.path.join(input_dir, filename)
        raw_img_sitk= sitk.ReadImage(input_path, sitk.sitkFloat32)
        raw_imag_sitk_arr = sitk.GetArrayFromImage(raw_img_sitk)

        # Create a Head Mask
        transformed = sitk.RescaleIntensity(raw_img_sitk, 0, 255)
        transformed = sitk.LiThreshold(transformed,0,1)
        head_mask = transformed

        # Bias Field Correction
        shrinkFactor = 4
        inputImage = raw_img_sitk

        inputImage = sitk.Shrink( raw_img_sitk, [ shrinkFactor] * inputImage.GetDimension() )
        maskImage = sitk.Shrink( head_mask, [ shrinkFactor] * inputImage.GetDimension())

        bias_corrector = sitk.N4BiasFieldCorrectionImageFilter()

        corrected = bias_corrector.Execute( inputImage, maskImage )

        # Get Corrected Image in original Resolution
        log_bias_field = bias_corrector.GetLogBiasFieldAsImage( raw_img_sitk )
        corrected_image_full_resolution = raw_img_sitk / sitk.Exp( log_bias_field)
        final_image = sitk.RescaleIntensity(corrected_image_full_resolution, 0, 255)
        
        #Save the image
        output_filename = "norm_" + filename
        output_path = os.path.join(output_dir, output_filename)
        sitk.WriteImage(final_image, output_path)

end_time = time.time()
print("Temps d execution : ", end_time - start_time)