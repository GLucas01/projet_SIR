# Projet SIR - Dall-e Brain

## Normalisation 
- Utilisation de simpleITK ( librairie python )
- Il faut utiliser un "algorithme de De Correction Du Biais" (très subtile...)
- Cf une étude dans Data/algosBias.pdf
- Utilisation de N4BiasFieldCorrectionImageFilter

## Recalage
- "ANTs, fsl, freesrufer et elastix sont tous capables de faire de bon recalage directement à partir des images. Pour le recalage déformable, ANTs semble être un peu mieux." 
- En utilisant elastix `sudo apt-get -y install elastix` 
- il faut utiliser la commande suivante : ``elastix -m moving_image.nii -f fixed_image.nii -p parameters.txt -o /output
- pour paramters.txt il y a des exemples ici : https://github.com/SuperElastix/ElastixModelZoo/tree/master/models
- Pour obtenir l'image recalé : `transformix -in image.nii -tp outputDir/TransformParameters.0.txt -out outputDir/result`