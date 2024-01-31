# Transformation pour OASIS 1 

- Installer les données OASIS : https://www.oasis-brains.org/#data dans "download instructions"

- Se renseigner sur l'organisation des données : "fact sheet" 
	- les fichiers `...anon.nii` dans les dossiers RAW pour chaque patients sont des séquences d'images IRM brute
	- Les fichier `...anon_sbj_111` c'est la moyennes des images dans RAW et normalisé en voxel size (1x1x1mm)
	- Les fichiers `anon_111_t88_gfc` c'est la moyennes + une tranformation 'T88' + gain field corrector

## Convertir les images en .nii

- Utilisation de FSL : https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/Linux
- Utiliser la commande : `fslchfiletype NIFTI nom_fichier_sans_extension`
- Le script `convert_hdr_img_to_nii.sh` prends en paramètre un dossier, et applique cela pour tout les fichiers nécessaire.


## Rotation des images pour matcher avec l'image fixe

- Nous on a décidé de prendre des images fixe IBSR
- Leurs orientations sont constantes, et celles des images OASIS aussi  
- Je choisi donc d'utiliser FSL 
- les images `...anon.nii` & `...anon_sbj_111` ne sont pas bien orienté mais orienté identiquement, il faut leurs appliquer la transformation suivantes :
	`fslswapdim input.nii z -x y output.nii`
- les images `...anon_111_t88_gfc` ne sont pas bien orienté mais orienté identiquement, il faut leurs appliquer la transformation suivantes :
	`fslswapdim input.nii -x -y z output.nii`
- Le script `rotation_OASIS.sh` automatise cela en prenant également un dossier en paramètre


