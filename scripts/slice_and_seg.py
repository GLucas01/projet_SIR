import nibabel as nib
import sys, os, re

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

def fixPath (Im_fix, ID):
    if Im_fix == "IBSR":
        pathFile = "../data/T1/IBSR/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"IBSR_{ID}" in file:
                fixedPath = os.path.join(pathFile,file)

    elif Im_fix == "IXI":
        pathFile = "../data/T2/IXI/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"IXI{ID}" in file:
                fixedPath = os.path.join(pathFile,file)
        
    elif Im_fix == "OAS":
        pathFile = "../data/T1/OASIS/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"OAS1_{ID}" in file:
                fixedPath = os.path.join(pathFile,file)
        
    elif Im_fix == "KKI":
        pathFile = "../data/FL/Kirby/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"KKI2009-{ID}" in file:
                fixedPath = os.path.join(pathFile,file)
        
    else:
        print("No fixed image found")
        fixedPath = ""
    
    return fixedPath


def findSegIBSR (inputFile, ID_mov, Im_fix, ID_fix):
    fixedPath = ""
    
    #Cas de la transformé inverse
    if "inv" in inputFile:
        pathFile = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"seg_inv")
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"seg_IBSR_{ID_mov}" in file:
                fixedPath = os.path.join(pathFile,file)
    
    #Cas IBSR sur IBSR, segmentation de l'IBSR fixe
    elif Im_fix == "IBSR":
        pathFile = "../data/T1/IBSR/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"IBSR_{ID_fix}" in file:
                fixedPath = os.path.join(pathFile,file)
    
    # Cas du calcul direct de recalage de l'IBSR en image mobile          
    else:
        pathFile = os.path.join(os.path.dirname(os.path.dirname(inputFilePath)),"seg")
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"IBSR_{ID_mov}" in file:
                fixedPath = os.path.join(pathFile,file)
    
    return fixedPath

def getSlices (inputImage, fixedImage):
    
    arrayImage = inputImage.get_fdata()
    segImage = fixedImage.get_fdata()

    sagittal_len = arrayImage.shape[0]
    coronal_len = arrayImage.shape[1]
    axial_len = arrayImage.shape[2]

    
    # sagittal
    image_slice = arrayImage[int(sagittal_len/2), :, :]
    fixedImage_slice = segImage[int(sagittal_len/2), :, :]

    sag_slice = nib.Nifti1Image(image_slice, affine=inputImage.affine)
    sag_seg_slice = nib.Nifti1Image(fixedImage_slice, affine=fixedImage.affine)

    sag_file = f"{file}_sagittal_{int(sagittal_len/2)}.nii.gz"
    sag_seg_file = f"{file}_sagittal_{int(sagittal_len/2)}_seg.nii.gz"

    outputFile = os.path.join(outputPath,sag_file)
    outputFile_seg = os.path.join(outputPath,sag_seg_file)

    nib.save(sag_slice, outputFile)
    nib.save(sag_seg_slice, outputFile_seg)

    # coronal
    image_slice = arrayImage[:, int(coronal_len/2), :]
    fixedImage_slice = segImage[:, int(coronal_len/2), :]
    
    cor_slice = nib.Nifti1Image(image_slice, affine=inputImage.affine)
    cor_seg_slice = nib.Nifti1Image(fixedImage_slice, affine=fixedImage.affine)

    cor_file = f"{file}_coronal_{int(coronal_len/2)}.nii.gz"
    cor_seg_file = f"{file}_coronal_{int(coronal_len/2)}_seg.nii.gz"

    outputFile = os.path.join(outputPath,cor_file)
    outputFile_seg = os.path.join(outputPath,cor_seg_file)

    nib.save(cor_slice, outputFile)
    nib.save(cor_seg_slice, outputFile_seg)

    # axial
    image_slice = arrayImage[:, :, int(axial_len/2)]
    fixedImage_slice = segImage[:, :, int(axial_len/2)]

    ax_slice = nib.Nifti1Image(image_slice, affine=inputImage.affine)
    ax_seg_slice = nib.Nifti1Image(fixedImage_slice, affine=fixedImage.affine)

    ax_file = f"{file}_axial_{int(axial_len/2)}.nii.gz"
    ax_seg_file = f"{file}_axial_{int(axial_len/2)}_seg.nii.gz"

    outputFile = os.path.join(outputPath,ax_file)
    outputFile_seg = os.path.join(outputPath,ax_seg_file)

    nib.save(ax_slice, outputFile)
    nib.save(ax_seg_slice, outputFile_seg)


# Réccupère le chemin du fichiers
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFile>")
    sys.exit(1)

inputFilePath = sys.argv[1]
inputFile = os.path.basename(inputFilePath)

# Extraire les infos du nom
Im_mov, ID_mov, Im_fix, ID_fix= getInfo()
# Nom de sortie
if Im_fix == "":
    file = f"{Im_mov}_{ID_mov}"
else:
    file = f"{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}"

# Chemin du fichier de sortie
outputPath = os.path.join(os.path.dirname(os.path.dirname(inputFilePath)),f"slice_{file}")
if not os.path.exists(outputPath):
    os.makedirs(outputPath) 
 
# Réccupérer la segmentation associée
if Im_mov == "IBSR":
    fixedImagePath = findSegIBSR(inputFile, ID_mov, Im_fix, ID_fix)
if Im_fix == "":
    fixedImagePath = fixPath(Im_mov, ID_mov)
else:
    fixedImagePath = fixPath(Im_fix, ID_fix)


# Création de 3 coupes dans le volume en niveau de gris et la segmentation
getSlices(nib.load(inputFilePath), nib.load(fixedImagePath))
print(f"3 slices and seg created in {outputPath}")