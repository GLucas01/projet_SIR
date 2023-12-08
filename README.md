# Projet SIR - Dall-e Brain

Un modèle génératif pour des images synthétiques de cerveau sain.

## Conversions

#### DICOM to nii file
- use dcm2niix
- ligne de commande : `dcm2niix -o /chemin/dossier/nii /chemin/dossier/dicom`

#### mgz to nii file
- Freesurfer command : `mri_convert image.mgz image.nii`

#### nii to mgz file
- Freesurfer command : `mri_convert image.nii image.mgz`

## Normalisation 

#### Comment faire la normalisation ?
- Utilisation de simpleITK ( librairie python )
- Il faut utiliser un "algorithme de De Correction Du Biais"
- Cf une étude dans Data/algosBias.pdf
- Utilisation de N4BiasFieldCorrectionImageFilter

#### Trouver la normalisation optimale avec N4filter de simpleITK
- Utilisation de Fijii, tracer un trait dans une zone
- Il suffit de regarder si la variation d'intensité des pixel le long du trait est grande ou non.
- Coordonnées du trait : x0,y0,x1,y1 = 116, 163, 188, 143 à la slice 100 (axe z, saggital)
- J'ai utilisé l'image : `IXI002-Guys-0828-MPRAGESEN_-s256_-0301-00003-000001-01.ni`
- Dans Fijii récupérer les intensités des pixel sur la ligne dans Analyse -> Plot profil -> Data -> Save data (obtention du fichier csv des valeurs)
- J'applique cela pour plusieurs images (tout dans ../Software/Fijii/)
- Pas de résultats significatifs, j'ai pourtant modifié les paramètres d'entrée pour le filtrage ...

#### Trouver la normalisation optimale avec mri_normalize de Freesurfer
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
- En utilisant elastix `sudo apt-get -y install elastix` 
- il faut utiliser la commande suivante : ``elastix -m moving_image.nii -f fixed_image.nii -p parameters.txt -out /output
- **Monomodale** : on compare T1 avec T1 ( information mutuelle )
- **Multimodale** : T1 avec flair ( différence nuance niveau de gris )
- on fait le recalage de l'image de la base de données ( moving image ) avec celle de l'atlas fixe
- pour paramters.txt il y a des exemples ici : https://github.com/SuperElastix/ElastixModelZoo/tree/master/models
- On pense que Par0035 est bien ( il ya du mono et multi modale )
- Sinom il existe d'autres fichiers de paramètre : Par0002, Par0009, Par0010, Par0035, Par0036, Par0039, Par0063, Par0064
- Pour obtenir l'image recalé : `transformix -in image.nii -tp outputDir/TransformParameters.0.txt -out outputDir/result`

#### ANTs
- installer ants avec le fichier .zip
- Le fichier `antsRegistrationSyN.sh` est le fichier necessaire pour le recadrage