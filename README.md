# Projet SIR - Dall-e Brain

Un modèle génératif pour des images synthétiques de cerveau sain.

![alt text](/home/thomas/Documents/GitHub/projet_SIR/logo.png)

## Conversions

#### DICOM to nii file
- use dcm2niix
- ligne de commande : `dcm2niix -o /chemin/dossier/nii /chemin/dossier/dicom`

#### mgz to nii file
- Freesurfer command : `mri_convert image.mgz image.nii`

#### nii to mgz file
- Freesurfer command : `mri_convert image.nii image.mgz`

## Normalisation 

####  Normalisation avec N4filter de simpleITK
- Cf script biasCorrector.py
- Sa normalise et lisser les nuances dans les tissus

#### Normalisation avec mri_normalize de Freesurfer
- faut utiliser `mri_normalize image.mgz image_norm.mgz` et ça marche
- Les nuances de gris sont "amplifié" mais c'est bien normalisé !
- `mri_normalize` amplifie uniquement le white matter, je ne sais pas si c'est bien ou pas
- Mais j'ai trouver https://justinblaber.org/t1-intensity-normalization/ qui devrait me permettre de normaliser les intensitée suivantes : white matter ~ 110 / grey matter ~80 / csf ~ 35 qui utilise les commandes suivantes à parir d'une image T1.mgz:
```bash
mri_convert T1.nii.gz T1.mgz
mri_nu_correct.mni --i T1.mgz --o T1_N3.mgz --n 2
mri_normalize -g 1 -mprage T1_N3.mgz T1_norm.mgz
mri_convert T1_norm.mgz T1_norm.nii.gz
```
- Par contre il est necessaire d'utiliser une image T1 en entrée dans sa méthode (peut on le faire avec T2 et Flair ?)


## Recalage

#### Elastix & Transformix
- On a abandonné car pas ouf

#### ANTs
- installer ants avec le fichier .zip
- Le fichier `antsRegistrationSyN.sh` est le fichier necessaire pour le recadrage
- C'est bien j'utilise une interpolation linéaire, une transformation rigide et je fais du skull stripping (commande FSL : `bet input output`) au préalable sur les images mobiles T2 et FLAIR car mes images fixes sont tous en T1 et si je fais pas ça le recalage n'est pas optimal.

## Rotations
- Utilisation de FSL 
- Commande : `fslswapdim input.nii x y z output.nii`

## Redimensionnement voxel size
- Nous ont veux avoir toutes les images en **1x1x1** comme ça c'est normalisé
- On peut modifer une image qui n'est pas en 1x1x1 avec **FSL** : 
	`fslchpixdim input_image 1 1 1 output_image`
- Il peut y avoir des impacts d'interpolation :
	- perte de résolution
	- Modification intensité voxels
- Il faut trouver un méthode pour palié à cela ...

## Augmentation de données ?
- Il suffit simplement de recaler une images sur plusieurs IBSR ( y'en a 18 donc on peut faire x18 la dataset )

## Nomenclature
### Architecture des fichiers
├── T1
│   ├── Patient 1
│   │   ├── movingimage_fixedimage1.nii
│   │   ├── movingimage_fixedimage2.nii
│   │   ├── movingimage_fixedimage3.nii
│   │   ├── movingimage.csv
│   ├── Patient 2
│   │   ├── etc
│   ├── Patient 3
│   │   ├── etc
│   ├── etc
├── T2
│   ├── etc
├── Flair
│   ├── etc

### fichier csv
- décrit les coupes des volumes d'un patient
- nom des colonnes : nom du volume, axe (sagital, coronnal,..), numéro de coupe, keywords, description
