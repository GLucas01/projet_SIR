"""
Renommer les images et les csv Kriby21 FLAIR en utilisant le modèle suivant:
    FL_<id>_<IBSR>_<id>.nii.gz
    FL_<id>_<IBSR>_<id>.csv
"""

# ------------------------------------------------------------------------------------

import os
import re
import sys

def rename_files(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} n'est pas un dossier valide.")
        return

    pattern = re.compile(r'KKI2009-(\d+)-FLAIR_brain_reg_IBSR_(\d+)_ana_norm')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):

            match = pattern.match(filename)
            if match:

                new_filename = f"FL_{match.group(1)}_IBSR_{match.group(2)}.csv" if filename.endswith('.csv') else f"FL_{match.group(1)}_IBSR_{match.group(2)}.nii.gz"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renommage de {filename} en {new_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation: python script.py chemin_du_dossier")
    else:
        folder_path = sys.argv[1]
        rename_files(folder_path)
