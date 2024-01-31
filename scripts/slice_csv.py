import csv
import sys
import os
import re
import numpy as np
import nibabel as nib

# Vérification du nombre d'arguments de la ligne de commande
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

# Récupération du chemin du dossier d'entrée et création d'un dossier de sortie pour les fichiers CSV
inputFiles = [f for f in os.listdir(inputFolder) if f.endswith('.nii.gz')]
if inputFolder.endswith("inv"):
    chemin_output = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Slice_csv_inv")
else:
    chemin_output = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Slice_csv")
if not os.path.exists(chemin_output):
    os.makedirs(chemin_output)

# Fonction pour extraire des informations sur les images fixe et mobile à partir du nom du fichier
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

# Fonction pour récupérer le chemin du fichier image fixe en fonction de la base de donnee et de l'ID
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

# Fonction pour trouver le chemin du fichier segmentation pour le cas spécifique de l'IBSR
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
        pathFile = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"seg")
        files = [f for f in os.listdir(pathFile) if f.endswith('.nii.gz')]
        for file in files:
            if f"seg_IBSR_{ID_mov}" in file:
                fixedPath = os.path.join(pathFile,file)
    
    return fixedPath

# Fonction pour obtenir des informations sur les coupes à partir de la segmentation de l'image fixe
def getSlicesSeg (inputImage):
    
    arrayImage = inputImage.get_fdata()

    sagittal_len = arrayImage.shape[0]
    coronal_len = arrayImage.shape[1]
    axial_len = arrayImage.shape[2]

    sliceArray = []
    
    for i in range(sagittal_len):
        image_slice = arrayImage[i, :, :]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["sagittal", i, image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])


    for i in range(coronal_len):
        image_slice = arrayImage[:, i, :]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["coronal",i,image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])

    for i in range(axial_len):
        image_slice = arrayImage[:, :, i]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["axial", i, image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])

    return sliceArray

# Boucle principale pour traiter chaque fichier dans le dossier d'entrée
for inputFile in inputFiles:
    inputFilePath = os.path.join(inputFolder, inputFile)
    
    # Vérification du type de fichier (reg, majority, seg)
    if "reg" in inputFile :

        Im_mov, ID_mov, Im_fix, ID_fix = getInfo(inputFile)

        # Cas particulier IBSR est l'image mouvante 
        if Im_mov == "IBSR":
            fixedImagePath = findSegIBSR(inputFile, ID_mov, Im_fix, ID_fix)
        else :
            fixedImagePath = fixPath(Im_fix, ID_fix)

        fixedImage = nib.load(fixedImagePath)
        sliceArray = getSlicesSeg(fixedImage)
        
        # Création du fichier CSV
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
        
    # Cas particulier des segmentations obtenue via le majority voting
    elif "majority" in inputFile:
        
        Im_mov,ID_mov, Im_fix, ID_fix= getInfo(inputFile)
        
        image = nib.load(inputFilePath)
        sliceArray = getSlicesSeg(image)
        
        # Création du fichier CSV
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
        
        # Création du fichier CSV
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