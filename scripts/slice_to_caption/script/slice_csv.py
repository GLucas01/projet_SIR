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

chemin_output_T1 = "../data/Slice_csv/T1"
if not os.path.exists(chemin_output_T1):
    os.makedirs(chemin_output_T1)

chemin_output_T2 = "../data/Slice_csv/T2"
if not os.path.exists(chemin_output_T2):
    os.makedirs(chemin_output_T2)
    
chemin_output_FL = "../data/Slice_csv/FL"
if not os.path.exists(chemin_output_FL):
    os.makedirs(chemin_output_FL)
    
chemin_output_IBSR = "../data/Slice_csv/IBSR"
if not os.path.exists(chemin_output_IBSR):
    os.makedirs(chemin_output_IBSR)

def getTypeID(inputFile):
    if "FLAIR" in inputFile:
        typeIRM = "FL"

        pattern = re.search(r'KKI2009-(\d+)', inputFile)
        if pattern:
            BD_ID = f"{pattern.group(1)}"

    elif "OAS" in inputFile:
        typeIRM = "T1"

        pattern = re.search(r'OAS1_(\d+)', inputFile)
        if pattern:
            BD_ID = f"{pattern.group(1)}"

    elif "T2" in inputFile:
        typeIRM = "T2"

        pattern = re.search(r'IXI(\d+)', inputFile)
        if pattern:
            BD_ID = f"{pattern.group(1)}"

    else:
        typeIRM = "none"
        BD_ID = "none"
    
    return typeIRM,BD_ID

def getSlicesSeg (inputImage):
    
    arrayImage = inputImage.get_fdata()

    sagittal_len = arrayImage.shape[0]
    coronal_len = arrayImage.shape[1]
    axial_len = arrayImage.shape[2]

    sliceArray = []

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

    for i in range(sagittal_len):
        image_slice = arrayImage[i, :, :]
        unique_values, counts = np.unique(image_slice, return_counts=True)
        resultats_comptage = list(zip(unique_values.astype(int), counts))
        sliceArray.append(["sagittal", i, image_slice.shape, inputImage.header.get_zooms(), resultats_comptage])

    return sliceArray

for inputFile in inputFiles:
    inputFilePath = os.path.join(inputFolder, inputFile)

    if "reg_IBSR" in inputFile :

        for i in range(1, 19):
            if i < 10:
                i = "0" + str(i)
            else:
                i = str(i)
            if f"IBSR_{i}_" in inputFile:
                fixedImagePath = f"../data/IBSR_seg/IBSR_{i}_seg_ana.nii.gz"
                IBSR_ID = f"{i}"

        fixedImage = nib.load(fixedImagePath)
        sliceArray = getSlicesSeg(fixedImage)

        pattern = re.search(r'IBSR_(\d+)_ana_reg_IBSR_(\d+)_ana_norm.nii.gz', inputFile)
        if pattern : 
            csv_file = f"IBSR_{pattern.group(1)}_IBSR_{pattern.group(2)}.csv"
            chemin_csv_sortie = os.path.join(chemin_output_IBSR, csv_file)
        else :
            typeIRM,BD_ID = getTypeID(inputFile)
            csv_file = f"{typeIRM}_{BD_ID}_IBSR_{IBSR_ID}.csv"
            # Chemin vers le fichier CSV de sortie
            if typeIRM == "T1":
                chemin_csv_sortie = os.path.join(chemin_output_T1, csv_file)
            elif typeIRM == "T2":
                chemin_csv_sortie = os.path.join(chemin_output_T2, csv_file)
            else:
                chemin_csv_sortie = os.path.join(chemin_output_FL, csv_file)

        colonnes = ["coupe", "num coupe", "dimensions","voxel", "labels"]
        with open(chemin_csv_sortie, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(colonnes)
        with open(chemin_csv_sortie, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(sliceArray)

        print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")

    elif "seg_IBSR" in inputFile:

        typeIRM,BD_ID = getTypeID(inputFile)
        pattern = re.search(r'IBSR_(\d+)', inputFile)
        if pattern:
            IBSR_ID = f"{pattern.group(1)}"

        image = nib.load(inputFilePath)

        sliceArray = getSlicesSeg(image)

        csv_file = f"IBSR_{IBSR_ID}_{typeIRM}_{BD_ID}.csv"
        # Chemin vers le fichier CSV de sortie
        if typeIRM == "T1":
            chemin_csv_sortie = os.path.join(chemin_output_T1, csv_file)
        elif typeIRM == "T2":
            chemin_csv_sortie = os.path.join(chemin_output_T2, csv_file)
        else:
            chemin_csv_sortie = os.path.join(chemin_output_FL, csv_file)

        colonnes = ["coupe", "num coupe", "dimensions","voxel", "labels"]

        with open(chemin_csv_sortie, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(colonnes)
        with open(chemin_csv_sortie, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(sliceArray)

        print(f"Le fichier {inputFile} a été traité et le CSV a été enregistré dans {csv_file}.")


    elif "majority" in inputFile:
        typeIRM,BD_ID = getTypeID(inputFile)

        image = nib.load(inputFilePath)

        sliceArray = getSlicesSeg(image)

        csv_file = f"{typeIRM}_{BD_ID}_majority.csv"
        # Chemin vers le fichier CSV de sortie
        if typeIRM == "T1":
            chemin_csv_sortie = os.path.join(chemin_output_T1, csv_file)
        elif typeIRM == "T2":
            chemin_csv_sortie = os.path.join(chemin_output_T2, csv_file)
        else:
            chemin_csv_sortie = os.path.join(chemin_output_FL, csv_file)

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