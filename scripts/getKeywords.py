import csv
import ast
import os
import sys
import re

# Chemin vers les fichiers info.csv
infoPath = "../data/Keywords"

# Chemin vers dossiers contenant les fichiers csv des coupes
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

inputFiles = [f for f in os.listdir(inputFolder) if f.endswith('csv')]

outputPath = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Keywords")
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

def extract_info(Im, ID):
    ID = int(ID)
    # Conserver les zéros en tête en convertissant l'ID en chaîne pour la BD OASIS
    if Im == 'OAS':
        ID = str(ID).zfill(4)
    else:
        ID = str(ID)

    # Choisir le bon fichier CSV en fonction de la BD
    if Im == 'OAS':
        infoFilePath = os.path.join(infoPath, 'OASIS_info.csv')
    elif Im == 'IXI':
        infoFilePath = os.path.join(infoPath, 'IXI_info.csv')
    elif Im == 'KKI':
        infoFilePath = os.path.join(infoPath, 'Kirby_info.csv')
    elif Im == 'IBSR':
        infoFilePath = os.path.join(infoPath, 'Atlas_info.csv')
    else:
        print(f"Infos about {Im} not found")

    # Ouvrir le fichier CSV
    with open(infoFilePath, 'r', newline='', encoding='utf-8') as fichier_infos:
        # Créer un lecteur CSV avec des dictionnaires pour accéder aux données par nom de colonne
        reader = csv.DictReader(fichier_infos)
        genre, age = "",""
        # Parcourir chaque ligne du CSV
        for ligne in reader:
            # Si l'ID de la ligne correspond à l'ID recherché
            if ligne['ID'] == ID:
                # Extraire l'âge et le genre
                age = ligne['AGE']
                genre = ligne['GENDER']

        return genre,age

def getModalite (Im):
    if Im == 'OAS':
        return "T1"
    elif Im == 'IXI':
        return "T2"
    elif Im == 'KKI':
        return "FL"
    elif Im == 'IBSR':
        return "T1"
    else:
        print(f"Modalite about {Im} not found")
        return ""

# Fonction pour extraire les données du nom du fichier
def extract_data_in_name(inputFile):
    # Supprimer l'extension .csv du nom du fichier
    fileName = os.path.splitext(inputFile)[0]
    # chemin vers le fichier
    inputPath = os.path.join(inputFolder,inputFile)

    # Diviser le nom en parties en utilisant '_' comme séparateur
    part = fileName.split('_')

    # Extraire les données nécessaires
    modalite = getModalite(part[0])
    genre_mov, age_mov = extract_info(part[0],part[1])
    if len(part)>3:
        genre_fix, age_fix = extract_info(part[2],part[3])
    else :
        genre_fix, age_fix = "",""
        
    with open(inputPath, 'r') as f:
        reader = csv.DictReader(f)
        # Extraire les valeurs de Sx, Sy et Sz
        voxel = next(reader)['voxel']
        Sx, Sy, Sz = map(float, voxel.strip('()').split(',')[:3])
   
    # Retourner une liste avec les données extraites
    return [modalite, genre_mov, age_mov,genre_fix,age_fix, Sx, Sy, Sz]



def modifier_id_par_labels(inputPath, anaPath, outputPath_coupes, Sx, Sy, Sz):
    # Noms des colonnes
    colonnes = ["coupe", "num coupe", "dimensions", "labels"]

    # Lire le fichier d'anatomie et créer un dictionnaire de correspondances
    correspondances = {}
    with open(anaPath, mode='r', newline='', encoding='utf-8') as fichier_anatomie:
        reader = csv.reader(fichier_anatomie)
        next(reader)  # Ignorer l'en-tête
        correspondances = {row[0]: row[1] for row in reader}

    # Ouvrir le fichier de coupes et le fichier de sortie
    with open(inputPath, mode='r', newline='', encoding='utf-8') as fichier_coupes, \
         open(outputPath_coupes, mode='w', newline='', encoding='utf-8') as fichier_sortie:
        reader = csv.DictReader(fichier_coupes)
        writer = csv.writer(fichier_sortie)

        # Écrire les noms des colonnes dans le fichier de sortie
        writer.writerow(colonnes)

        # Itérer sur chaque ligne du fichier de coupes
        for ligne in reader:
            labels_str = ligne["labels"]  # La troisième colonne contient la valeur des labels
            labels_list = ast.literal_eval(labels_str)  # Convertir la chaîne en liste

            # Remplacer les ID par les correspondances de labels et modifier la valeur du nombre de pixels
            labels_correspondants = [(correspondances.get(str(id), ""), "{:.4f}".format(pixels*Sx*Sy*Sz)) for id, pixels in labels_list]
            # Définir la dimension en fonction de la coupe
            dimension = ligne["dimensions"]

            # Écrire la ligne modifiée dans le fichier de sortie
            writer.writerow([ligne["coupe"], ligne["num coupe"],dimension, str(labels_correspondants) ])


# Traiter chaque fichier de coupes
for inputFile in inputFiles:

    # Réinitialiser la liste des données pour chaque nouveau fichier
    data = []
    inputPath = os.path.join(inputFolder,inputFile)

    # Construire le nom du fichier CSV de sortie
    outputFile_header = f'{os.path.splitext(inputFile)[0]}_header.csv'
    outputFile_coupes = f'{os.path.splitext(inputFile)[0]}_coupes.csv'

    # Chemin vers le fichier CSV de sortie
    outputPath_header = os.path.join(outputPath, outputFile_header)
    outputPath_coupes = os.path.join(outputPath, outputFile_coupes)

    # Noms des colonnes
    colonnes = ["modalite", "genre_mov", "age_mov","genre_fix","age_fix", "Sx", "Sy", "Sz"]

    # Ajouter les données à la liste
    data = extract_data_in_name(inputFile)

    # Ouvrir le fichier CSV en mode append
    with open(outputPath_header, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        # Écrire les noms des colonnes
        writer.writerow(colonnes)
        # Écrire les données dans le fichier CSV de sortie
        writer.writerow(data)

    # Appeler la fonction
    modifier_id_par_labels(inputPath, os.path.join(infoPath, "Anatomie.csv"), outputPath_coupes, data[5], data[6], data[7])
print(f"Les données ont été écrites dans les fichiers CSV dans le dossier : Keywords")