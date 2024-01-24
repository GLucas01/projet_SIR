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
│   │   │   ├── norm
│   │   │   └── seg
│   │   ├── Kirby_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg_inv
│   │   ├── Kirby_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── reg_norm
│   │   ├── Kirby_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── reg_norm
│   │   └── Kirby_OASIS
│   │       ├── reg
│   │       ├── reg_brain
│   │       ├── reg_inv
│   │       └── reg_norm
│   ├── T1
│   │   ├── IBSR
│   │   │   ├── brain
│   │   │   ├── NG
│   │   │   ├── norm
│   │   │   └── seg
│   │   ├── IBSR_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg
│   │   ├── IBSR_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg
│   │   ├── IBSR_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg
│   │   ├── IBSR_OASIS
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg
│   │   ├── OASIS
│   │   │   ├── brain
│   │   │   ├── NG
│   │   │   ├── norm
│   │   │   └── seg
│   │   ├── OASIS_IBSR
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   ├── reg_norm
│   │   │   └── seg_inv
│   │   ├── OASIS_IXI
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── reg_norm
│   │   ├── OASIS_Kirby
│   │   │   ├── reg
│   │   │   ├── reg_brain
│   │   │   ├── reg_inv
│   │   │   └── reg_norm
│   │   └── OASIS_OASIS
│   │       ├── reg
│   │       ├── reg_brain
│   │       ├── reg_inv
│   │       └── reg_norm
│   └── T2
│       ├── IXI
│       │   ├── brain
│       │   ├── NG
│       │   ├── norm
│       │   └── seg
│       ├── IXI_IBSR
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       │   ├── reg_norm
│       │   └── seg_inv
│       ├── IXI_IXI
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       │   └── reg_norm
│       ├── IXI_Kirby
│       │   ├── reg
│       │   ├── reg_brain
│       │   ├── reg_inv
│       │   └── reg_norm
│       └── IXI_OASIS
│           ├── reg
│           ├── reg_brain
│           ├── reg_inv
│           └── reg_norm
└── scripts

### Explication des noms de dossiers
- On appelera dataset IBSR,OASIS,IXI et Kirby

#### Dossiers dont le nom contient 1 dataset
- exemple de nomenclature : 
    ├── IXI
    │   ├── brain
    │   ├── NG
    │   ├── norm
    │   └── seg
- `NG` : contient les images originales IBSR/IXI/OASIS/Kirby en niveau de gris(NG)
- `brain` : contient les images originales IBSR/IXI/OASIS/Kirby en niveau de gris(NG) dont les zones extérieures du cerveau ont été enlevé (skulled)
- `norm` : contient les images originales IBSR/IXI/OASIS/Kirby en niveau de gris(NG) qui ont été normalisées
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
- `reg_norm` : images du moving dataset (ici IXI) recalées sur le fixed dataset (ici Kirby). norm indique que les images sont normalisées

##### Dossiers dont le nom contient 2 datasets, avec IBSR comme 1er nom
- Il faut mieux utiliser la segmentation de l'IBSR plutôt que la segmentation du 1er dataset
- exemple de nomenclature
├── IBSR_OASIS
│   ├── reg
│   ├── reg_brain
│   ├── reg_inv
│   ├── reg_norm
│   └── seg
- `reg`, `reg_brain`, `reg_inv`, `reg_norm` : cf paragraphe cas général
- `seg` : images de IBSR () segmentées qui ont été obtenues par recalage direct. Paramètres : fichier .mat (obtenu par recalage direct --> dans le dossier reg_brain). Fixes : images du fixed_dataset (ici IXI). Moving : images du moving_dataset segmentées (ici IBSR)

##### Dossiers dont le nom contient 2 datasets, avec IBSR comme 2ème nom
- exemple de nomencalture
    ├── IXI_IBSR
    │   ├── reg
    │   ├── reg_brain
    │   ├── reg_inv
    │   ├── reg_norm
    │   └── seg_inv
- `reg`, `reg_brain`, `reg_inv`, `reg_norm` : cf paragraphe cas général
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

#### registration_with_mat.sh
- permet d'effectuer le recalage
- **adaptation code** : changer la ligne 28 pour insérer le chemin vers le fichier `antsRegistration` 
- **usage** : 
	- général : `registration_with_mat.sh <fixed_folder> <moving_folder> <output_folder>`
	- exemple : `sh registration_with_mat.sh T1/IBSR/NG T1/OASIS/brain T1/OASIS_IBSR/reg_brain`

#### apply_transformation.sh  
- permet de remettre le cerveau à partir des matrices de registration
- **adaptation code** : changer la ligne 26 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** 
	- général : `apply_transformation.sh <dataset_brain_reg_folder> <dataset_folder> <dataset_reg_folder>`
	- exemple : `sh apply_transformation.sh T1/OASIS_IBSR/reg_brain T1/OASIS/NG T1/OASIS_IBSR/reg`

#### MajorityVoting.py
- A partir des images segmentées, il est possible de créer un atlas par le processus de majority voting. Pour chaque image d'origine, 18 images segmentées ont été crées et sont stockées dans le dossier namedb_seg_atlas.
- Le majority voting consiste à regarder, pour chaque pixel, quel label lui a été attribué dans les 18 images segmentées. Ensuite, le label qui lui a été le plus attribué est retenu. Le majority voting crée une image segmentée en prenant en compte le vote majoritaire des 18 images segmentées. 
- **usage**
	- général : `MajorityVoting.py <input_folder_seg> <output_folder>`
	- exemple : `MajorityVoting.py T1/OASIS_IBSR/seg_inv T1/OASIS/seg`

#### registration_seg.sh
- permet de faire le recalage inverse à partir des fichiers .mat (obtenu par recalage direct) inverse. Images fixes : T1/OASIS_IBSR/reg. Images mobiles : T1/IBSR/seg
- - **adaptation code** : changer la ligne 26 pour insérer le chemin vers le fichier `antsApplyTransforms`
- **usage** : `sh registration_seg.sh`


### Normalisation
#### BiasCorrection.py
- permet de normaliser les images
- **usage**
	- général : `BiasCorrection.py [-h] input_dir output_dir`
	- exemple : `BiasCorrection.py [-h] T1/OASIS_IBSR/reg T1/OASIS_IBSR/reg_norm`

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
