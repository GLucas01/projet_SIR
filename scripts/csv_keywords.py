import csv
import ast
import os

# Chemin vers les fichiers info.csv
chemin_dossier_infos = r'C:\Users\Admin\Documents\4TC\SIR\infos_keywords'

# Chemin vers le dossier contenant les fichiers CSV des coupes
chemin_dossier_coupes = r'C:\Users\Admin\Documents\4TC\SIR\DATA\FLAIR_csv'

# Chemin vers le fichier anatomie.csv
chemin_fichier_anatomie = r'C:\Users\Admin\Documents\4TC\SIR\infos_keywords\Anatomie.csv'




# Fonction pour extraire les données du nom du fichier
def extraire_donnees_de_nom(nom_fichier):
    # Supprimer l'extension .csv du nom du fichier
    nom_sans_extension = os.path.splitext(nom_fichier)[0]

    # Diviser le nom en parties en utilisant '_' comme séparateur
    parties = nom_sans_extension.split('_')

    # Extraire les données nécessaires
    modalite = parties[0]
    ID = int(parties[1])  # Convertir l'ID en entier
   
    # Retourner une liste avec les données extraites
    
    return [modalite, ID]




def extraire_infos(ID, modalite, chemin_dossier_infos):
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
    else:
        print(f"Modalité inconnue : {modalite}")
        return "", ""

    # Ouvrir le fichier CSV
    with open(chemin_fichier_infos, 'r', newline='', encoding='utf-8') as fichier_infos:
        # Créer un lecteur CSV
        reader = csv.reader(fichier_infos)

        # Passer l'en-tête du CSV
        next(reader)

        # Parcourir chaque ligne du CSV
        for ligne in reader:
            # Si l'ID de la ligne correspond à l'ID recherché
            if ligne[0] == ID:
                # Extraire l'âge et le genre
                age = ligne[1]
                genre = ligne[2]

                # Retourner l'âge et le genre
                return age, genre

    # Si l'ID n'a pas été trouvé dans le CSV, retourner des chaînes vides
    return "", ""









# Liste pour stocker les données
donnees = []





# Itérer sur chaque fichier de coupes dans le dossier
for fichier_coupes in os.listdir(chemin_dossier_coupes):
    if fichier_coupes.endswith('.csv'):
        # Réinitialiser la liste des données pour chaque nouveau fichier
        donnees = []

        # Chemin vers le fichier de coupes
        chemin_fichier_coupes = os.path.join(chemin_dossier_coupes, fichier_coupes)

        # Extraire les données du nom du fichier
        donnees_nom_fichier = extraire_donnees_de_nom(fichier_coupes)

        # Extraire les informations d'âge et de genre
        age, genre = extraire_infos(donnees_nom_fichier[1], donnees_nom_fichier[0], chemin_dossier_infos)

        # Construire le nom du fichier CSV de sortie
        nom_fichier_sans_extension = os.path.splitext(fichier_coupes)[0]
        nom_fichier_sortie = f'{nom_fichier_sans_extension}_header.csv'

        # Chemin vers le fichier CSV de sortie
        chemin_csv_sortie = os.path.join(r'C:\Users\Admin\Documents\4TC\SIR\DATA\FLAIR_csv3', nom_fichier_sortie)

        # Noms des colonnes
        colonnes = ["modalite", "genre", "age", "Sx", "Sy", "Sz"]

        # Lire le fichier coupes
        with open(chemin_fichier_coupes, 'r') as f:
            first_line = f.readline()

        # Extraire les valeurs de Sx, Sy et Sz de la première ligne
        
        columns = first_line.split(',')

        # Extract the fourth column
        fourth_column = columns[4] + columns[5] + columns[6]
        fourth_column = fourth_column.replace('"', '').replace('(','').replace(')','')
                                      
    

       

        # Split the fourth column on spaces and assign the values to Sx, Sy, Sz
        Sx, Sy, Sz = map(float, fourth_column.split())

        

        # Ajouter les données à la liste
        donnees = [donnees_nom_fichier[0], genre, age, Sx, Sy, Sz]

        # Ouvrir le fichier CSV en mode append
        with open(chemin_csv_sortie, mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)

            # Écrire les noms des colonnes
            writer.writerow(colonnes)
            
            # Écrire les données dans le fichier CSV de sortie
            writer.writerow(donnees)
print(f"Les données ont été écrites dans les fichiers CSV dans le dossier ")



def modifier_id_par_labels(chemin_fichier_coupes, chemin_fichier_anatomie, chemin_csv_sortie):
    # Noms des colonnes
    colonnes = ["coupe", "num_coupe", "dimension", "labels"]

    # Lire le fichier d'anatomie et créer un dictionnaire de correspondances
    correspondances = {}
    with open(chemin_fichier_anatomie, mode='r', newline='', encoding='utf-8') as fichier_anatomie:
        reader = csv.reader(fichier_anatomie)
        next(reader)  # Ignorer l'en-tête
        correspondances = {row[0]: row[1] for row in reader}

    # Ouvrir le fichier de coupes et le fichier de sortie
    with open(chemin_fichier_coupes, mode='r', newline='', encoding='utf-8') as fichier_coupes, \
         open(chemin_csv_sortie, mode='w', newline='', encoding='utf-8') as fichier_sortie:
        reader = csv.reader(fichier_coupes)
        writer = csv.writer(fichier_sortie)

        # Écrire les noms des colonnes dans le fichier de sortie
        writer.writerow(colonnes)

        # Itérer sur chaque ligne du fichier de coupes
        for ligne in reader:
            labels_str = ligne[2]  # La troisième colonne contient la valeur des labels
            labels_list = ast.literal_eval(labels_str)  # Convertir la chaîne en liste
            
            # Remplacer les ID par les correspondances de labels et modifier la valeur du nombre de pixels
            labels_correspondants = [(correspondances.get(str(id), ""), pixels * Sx * Sy * Sz) for id, pixels in labels_list]
            # Définir la dimension en fonction de la coupe
            if ligne[0] == 'Coronal':
                dimension = '256*128'
            elif ligne[0] == 'Axial':
                dimension = '256*256'
            elif ligne[0] == 'Sagittal':
                dimension = '256*128'
            else:
                dimension = ''

            # Écrire la ligne modifiée dans le fichier de sortie
            writer.writerow([ligne[0], ligne[1],dimension, str(labels_correspondants) ])




# Obtenir une liste de tous les fichiers dans le dossier de coupes
fichiers_coupes = os.listdir(chemin_dossier_coupes)

# Traiter chaque fichier de coupes
for fichier_coupes in fichiers_coupes:
    # Construire le chemin complet vers le fichier de coupes
    chemin_fichier_coupes = os.path.join(chemin_dossier_coupes, fichier_coupes)

    # Construire le nom du fichier CSV de sortie
    nom_fichier_sans_extension = os.path.splitext(fichier_coupes)[0]
    nom_fichier_sortie = f'{nom_fichier_sans_extension}_coupes.csv'

    # Chemin vers le fichier CSV de sortie
    chemin_csv_sortie = os.path.join(r'C:\Users\Admin\Documents\4TC\SIR\DATA\FLAIR_csv3', nom_fichier_sortie)

    # Appeler la fonction
    modifier_id_par_labels(chemin_fichier_coupes, chemin_fichier_anatomie, chemin_csv_sortie)




