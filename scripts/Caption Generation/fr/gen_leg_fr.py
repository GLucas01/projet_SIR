import pandas as pd
import random
import re, sys, os

def extraire_mots_cles(label):
    # Utiliser une expression régulière pour extraire les mots-clés du format "[(mot1,15),(mot2,54)]"
    matches = re.findall(r'\(([^)]+),(\d+)\)', label)
    mots_cles = [(mot, int(nombre)) for mot, nombre in matches]
    return mots_cles

def determiner_le_determinant(mot):
    # Détermine le déterminant approprié en fonction de la première lettre du mot
    determinant = "le "
    if mot[0].lower() in ['a', 'e', 'i', 'o', 'u', 'h']:
        determinant = "l'"
    premier_mot = mot.split()[0]
    if premier_mot in ['matière','corne']:
        determinant = "la "
    return determinant

def generer_version_mots_cles(mots_cles):
    # Générer une version aléatoire de la présentation des mots-clés
    versions = [
        "On y observe {mots_cles}.",
        "Les éléments suivants sont présents : {mots_cles}.",
        "On y distingue {mots_cles}.",
        "On y voit {mots_cles}.",
        "L'image révèle la présence de {mots_cles}.",
        "Les détails observés comprennent {mots_cles}.",
        "La coupe révèle {mots_cles}.",
        "On y observe les caractéristiques suivantes : {mots_cles}.",
        "Les éléments suivants sont présents dans l'image : {mots_cles}.",
        "On y distingue clairement : {mots_cles}.",
        "On y voit clairement : {mots_cles}.",
        "L'image révèle la présence notable de : {mots_cles}.",
        "Les détails observés comprennent : {mots_cles}.",
        "La coupe révèle la présence de : {mots_cles}."
    ]
    version_choisie = random.choice(versions)
    mots_a_retirer = ['Non identifié', 'Indéterminé gauche', 'Indéterminé droit']

    # Filtrer les mots-clés pour exclure ceux à retirer
    mots_cles_filtres = [(mot, nombre) for mot, nombre in mots_cles if mot not in mots_a_retirer]

    mots_cles_texte = ', '.join([f"{determiner_le_determinant(mot)}{mot}" for mot, nombre in mots_cles_filtres])
    dernier_mot_index = mots_cles_texte.rfind(', ')
    if dernier_mot_index != -1:
        mots_cles_texte = mots_cles_texte[:dernier_mot_index] + ' ainsi que ' + mots_cles_texte[dernier_mot_index + 2:]
    return version_choisie.format(mots_cles=mots_cles_texte)

def convertir_genre_en_mot(genre):
    # Mappez chaque valeur de [genre] à un mot spécifique
    mots_genre = {'M': 'un homme', 'F': 'une femme', '1': 'un homme', '2': 'une femme'}
    return mots_genre.get(genre.upper(), genre)

def lire_textes_par_coupe(chemin_fichier):
    textes_par_coupe = {}
    coupe_actuelle = None

    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line in ['axiale', 'coronale', 'sagittale']:
                coupe_actuelle = line
                textes_par_coupe[coupe_actuelle] = []
            else:
                textes_par_coupe[coupe_actuelle].append(line)

    return textes_par_coupe


def extraire_descriptions_pour_toutes_les_lignes(chemin_csv_header, chemin_csv_label, chemin_textes):
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
            texte_original_choisi = random.choice(textes_choisis)

            for colonne, valeur in valeurs_ligne_header.items():
                if colonne == 'genre':
                    valeur = convertir_genre_en_mot(valeur)
                elif colonne == 'age':
                    if pd.notnull(valeur):
                        valeur = f" de {int(valeur)} ans"
                    else:
                        valeur = ""  # Si la valeur de l'âge est nulle, n'affiche rien
                texte_original_choisi = texte_original_choisi.replace(f"[{colonne}]", str(valeur))
            for colonne, valeur in valeurs_ligne_label.items():
                texte_original_choisi = texte_original_choisi.replace(f"[{colonne}]", str(valeur))

            label = valeurs_ligne_label['label']
            mots_cles = extraire_mots_cles(label)

            version_mots_cles = generer_version_mots_cles(mots_cles)
            texte_modifie = f"{texte_original_choisi} {version_mots_cles}"
            descriptions_modifiees.append(texte_modifie)
    
    df_descriptions = pd.DataFrame({'description': descriptions_modifiees})

    nom_base = os.path.splitext(os.path.basename(chemin_csv_label))[0].rsplit('_', 1)[0]
    num_coupe = valeurs_ligne_label['num coupe']

    chemin_csv_sortie = f"{nom_base}_{coupe}_{num_coupe }.csv"
    df_descriptions.to_csv(chemin_csv_sortie, index=False)

       
    return None

def afficher_aide():
    print("Usage: python script.py chemin_du_csv_header.csv chemin_du_csv_coupe.csv")

if len(sys.argv) < 3:
    print("Erreur: Les chemins des fichiers CSV sont manquants.")
    afficher_aide()
    sys.exit(1)

chemin_du_csv_header = sys.argv[1]
chemin_du_csv_label = sys.argv[2]
chemin_textes = "Phrases_generique.txt"

extraire_descriptions_pour_toutes_les_lignes(chemin_du_csv_header, chemin_du_csv_label, chemin_textes)
