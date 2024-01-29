import pandas as pd
import random
import re, sys, os, ast

# Fonction pour extraire le contenu de la colonne "labels"
def extract_labels(label):
    labels = ast.literal_eval(label)
    return labels

# Fonction pour générer la deuxième moitié de la légende contenant les éléments présents et leur volume
def gen_label_part(mots_cles):
    versions = [
        "We observe {mots_cles} there.",
        "The following elements are present : {mots_cles}.",
        "We distinguishe {mots_cles} in it.",
        "We see {mots_cles}.",
        "The image reveals the presence of {mots_cles}.",
        "The observed details include {mots_cles}.",
        "The section reveals {mots_cles}.",
        "We observe the following characteristics: {mots_cles}.",
        "The following elements are present in the image: {mots_cles}.",
        "We distinguishe clearly: {mots_cles}.",
        "We see clearly: {mots_cles}.",
        "The image notably reveals the presence of: {mots_cles}.",
        "The observed details include: {mots_cles}.",
        "The section reveals the presence of: {mots_cles}."
    ]
    label_part = random.choice(versions)
    uselessLabel = ['Unknown', 'left undetermined', 'right undetermined']
    words = [(word, num) for word, num in mots_cles if word not in uselessLabel]
    if not [mot for mot, nombre in words]:
        return "We observe nothing there."
    else: 
        text = ', '.join([f"the {mot} of volume {nombre} mm³" for mot, nombre in words])
        lastWord_index = text.rfind(', ')
        if lastWord_index != -1:
            text = text[:lastWord_index] + ' and ' + text[lastWord_index + 2:]
        return label_part.format(mots_cles=text)

# Fonction pour convertir le contenu de la colonne genre en une formulation textuelle
def convert_gender(genre):
    mots_genre = {'M': 'a man', 'F': 'a woman', '': 'a person'}
    if isinstance(genre,str):
        return mots_genre.get(genre.upper(), genre)
    else :
        return "a person"

# Fonction pour convertir le contenu de la colonne coupe en une formulation textuelle
def convert_slice(coupe):
    mots_coupe = {'axial': 'an axial', 'coronal': 'a coronal', 'sagittal': 'a sagittal'}
    return mots_coupe.get(coupe.upper(), coupe)

# Fonction pour charger les textes spécifiques à chaque type de coupe
def text_by_slice():
    text = {}
    slice = None

    with open(textPath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line in ['axial', 'coronal', 'sagittal']:
                slice = line
                text[slice] = []
            else:
                text[slice].append(line)

    return text

# Fonction pour extraire les informations des fichiers CSV et générer des légendes
def extract_captions(filePath_header, filePath_coupes, outputPath_final):
    df_header = pd.read_csv(filePath_header)
    df_label = pd.read_csv(filePath_coupes)

    for index_ligne in range(len(df_label)):
        modifCaption = []
        headerLine = df_header.iloc[0]
        labelLine = df_label.iloc[index_ligne]

        coupe = labelLine['coupe']
        text = text_by_slice()
        sliceText = text.get(coupe, text)

        for _ in range(5):
            age_mov = ""
            genre_mov_null = True
            caption = random.choice(sliceText)

            for colonne, valeur in headerLine.items():
                # Sélection du genre de l'image mouvante en priorité
                if colonne == 'genre_mov':
                    valeur = convert_gender(valeur)
                    genre_mov_null = False
                    caption = caption.replace("[genre]", str(valeur))
                elif colonne == 'genre_fix'and genre_mov_null:
                    valeur = convert_gender(valeur)
                    caption = caption.replace("[genre]", str(valeur))
                
                # Sélection de l'age de l'image fix en priorité
                elif colonne == 'age_mov':
                    if pd.notnull(valeur):
                        age_mov = "juvenile" if valeur == "JUV" else f" of {''.join(char if char.isdigit() or char == ',' else '' for char in valeur).split(',')[0]} years old" if isinstance(valeur, str) else f" of {int(valeur)} years old"
                elif colonne == 'age_fix':
                    if pd.notnull(valeur):
                        valeur = "juvenile" if valeur == "JUV" else f" of {''.join(char if char.isdigit() or char == ',' else '' for char in valeur).split(',')[0]} years old" if isinstance(valeur, str) else f" of {int(valeur)} years old"
                        caption = caption.replace("[age]", str(valeur))
                    else:
                        caption = caption.replace("[age]", str(age_mov))
                # Autres colonnes
                else: 
                    caption = caption.replace(f"[{colonne}]", str(valeur))
                    
            # Ajout du type de coupe et des label
            for colonne, valeur in labelLine.items():
                if colonne == 'genre_mov':
                    valeur = convert_slice(valeur)
                caption = caption.replace(f"[{colonne}]", str(valeur))

            label = labelLine['labels']
            words = extract_labels(label)

            version_mots_cles = gen_label_part(words)
            texte_modifie = f"{caption} {version_mots_cles}"

            modifCaption.append(texte_modifie)
        
        # Enregistrer les 5 descriptions générées pour la coupe dans un fichier csv
        df_caption = pd.DataFrame({'description': modifCaption})

        nom_base = os.path.splitext(os.path.basename(filePath_coupes))[0].rsplit('_', 1)[0]
        num_coupe = labelLine['num coupe']

        csv_sortie = f"{nom_base}_{coupe}_{num_coupe}.csv"
        chemin_csv_sortie = os.path.join(outputPath_final, csv_sortie)
        df_caption.to_csv(chemin_csv_sortie, index=False)

    return None

# Vérification du nombre d'arguments de la ligne de commande
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

# Récupération du chemin du dossier d'entrée et création d'un dossier de sortie pour les descriptions
inputFolder = sys.argv[1]
if inputFolder.endswith("inv"):
    outputPath = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Captions_inv")
else:
    outputPath = os.path.join(os.path.sep.join(inputFolder.split(os.path.sep)[:-1]),"Captions")
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

# Liste pour les fichiers finissant par "header.csv"
header_files = [f for f in os.listdir(inputFolder) if f.endswith("header.csv")]

# Liste pour les fichiers finissant par "coupes.csv"
coupes_files = [f for f in os.listdir(inputFolder) if f.endswith("coupes.csv")]

# Chemin vers le fichier texte contenant des formulations génériques
textPath = "./Caption_Generation/en/generic_leg.txt"

for header_file in header_files:
    filePath_header = os.path.join(inputFolder, header_file)
    # Recherche le fichier coupes.csv correspondant
    fileName = header_file.replace('_header.csv', '')
    for coupes_file in coupes_files:
        if coupes_file.startswith(fileName):
            filePath_coupes = os.path.join(inputFolder, coupes_file)
            break

    # Chemin vers dossier final
    outputPath_final = os.path.join(outputPath,fileName)     
    if not os.path.exists(outputPath_final):
        os.makedirs(outputPath_final)
                    
    print(f"Processing {filePath_header} and {filePath_coupes}")
    extract_captions(filePath_header, filePath_coupes, outputPath_final)
