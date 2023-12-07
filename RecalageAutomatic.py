import subprocess
import SimpleITK as sitk
import os

files = os.listdir('moving_images')
print(files)
moving_image = os.path.join('moving_images', files[0])
print(moving_image)

files = os.listdir('fixed_images')
print(files)
fixed_image = os.path.join('fixed_images', files[0])
print(fixed_image)

files = os.listdir('parameters')
print(files)
parameters = os.path.join('parameters', files[0])
print(parameters)

files = os.listdir('seg_images')
print(files)
seg_image = os.path.join('seg_images', files[0])
print(seg_image)

# Initialiser le compteur de dossiers
folder_counter = 1

# Construire le nom du dossier
output_folder = f"output{folder_counter}"

# Tant que le dossier existe déjà, incrémenter le compteur et construire un nouveau nom de dossier
while os.path.exists(output_folder):
    folder_counter += 1
    output_folder = f"output{folder_counter}"

# Créer le nouveau dossier
os.makedirs(output_folder)

# Créer le sous-dossier 'result' dans 'output_folder'
result_folder = os.path.join(output_folder, 'result')
os.makedirs(result_folder, exist_ok=True)

# Construire les commandes
elastic_command = f"elastix -m {moving_image} -f {fixed_image} -p {parameters} -out {output_folder}"
transformix_command = f"transformix -in {seg_image} -tp {output_folder}/TransformParameters.0.txt -out {output_folder}/result"

# Exécuter les commandes
subprocess.run(elastic_command, shell=True)
subprocess.run(transformix_command, shell=True)

# Image recalée
registrationImagePath = f"{output_folder}/result/result.mha"
registrationImage = sitk.ReadImage(registrationImagePath)

# Save the image
output_folder = f"{output_folder}/result/"
output_filename = f"result.nii"
output_path = output_folder + output_filename
sitk.WriteImage(registrationImage, output_path)

