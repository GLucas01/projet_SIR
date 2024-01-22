import pandas as pd
import random
import re, sys, os,ast

def extraire_mots_cles(label):
    #matches = re.findall(r'\(([^)]+),(\d+)\)', label)
    #mots_cles = [(mot, int(nombre)) for mot, nombre in matches]
    mots_cles = ast.literal_eval(label)
    return mots_cles

def generer_version_mots_cles(mots_cles):
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
    version_choisie = random.choice(versions)
    mots_a_retirer = ['Unknown', 'left undetermined', 'right undetermined']
    mots_cles_filtres = [(mot, nombre) for mot, nombre in mots_cles if mot not in mots_a_retirer]
    test_list_mot = [mot for mot, nombre in mots_cles_filtres]
    if test_list_mot == []:
       return "We observe nothing there."
    else: 
        mots_cles_texte = ', '.join([f"the {mot} of volume {nombre} mm³" for mot, nombre in mots_cles_filtres])
        dernier_mot_index = mots_cles_texte.rfind(', ')
        if dernier_mot_index != -1:
            mots_cles_texte = mots_cles_texte[:dernier_mot_index] + ' and ' + mots_cles_texte[dernier_mot_index + 2:]
            return version_choisie.format(mots_cles=mots_cles_texte)

def convertir_genre_en_mot(genre):
    mots_genre = {'M': 'a man', 'F': 'a woman'}
    return mots_genre.get(genre.upper(), genre)

def lire_textes_par_coupe(chemin_fichier):
    textes_par_coupe = {}
    coupe_actuelle = None

    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line in ['axial', 'coronal', 'sagittal']:
                coupe_actuelle = line
                textes_par_coupe[coupe_actuelle] = []
            else:
                textes_par_coupe[coupe_actuelle].append(line)

    return textes_par_coupe

def extraire_descriptions_pour_toutes_les_lignes(chemin_csv_header, chemin_csv_label, chemin_textes,chemin_output):
    df_header = pd.read_csv(chemin_csv_header)
    df_label = pd.read_csv(chemin_csv_label)


    for index_ligne in range(len(df_label)):
        descriptions_modifiees = []
        valeurs_ligne_header = df_header.iloc[0]
        valeurs_ligne_label = df_label.iloc[index_ligne]

        coupe = valeurs_ligne_label['coupe']

        textes_par_coupe = lire_textes_par_coupe(chemin_textes)
        textes_choisis = textes_par_coupe.get(coupe, textes_par_coupe)

        for _ in range(5):
            age_mov_null = False
            genre_fix_null = ""
            texte_original_choisi = random.choice(textes_choisis)
            for colonne, valeur in valeurs_ligne_header.items():
                if colonne == 'genre_mov':
                    genre_fix_null = convertir_genre_en_mot(valeur)
                elif colonne == 'genre_fix':
                    if pd.notnull(valeur):
                        valeur = convertir_genre_en_mot(valeur)
                        texte_original_choisi = texte_original_choisi.replace("[genre]", str(valeur))
                    else:
                        texte_original_choisi = texte_original_choisi.replace("[genre]", genre_fix_null)
                elif colonne == 'age_mov':
                    if pd.notnull(valeur):
                        if valeur == "JUV":
                            valeur = "juvenile"
                        else:
                            if isinstance(valeur, str):
                                valeur = f" of {''.join(char if char.isdigit() or char == ',' else '' for char in valeur).split(',')[0]} years old"
                            else:
                                valeur = f" of {int(valeur)} years old"
                        texte_original_choisi = texte_original_choisi.replace("[age]", str(valeur))
                    else:
                        age_mov_null = True
                elif colonne == 'age_fix' and age_mov_null:
                    if pd.notnull(valeur):
                        if valeur == "JUV":
                            valeur = "juvenile"
                        else:
                            if isinstance(valeur, str):
                                valeur = f" of {''.join(char if char.isdigit() or char == ',' else '' for char in valeur).split(',')[0]} years old"
                            else:
                                valeur = f" of {int(valeur)} years old"
                        texte_original_choisi = texte_original_choisi.replace("[age]", str(valeur))
                    else:
                        texte_original_choisi = texte_original_choisi.replace("[age]", '')
                else: 
                    texte_original_choisi = texte_original_choisi.replace(f"[{colonne}]", str(valeur))

            for colonne, valeur in valeurs_ligne_label.items():
                texte_original_choisi = texte_original_choisi.replace(f"[{colonne}]", str(valeur))

            label = valeurs_ligne_label['labels']
            mots_cles = extraire_mots_cles(label)

            version_mots_cles = generer_version_mots_cles(mots_cles)
            texte_modifie = f"{texte_original_choisi} {version_mots_cles}"

            descriptions_modifiees.append(texte_modifie)
            
        df_descriptions = pd.DataFrame({'description': descriptions_modifiees})

        nom_base = os.path.splitext(os.path.basename(chemin_csv_label))[0].rsplit('_', 1)[0]
        num_coupe = valeurs_ligne_label['num coupe']

        csv_sortie = f"{nom_base}_{coupe}_{num_coupe }.csv"
        chemin_csv_sortie = os.path.join(chemin_output, csv_sortie)
        df_descriptions.to_csv(chemin_csv_sortie, index=False)

    return None

def afficher_aide():
    print("Usage: python script.py <InputFolder>")

# Chemin vers dossiers contenant les fichiers csv des coupes
if len(sys.argv) != 2:
    print("Usage: python3 mon_script.py <inputFolder>")
    sys.exit(1)

inputFolder = sys.argv[1]

# Liste pour les fichiers finissant par "header.csv"
header_files = [f for f in os.listdir(inputFolder) if f.endswith("header.csv")]

# Liste pour les fichiers finissant par "coupes.csv"
coupes_files = [f for f in os.listdir(inputFolder) if f.endswith("coupes.csv")]


chemin_textes = "./Caption_Generation/en/generic_leg.txt"

for header_file in header_files:
    chemin_du_csv_header = os.path.join(inputFolder, header_file)
    # Recherche le fichier coupes.csv correspondant
    for coupes_file in coupes_files:
        if coupes_file.startswith(header_file.replace('_header.csv', '')):
            chemin_du_csv_label = os.path.join(inputFolder, coupes_file)
            break

    # Chemin vers dossier final
    chemin_output = f"../data/Captions/{header_file.replace('_header.csv', '')}"
    if not os.path.exists(chemin_output):
        os.makedirs(chemin_output)
    print(f"Processing {chemin_du_csv_header} and {chemin_du_csv_label}")
    extraire_descriptions_pour_toutes_les_lignes(chemin_du_csv_header, chemin_du_csv_label, chemin_textes,chemin_output)
