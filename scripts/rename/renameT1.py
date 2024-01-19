"""
Renommer les images et les csv OASIS T1 en utilisant le modèle suivant:
    T1_<id>_<IBSR>_<id>.nii.gz
    T1_<id>_<IBSR>_<id>.csv
"""

# ------------------------------------------------------------------------------------

import os
import re
import sys

def rename_files(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} n'est pas un dossier valide.")
        return
    
    sbj_pattern = re.compile(r'OAS1_(\d+)_MR\d+_mpr.*_sbj_(\d+)_reg_IBSR_(\d+)_ana\.nii_norm\.(csv|nii.gz)')
    gfc_pattern = re.compile(r'OAS1_(\d+)_MR\d+_mpr.*_gfc_reg_IBSR_(\d+)_ana\.nii_norm\.(csv|nii.gz)')
    default_pattern = re.compile(r'OAS1_(\d+)_MR\d+_mpr.*?(\d+)_anon_reg_IBSR_(\d+)_ana\.nii_norm\.(csv|nii.gz)')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):

            match_sbj = sbj_pattern.match(filename)
            if match_sbj:
                new_filename = f"T1_{match_sbj.group(1)}_IBSR_{match_sbj.group(3)}_sbj.{match_sbj.group(4)}"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renommage de {filename} en {new_filename}")
                continue

            match_gfc = gfc_pattern.match(filename)
            if match_gfc:
                new_filename = f"T1_{match_gfc.group(1)}_IBSR_{match_gfc.group(2)}_gfc.{match_gfc.group(3)}"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renommage de {filename} en {new_filename}")
                continue

            match_default = default_pattern.match(filename)
            if match_default:
                num = match_default.group(2) if match_default.group(2) else "1"
                new_filename = f"T1_{match_default.group(1)}_IBSR_{match_default.group(3)}_{num}.{match_default.group(4)}"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renommage de {filename} en {new_filename}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Utilisation: python script.py chemin_du_dossier")
    else:
        folder_path = sys.argv[1]
        rename_files(folder_path)

