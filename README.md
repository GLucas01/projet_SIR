# Projet SIR - Dall-e Brain

Un modèle génératif pour des images synthétiques de cerveau sain.

![alt text](logo.png)

## Structure de la base de données (sur clé USBs)
### Arborescence utilisée
├── data
│   ├── FL
│   │   ├── Kirby
│   │   │   ├── brain
│   │   │   ├── NG
│   │   │   └── seg
│   │   ├── Kirby_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg_inv
│   │   ├── Kirby_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   ├── Kirby_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   └── Kirby_OASIS
│   │       ├── reg
│   │       ├── reg_brain
│   │       ├── reg_inv
│   ├── T1
│   │   ├── IBSR
│   │   │   ├── brain
│   │   │   ├── NG
│   │   │   └── seg
│   │   ├── IBSR_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg
│   │   ├── IBSR_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg
│   │   ├── IBSR_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg
│   │   ├── IBSR_OASIS
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg
│   │   ├── OASIS
│   │   │   ├── brain
│   │   │   ├── NG
│   │   │   └── seg
│   │   ├── OASIS_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── seg_inv
│   │   ├── OASIS_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   ├── OASIS_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   └── OASIS_OASIS
│   │       ├── reg
│   │       ├── reg_brain
│   │       ├── reg_inv
│   └── T2
│       ├── IXI
│       │   ├── brain
│       │   ├── NG
│       │   └── seg
│       ├── IXI_IBSR
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       │   └── seg_inv
│       ├── IXI_IXI
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       ├── IXI_Kirby
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       └── IXI_OASIS
│           ├── reg
│           ├── reg_brain
│           ├── reg_inv
└── scripts

### Explication des noms de dossiers
- On appelera dataset IBSR,OASIS,IXI et Kirby
- par défaut, tous les fichiers sont normalisés

#### Dossiers dont le nom contient 1 dataset
- exemple de nomenclature : 
    ├── IXI
    │   ├── brain
    │   ├── NG
    │   ├── norm
    │   └── seg
- `NG` : contient les images originales IBSR/IXI/OASIS/Kirby en niveau de gris(NG)
- `brain` : contient les images originales IBSR/IXI/OASIS/Kirby en niveau de gris(NG) dont les zones extérieures du cerveau ont été enlevé (skulled)
- `seg` : contient les segmentations des images originales IBSR/IXI/OASIS/Kirby. IBSR est l'atlas que nous avons téléchargé depuis internet donc les segmentations sont connues au départ. Pour les images IXI/OASIS/Kirby, les segmentations des images sont obtenues par majority voting à partir du dossier `seg_inv`

#### Dossiers dont le nom contient 2 datasets
- nom : `moving_fixed`. Par exemple pour `IXI_IBSR`, IXI sont les images mobiles (moving dataset) et IBSR les images fixes (fixed dataset)

##### Dossiers dont le nom contient 2 datasets, cas général
- exemple de nomencalture
    ├── IXI_Kirby
    │   ├── reg
    │   ├── reg_brain
    │   ├── reg_inv
    │   └── reg_norm
- `reg` : images du moving dataset (ici IXI) recalées sur le fixed dataset (ici Kirby).
- `reg_brain` : images du moving dataset (ici IXI) recalées sur le fixed dataset (ici Kirby). brain indique que les zones extérieures du cerveau ont été enelvé
- `reg_inv` : images obtenues par recalage inverse. Paramètres : fichier .mat (obtenu par recalage direct) inverse. Fixes : images du moving_dataset (ici IXI). Moving : images du fixed_dataset en niveau de gris (ici Kirby)

##### Dossiers dont le nom contient 2 datasets, avec IBSR comme 1er nom
- Il faut mieux utiliser la segmentation de l'IBSR plutôt que la segmentation du 1er dataset
- exemple de nomenclature
├── IBSR_OASIS
│   ├── reg
│   ├── reg_brain
│   ├── reg_inv
│   ├── reg_norm
│   └── seg
- `reg`, `reg_brain`, `reg_inv` : cf paragraphe cas général
- `seg` : images de IBSR () segmentées qui ont été obtenues par recalage direct. Paramètres : fichier .mat (obtenu par recalage direct --> dans le dossier reg_brain). Fixes : images du fixed_dataset (ici IXI). Moving : images du moving_dataset segmentées (ici IBSR)

##### Dossiers dont le nom contient 2 datasets, avec IBSR comme 2ème nom
- exemple de nomencalture
    ├── IXI_IBSR
    │   ├── reg
    │   ├── reg_brain
    │   ├── reg_inv
    │   ├── reg_norm
    │   └── seg_inv
- `reg`, `reg_brain`, `reg_inv` : cf paragraphe cas général
- `seg_inv` : images du moving dataset segmentées qui ont été obtenues par recalage inverse. Paramètres : fichier .mat (obtenu par recalage direct) inverse. Fixes : images du moving_dataset (ici IXI). Moving : images du fixed_dataset segmentées (ici IBSR)

## Scripts de traitement sur les images (rotation, recalage, normalisation, nouveaux atlas)

### Rotations
- Utilisation de FSL 
- Commande : `fslswapdim input.nii x y z output.nii`
- pour la dataset OASIS, rotation constante qui est la suivante : `fslswapdim input.nii z -x y output.nii`

