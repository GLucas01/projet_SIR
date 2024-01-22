import csv
import ast
import os
import sys
import re

# Chemin vers les fichiers info.csv
chemin_dossier_infos = "../data/Keywords"

# Chemin vers dossier final
chemin_output_T1 = "../data/Keywords_csv/T1"
if not os.path.exists(chemin_output_T1):
    os.makedirs(chemin_output_T1)

chemin_output_T2 = "../data/Keywords_csv/T2"
if not os.path.exists(chemin_output_T2):
    os.makedirs(chemin_output_T2)
    
chemin_output_FL = "../data/Keywords_csv/FL"
if not os.path.exists(chemin_output_FL):
    os.makedirs(chemin_output_FL)

# Chemin vers dossiers contenant les fichiers csv des coupes
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

inputFiles = [f for f in os.listdir(inputFolder) if f.endswith('csv')]


# Fonction pour extraire les données du nom du fichier
def extraire_donnees_de_nom(nom_fichier):
    # Supprimer l'extension .csv du nom du fichier
    nom_sans_extension = os.path.splitext(nom_fichier)[0]

    # Diviser le nom en parties en utilisant '_' comme séparateur
    parties = nom_sans_extension.split('_')

    # Extraire les données nécessaires
    modalite = parties[0]
    ID = parties[1]
   
    # Retourner une liste avec les données extraites
    
    return [modalite, ID]


def extraire_infos(ID, modalite, chemin_dossier_infos):
    ID = int(ID)
    # Conserver les zéros en tête en convertissant l'ID en chaîne pour la modalité 'T1'
    if modalite == 'T1':
        ID = str(ID).zfill(4)
    else:
        ID = str(ID)

    # Choisir le bon fichier CSV en fonction de la modalité
    if modalite == 'T1':
        chemin_fichier_infos = os.path.join(chemin_dossier_infos, 'OASIS_info.csv')
    elif modalite == 'T2':
        chemin_fichier_infos = os.path.join(chemin_dossier_infos, 'IXI_info.csv')
    elif modalite == 'FL':
        chemin_fichier_infos = os.path.join(chemin_dossier_infos, 'Kirby_info.csv')
    elif modalite == 'IBSR':
        chemin_fichier_infos = os.path.join(chemin_dossier_infos, 'Atlas_info.csv')
    else:
        print(f"Modalité inconnue : {modalite}")
        return "", ""

    # Ouvrir le fichier CSV
    with open(chemin_fichier_infos, 'r', newline='', encoding='utf-8') as fichier_infos:
        # Créer un lecteur CSV avec des dictionnaires pour accéder aux données par nom de colonne
        reader = csv.DictReader(fichier_infos)

        # Parcourir chaque ligne du CSV
        for ligne in reader:
            # Si l'ID de la ligne correspond à l'ID recherché
            if ligne['ID'] == ID:
                # Extraire l'âge et le genre
                age = ligne['AGE']
                genre = ligne['GENDER']

                # Retourner l'âge et le genre
                return age, genre

    # Si l'ID n'a pas été trouvé dans le CSV, retourner des chaînes vides
    return "", ""


def modifier_id_par_labels(chemin_fichier_coupes, chemin_fichier_anatomie, chemin_csv_sortie):
    # Noms des colonnes
    colonnes = ["coupe", "num coupe", "dimensions", "labels"]

    # Lire le fichier d'anatomie et créer un dictionnaire de correspondances
    correspondances = {}
    with open(chemin_fichier_anatomie, mode='r', newline='', encoding='utf-8') as fichier_anatomie:
        reader = csv.reader(fichier_anatomie)
        next(reader)  # Ignorer l'en-tête
        correspondances = {row[0]: row[1] for row in reader}

    # Ouvrir le fichier de coupes et le fichier de sortie
    with open(chemin_fichier_coupes, mode='r', newline='', encoding='utf-8') as fichier_coupes, \
         open(chemin_csv_sortie, mode='w', newline='', encoding='utf-8') as fichier_sortie:
        reader = csv.DictReader(fichier_coupes)
        writer = csv.writer(fichier_sortie)

        # Écrire les noms des colonnes dans le fichier de sortie
        writer.writerow(colonnes)

        # Itérer sur chaque ligne du fichier de coupes
        for ligne in reader:
            labels_str = ligne["labels"]  # La troisième colonne contient la valeur des labels
            labels_list = ast.literal_eval(labels_str)  # Convertir la chaîne en liste

            # Remplacer les ID par les correspondances de labels et modifier la valeur du nombre de pixels
            labels_correspondants = [(correspondances.get(str(id), ""), "{:.4f}".format(pixels * Sx * Sy * Sz)) for id, pixels in labels_list]
            # Définir la dimension en fonction de la coupe
            dimension = ligne["dimensions"]

            # Écrire la ligne modifiée dans le fichier de sortie
            writer.writerow([ligne["coupe"], ligne["num coupe"],dimension, str(labels_correspondants) ])


