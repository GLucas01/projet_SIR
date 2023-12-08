import os
import subprocess
import SimpleITK as sitk

# Liste des images dans les dossiers
moving_images = os.listdir('/home/julie/Documents/SIR/projet_SIR/data/moving_images')
print(moving_images)
fixed_images = os.listdir('/home/julie/Documents/SIR/projet_SIR/data/fixed_images')
print(fixed_images)

files = os.listdir('/home/julie/Documents/SIR/projet_SIR/data/parameters')
print(files)
nbParam = len(files)
if nbParam == 0:
    print("Aucun fichier de paramètres")
    exit()
elif nbParam == 1:
    parameters = os.path.join('/home/julie/Documents/SIR/projet_SIR/data/parameters', files[0])
    print(parameters)
elif nbParam == 2:
    parameters_file1 = os.path.join('/home/julie/Documents/SIR/projet_SIR/data/parameters', files[0])
    parameters_file2 = os.path.join('/home/julie/Documents/SIR/projet_SIR/data/parameters', files[1])
    print(parameters_file1)
    print(parameters_file2)
else:
    print("Trop de fichiers de paramètres")
    exit()

# Parcourir toutes les combinaisons d'images
for moving_image in moving_images:
    for fixed_image in fixed_images:
        # Extraire les numéros des images
        moving_number = moving_image[5:7]
        fixed_number = fixed_image[5:7]

        # Créer le nom du dossier de sortie
        output_folder = f"/home/julie/Documents/SIR/projet_SIR/output/output{moving_number}{fixed_number}"
        os.makedirs(output_folder, exist_ok=True)

        # Créer le nom du dossier de résultat
        result_folder = os.path.join(output_folder, 'result')
        os.makedirs(result_folder, exist_ok=True)

        # Construire les commandes elastix et transformix
        if nbParam == 1:
            elastix_command = f"elastix -m /home/julie/Documents/SIR/projet_SIR/data/moving_images/{moving_image} -f /home/julie/Documents/SIR/projet_SIR/data/fixed_images/{fixed_image} -p {parameters} -out {output_folder}"
        if nbParam == 2:
            elastix_command = f"elastix -m /home/julie/Documents/SIR/projet_SIR/data/moving_images/{moving_image} -f /home/julie/Documents/SIR/projet_SIR/data/fixed_images/{fixed_image} -p {parameters_file1} -p {parameters_file2} -out {output_folder}"
        #elastix -f fixed_image.nii -m moving_image.nii -out output_folder -p parametres1.txt,parametres2.txt
        transformix_command = f"transformix -in /home/julie/Documents/SIR/projet_SIR/data/seg_images/IBSR_{fixed_number}_seg_ana.nii -tp {output_folder}/TransformParameters.0.txt -out {result_folder}"

        # Exécuter les commandes
        subprocess.run(elastix_command, shell=True)
        subprocess.run(transformix_command, shell=True)

        # Image recalée
        registrationImagePath = f"{output_folder}/result/result.mha"
        registrationImage = sitk.ReadImage(registrationImagePath)

        # Save the image
        output_folder = f"{output_folder}/result/"
        output_filename = f"result.nii"
        output_path = output_folder + output_filename
        sitk.WriteImage(registrationImage, output_path)