### Recalage

#### skull_stripping.sh
- permet d'enlever les zones extérieures du cerveau . Les images obtenues sont "skulled"
- **usage** :
	- général : `skull_stripping.sh <dossier>`

#### reg.sh
- permet d'effectuer le recalage
- **adaptation code** : changer la ligne 31 pour insérer le chemin vers le fichier `antsRegistration` 
- **usage** : 
	- général : `reg.sh <fixed_folder> <moving_folder> <output_folder>`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data/T1/IBSR_IXI `sh /media/julie/Intenso/SIR/scripts/reg.sh /media/julie/Intenso/SIR/data/T2/IXI/brain/ /media/julie/Intenso/SIR/data/T1/IBSR/brain reg_brain/`


#### convert_brain_reg_to_reg.sh  
- permet de remettre le cerveau à partir des matrices de registration
- **adaptation code** : changer la ligne 45 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** 
	- général : `convert_brain_reg_to_reg.sh <brain_reg_folder> <reg_folder> <NG_mov_folder> <NG_fix_folder>`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data/T1/IBSR_IXI `sh /media/julie/Intenso/SIR/scripts/convert_brain_reg_to_reg.sh reg_brain reg /media/julie/Intenso/SIR/data/T1/IBSR/NG /media/julie/Intenso/SIR/data/T2/IXI/NG`

#### MajorityVoting.py
- A partir des images segmentées, il est possible de créer un atlas par le processus de majority voting. Pour chaque image d'origine, 18 images segmentées ont été crées et sont stockées dans le dossier namedb_seg_atlas.
- Le majority voting consiste à regarder, pour chaque pixel, quel label lui a été attribué dans les 18 images segmentées. Ensuite, le label qui lui a été le plus attribué est retenu. Le majority voting crée une image segmentée en prenant en compte le vote majoritaire des 18 images segmentées. 
- **usage**
	- général : `MajorityVoting.py <input_folder_seg> <output_folder>`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data `python3 /media/julie/Intenso/SIR/scripts/MajorityVoting.py T1/OASIS_IBSR/seg_inv T1/OASIS/seg`

#### seg_inv.sh
-  Tout d’abord, nous avons effecue un recalage d’une image d’une base de donnee, par exemple OASIS (image mobile) sur une image d’un atlas, par exemple IBSR (image fixe). Ce recalage a pour resultat :
	- une image d’une base de donnee (par exemple OASIS) recalee sur une image d’un atlas (par exemple IBSR) en niveau de gris
	- un fichier .mat stockant les parametre du recalage
- L’application inverse du fichier .mat permet alors de recaler une image segmentée d’un atlas (par exemple IBSR) sur l’image de la base de donnee (par exemple OASIS) precedemment recalee.
- Les images resultantes de ce recalage inverse sont donc des images de la base de donnee d’origine (par exemple OASIS) qui sont segmentees.
- Ainsi, si l’on a n images OASIS et 18 IBSR, on obtient 18 images OASIS recalées par recalage ”direct”. Avec le recalage inverse, il est possible d’obtenir nx18 images segmentees OASIS
- **adaptation code** : changer la ligne 29 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** : 
	- général : `seg_inv.sh <fixed/seg folder> <moving_fixed/seg_inv folder> <moving/brain folder> <moving_fixed/reg_brain folder>`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data/T1/OASIS_IBSR$ `sh /media/julie/Intenso/SIR/scripts/seg_inv.sh /media/julie/Intenso/SIR/data/T1/IBSR/seg/ seg_inv/ /media/julie/Intenso/SIR/data/T1/OASIS/brain/ reg_brain/`

####  reg_inv_NG
- Tout d’abord, nous avons effecue un recalage d’une image d’une base de donnee, par exemple Kirby (image mobile) sur une image d’un atlas, par exemple IXI (image fixe). Ce recalage a pour resultat :
	- une image d’une base de donnee (par exemple Kirby) recalee sur une image d’un atlas (par exemple IXI) en niveau de gris
	- un fichier .mat stockant les parametre du recalage
- L’application inverse du fichier .mat permet alors de recaler une image en NG d’un atlas (par exemple IXI) sur l’image de la base de donnee en niveau de gris(par exemple Kirby).
- **adaptation code** : changer la ligne 45 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage**
	- général : `reg_inv_NG_new.sh <fixed_NG_folder> <moving_NG_folder> <moving_fixed_reg_brain_folder> <moving_fixed_reg_inv_folder>`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data/T2/Kirby_IXI `bash /media/julie/Intenso/SIR/scripts/reg_inv_NG_new.sh /media/julie/Intenso/SIR/data/T2/IXI/NG /media/julie/Intenso/SIR/data/FL/Kirby/NG reg_brain reg_inv`

### Normalisation
#### BiasCorrection.py
- permet de normaliser les images
- **usage**
	- général : `BiasCorrection.py [-h] input_dir output_dir`
	- exemple : julie@julie-ThinkPad:/media/julie/Intenso/SIR/data `python3 /media/julie/Intenso/SIR/scripts/BiasCorrection.py [-h] T1/OASIS_IBSR/reg T1/OASIS_IBSR/reg_norm`

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
