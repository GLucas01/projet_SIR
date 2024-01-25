import csv
import sys
import os
import re
import numpy as np
import nibabel as nib

if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

inputFiles = [f for f in os.listdir(inputFolder) if f.endswith('.nii.gz')]

chemin_output = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Slice_csv_after_slicer")
if not os.path.exists(chemin_output):
    os.makedirs(chemin_output)


def getInfo(inputFile):
    
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
        pathFile = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"seg_inverse")
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"seg_IBSR_{ID_mov}" in file:
                fixedPath = os.path.join(pathFile,file)
    #Cas IBSR sur IBSR, segmentation de l'IBSR fix
    elif Im_fix == "IBSR":
        pathFile = "../data/T1/IBSR/seg"
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"IBSR_{ID_fix}" in file:
                fixedPath = os.path.join(pathFile,file)
        
    ##ATENTION
    #Autres cas non pris en compte pour le moment
    
    return fixedPath

def getSlicesSeg (inputImage):
    
    sagittal_len = inputImage.shape[0]
    coronal_len = inputImage.shape[1]
    axial_len = inputImage.shape[2]

    sliceArray = []
    
    for i in range(sagittal_len):
        image_slice = inputImage.slicer[i:i+1, :, :]
        unique_values, counts = np.unique(image_slice.get_fdata(), return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["sagittal", i, image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])


    for i in range(coronal_len):
        image_slice = inputImage.slicer[:, i:i+1, :]
        unique_values, counts = np.unique(image_slice.get_fdata(), return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["coronal",i,image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])

    for i in range(axial_len):
        image_slice = inputImage.slicer[:, :, i:i+1]
        unique_values, counts = np.unique(image_slice.get_fdata(), return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["axial", i, image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])

    return sliceArray

for inputFile in inputFiles:
    inputFilePath = os.path.join(inputFolder, inputFile)

    if "reg" in inputFile :

        Im_mov, ID_mov, Im_fix, ID_fix = getInfo(inputFile)
        #print (Im_mov, ID_mov, Im_fix, ID_fix)
        #cas particulier IBSR est l'image mouvante 
        if Im_mov == "IBSR":
            fixedImagePath = findSegIBSR(inputFile, ID_mov, Im_fix, ID_fix)
        else :
            fixedImagePath = fixPath(Im_fix, ID_fix)
        #print(fixedImagePath)
        fixedImage = nib.load(fixedImagePath)
        sliceArray = getSlicesSeg(fixedImage)

        csv_file = f"{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}.csv"
        chemin_csv_sortie = os.path.join(chemin_output, csv_file)

        colonnes = ["coupe", "num coupe", "dimensions","voxel", "labels"]
        with open(chemin_csv_sortie, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(colonnes)
        with open(chemin_csv_sortie, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(sliceArray)

        print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")

    elif "majority" in inputFile:
        
        Im_mov,ID_mov, Im_fix, ID_fix= getInfo(inputFile)
        image = nib.load(inputFilePath)
        sliceArray = getSlicesSeg(image)

        csv_file = f"{Im_mov}_{ID_mov}_majority.csv"
        chemin_csv_sortie = os.path.join(chemin_output, csv_file)

        colonnes = ["coupe", "num coupe", "dimensions","voxel", "labels"]
        with open(chemin_csv_sortie, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(colonnes)
        with open(chemin_csv_sortie, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(sliceArray)

        print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")
    
    #Cas particulier de la segmentation des IBSR  
    elif "seg" in inputFile:
        
        Im_mov,ID_mov, Im_fix, ID_fix= getInfo(inputFile)
        image = nib.load(inputFilePath)
        sliceArray = getSlicesSeg(image)

        csv_file = f"{Im_mov}_{ID_mov}_seg.csv"
        chemin_csv_sortie = os.path.join(chemin_output, csv_file)

        colonnes = ["coupe", "num coupe", "dimensions","voxel", "labels"]
        with open(chemin_csv_sortie, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(colonnes)
        with open(chemin_csv_sortie, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(sliceArray)

        print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")
    
    else:
        print("Le fichier n'est pas valide.")