# Liste pour stocker les données
donnees = []
# Traiter chaque fichier de coupes
for fichier_coupes in inputFiles:

    # Réinitialiser la liste des données pour chaque nouveau fichier
    donnees = []

    # Chemin vers le fichier de coupes
    chemin_fichier_coupes = os.path.join(inputFolder, fichier_coupes)

    # Extraire les données du nom du fichier
    modalite, ID = extraire_donnees_de_nom(fichier_coupes)

    # Extraire les informations d'âge et de genre de l'image mobile
    age_mov, genre_mov = extraire_infos(ID, modalite, chemin_dossier_infos)

    # Extraire les informations d'âge et de genre de l'image fixe
    age_fix, genre_fix = "", ""
    if "majority" in fichier_coupes:
        age_fix, genre_fix = "", ""
    else:
        pattern = re.search(r'([^_]+)_([^_]+)_([^_]+)_([^_]+)\.csv', fichier_coupes)
        if pattern:
            age_fix, genre_fix = extraire_infos(f'{pattern.group(4)}', f'{pattern.group(3)}', chemin_dossier_infos)
        if pattern.group(1) == 'IBSR':
            modalite = f'{pattern.group(3)}'

    # Construire le nom du fichier CSV de sortie
    nom_fichier_sans_extension = os.path.splitext(fichier_coupes)[0]
    nom_fichier_sortie = f'{nom_fichier_sans_extension}_header.csv'

    # Chemin vers le fichier CSV de sortie
    if modalite == "T1":
            chemin_csv_sortie = os.path.join(chemin_output_T1, nom_fichier_sortie)
    elif modalite == "T2":
        chemin_csv_sortie = os.path.join(chemin_output_T2, nom_fichier_sortie)
    else:
        chemin_csv_sortie = os.path.join(chemin_output_FL, nom_fichier_sortie)

    # Noms des colonnes
    colonnes = ["modalite", "genre_mov", "age_mov","genre_fix","genre_fix", "Sx", "Sy", "Sz"]

    # Lire le fichier coupes
    with open(chemin_fichier_coupes, 'r') as f:
        reader = csv.DictReader(f)

        # Extraire les valeurs de Sx, Sy et Sz
        voxel = next(reader)['voxel']
        Sx, Sy, Sz = map(float, voxel.strip('()').split(','))

    # Ajouter les données à la liste
    donnees = [modalite, genre_mov, age_mov,genre_fix,age_fix, Sx, Sy, Sz]

    # Ouvrir le fichier CSV en mode append
    with open(chemin_csv_sortie, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)

        # Écrire les noms des colonnes
        writer.writerow(colonnes)

        # Écrire les données dans le fichier CSV de sortie
        writer.writerow(donnees)

    # Construire le nom du fichier CSV de sortie
    nom_fichier_sans_extension = os.path.splitext(fichier_coupes)[0]
    nom_fichier_sortie = f'{nom_fichier_sans_extension}_coupes.csv'

    # Chemin vers le fichier CSV de sortie
    if modalite == "T1":
            chemin_csv_sortie = os.path.join(chemin_output_T1, nom_fichier_sortie)
    elif modalite == "T2":
        chemin_csv_sortie = os.path.join(chemin_output_T2, nom_fichier_sortie)
    else:
        chemin_csv_sortie = os.path.join(chemin_output_FL, nom_fichier_sortie)

    # Appeler la fonction
    modifier_id_par_labels(chemin_fichier_coupes, os.path.join(chemin_dossier_infos, "Anatomie.csv"), chemin_csv_sortie)
print(f"Les données ont été écrites dans les fichiers CSV dans le dossier : ../data/Keywords_csv")