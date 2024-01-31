import nibabel as nib
import sys, os, re, random

def getInfo():
    
    #Im_fix
    ID_fix = ""
    Im_fix = ""
    pattern_fix = re.search(r'reg_KKI2009-(\d+)', inputFile)
    if pattern_fix:
        ID_fix = f"{pattern_fix.group(1)}"
        Im_fix = "KKI"


    pattern_fix = re.search(r'reg_OAS1_(\d+)', inputFile)
    if pattern_fix:
        ID_fix = f"{pattern_fix.group(1)}"
        Im_fix = "OAS"


    pattern_fix = re.search(r'reg_IXI(\d+)', inputFile)
    if pattern_fix:
        ID_fix = f"{pattern_fix.group(1)}"
        Im_fix = "IXI"
        
        
    pattern_fix = re.search(r'reg_IBSR_(\d+)', inputFile)
    if pattern_fix:
        ID_fix = f"{pattern_fix.group(1)}"
        Im_fix = "IBSR"
    
    #Im_mov
    ID_mov = ""
    Im_mov = ""
    pattern_mov = re.search(r'^KKI2009-(\d+)', inputFile)
    if pattern_mov:
        ID_mov = f"{pattern_mov.group(1)}"
        Im_mov = "KKI"


    pattern_mov = re.search(r'^OAS1_(\d+)', inputFile)
    if pattern_mov:
        ID_mov = f"{pattern_mov.group(1)}"
        Im_mov = "OAS"


    pattern_mov = re.search(r'^IXI(\d+)', inputFile)
    if pattern_mov:
        ID_mov = f"{pattern_mov.group(1)}"
        Im_mov = "IXI"
        
        
    pattern_mov = re.search(r'^IBSR_(\d+)', inputFile)
    if pattern_mov:
        ID_mov = f"{pattern_mov.group(1)}"
        Im_mov = "IBSR"
              
    return Im_mov, ID_mov, Im_fix, ID_fix
  
def getSlices ():
    arrayImage = image.get_fdata()

    sagittal_len = arrayImage.shape[0]
    coronal_len = arrayImage.shape[1]
    axial_len = arrayImage.shape[2]
    
    for i in range(sagittal_len):
        image_slice = arrayImage[i, :, :]
        nifti_slice = nib.Nifti1Image(image_slice, affine=image.affine)
        slice_file = f"{file}_sagittal_{i}.nii.gz"
        outputFile = os.path.join(outputPath,slice_file)
        nib.save(nifti_slice, outputFile)

    for i in range(coronal_len):
        image_slice = arrayImage[:, i, :]
        nifti_slice = nib.Nifti1Image(image_slice, affine=image.affine)
        slice_file = f"{file}_coronal_{i}.nii.gz"
        outputFile = os.path.join(outputPath,slice_file)
        nib.save(nifti_slice, outputFile)
        
    for i in range(axial_len):
        image_slice = arrayImage[:, :, i]
        nifti_slice = nib.Nifti1Image(image_slice, affine=image.affine)
        slice_file = f"{file}_axial_{i}.nii.gz"
        outputFile = os.path.join(outputPath,slice_file)
        nib.save(nifti_slice, outputFile)


if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFile>")
    sys.exit(1)

inputFile = sys.argv[1]

Im_mov, ID_mov, Im_fix, ID_fix= getInfo()
# Name output:
if "reg" in inputFile :
    file = f"{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}"
elif "majority" in inputFile:
    file = f"{Im_mov}_{ID_mov}_majority"
elif "seg" in inputFile:
    file = f"{Im_mov}_{ID_mov}_seg"
else :
    print("Le fichier n'est pas valide.")
    
outputPath = os.path.join(os.path.sep.join(inputFile.split(os.path.sep)[:-1]),"slice_NG_{file}")
if not os.path.exists(outputPath):
    os.makedirs(outputPath)    

# Load image
image = nib.load(inputFile)

# Get slices
getSlices()

