"""
Renommer les images et les csv IXI-T2 en utilisant le modèle suivant:
    T2_<id>_<IBSR>_<id>.nii.gz
    T2_<id>_<IBSR>_<id>.csv
"""

# ------------------------------------------------------------------------------------

import os
import re
import sys

def rename_files(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} n'est pas un dossier valide.")
        return

    pattern = re.compile(r'IXI(\d+)-IOP-(\d+)-(\w+)_brain_reg_IBSR_(\d+)_ana_norm')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            match = pattern.match(filename)
            if match:

                new_filename = f"{match.group(3)}_{match.group(1)}_IBSR_{match.group(4)}.csv" if filename.endswith('.csv') else f"{match.group(3)}_{match.group(1)}_IBSR_{match.group(4)}.nii.gz"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renommage de {filename} en {new_filename}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Utilisation: python script.py chemin_du_dossier")
    else:
        folder_path = sys.argv[1]
        rename_files(folder_path)

