# Projet SIR - Dall-e Brain

Un modèle génératif pour des images synthétiques de cerveau sain.

![alt text](logo.png)

## Traitement sur les images (rotation, recalage, normalisation, nouveaux atlas)

### Rotations
- Utilisation de FSL 
- Commande : `fslswapdim input.nii x y z output.nii`
- pour la dataset OASIS, rotation constante qui est la suivante : `fslswapdim input.nii z -x y output.nii`

### Recalage

#### skull_stripping.sh
- permet d'enlever les zones extérieures du cerveau . Les images obtenues sont "skulled"
- **usage** :
	- général : `skull_stripping.sh <dossier>`

#### registration_with_mat.sh
- permet d'effectuer le recalage
- **adaptation code** : changer la ligne 28 pour insérer le chemin vers le fichier `antsRegistration` 
- **usage** : 
	- général : `registration_with_mat.sh <fixed_folder> <moving_folder> <output_folder>`
	- exemple : `sh registration_with_mat.sh IBSR dataset_brain dataset_brain_reg`

#### apply_transformation.sh  
- permet de remettre le cerveau à partir des matrices de recalage. Permet d'obtenir des images recalées non skulled
- **adaptation code** : changer la ligne 26 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** 
	- général : `apply_transformation.sh <dataset_brain_reg_folder> <dataset_folder> <dataset_reg_folder>`
	- exemple : `sh apply_transformation.sh dataset_brain_reg dataset dataset_reg`

#### registration_seg.sh
- permet de faire le recalage inverse à partir des fichiers .mat du recalage direct. Images fixes : dataset_reg (contient les images IXI/OASIS/Kirby recalées non-skulled=les zones extérieures du cerveau ont été remises). Images mobiles : IBSR_seg (contient les images des atlas segmentées)
- **adaptation code** : changer la ligne 26 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** : `sh registration_seg.sh`

#### MajorityVoting.py
- A partir des images segmentées, il est possible de créer un atlas par le processus de majority voting. Pour chaque image d'origine, 18 images segmentées ont été crées et sont stockées dans un dossier.
- Le majority voting consiste à regarder, pour chaque pixel, quel label lui a été attribué dans les 18 images segmentées. Ensuite, le label qui lui a été le plus attribué est retenu. Le majority voting crée une image segmentée en prenant en compte le vote majoritaire des 18 images segmentées. 
- **usage**
	- général : `MajorityVoting.py <input_folder_seg> <output_folder>`
	- exemple : `MajorityVoting.py IXI_seg_IBSR IXI_majority`

### Normalisation
#### BiasCorrection.py
- permet de normaliser les images
- **usage**
	- général : `BiasCorrection.py [-h] input_dir output_dir`
	- exemple : `BiasCorrection.py [-h] dataset_reg dataset_reg_norm`

### Conversions

#### DICOM to nii file
- use dcm2niix
- ligne de commande : `dcm2niix -o /chemin/dossier/nii /chemin/dossier/dicom`

#### mgz to nii file
- Freesurfer command : `mri_convert image.mgz image.nii`

#### nii to mgz file
- Freesurfer command : `mri_convert image.nii image.mgz`

## Génération d'un texte associée à chaque image obtenue

### fichier csv
- décrit les coupes des volumes d'un patient
- nom des colonnes : nom du volume, axe (sagital, coronnal,..), numéro de coupe, keywords, description
