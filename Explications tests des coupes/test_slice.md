# Test de différentes méthodologies de création de coupe

Une des problématiques qui ont avons est de savoir si les coupes qui nous créons correspondent bien aux coupes axiale, coronale et sagittale. DE plus, comment savoir si les segmentations seront adaptées aux coupes en niveau de gris sachant que nous les enregistrons pas ?

Voici une présentation de plusieurs méthodologies de création de coupe que nous avons tester sur des volumes IXI recalé sur IXI.

## Librairie Nibabel

### Niveau de gris
 
Les coupes sont faites celon les même procéder pour les image en niveau de gris et les segmentations pour obtenir les csv

#### slice_NG.py
Prend un volume en niveau de gris en entrée et crée toutes les coupes avec la librairie nibabel. Ce code applique la fonction `fdata` de nibabel sur le volume avant de créer les coupes, puis reforme des images avec `nib.Nifti1Image`

IXI_476_IXI_293_axial_64.nii.gz  
![Alt text](image-3.png)  

IXI_476_IXI_293_coronal_101.nii.gz  
![Alt text](image-4.png)  

IXI_476_IXI_293_sagittal_150.nii.gz
![Alt text](image-5.png)   

#### slice_NG_without_fdata.py
Prend un dossier en entrée contenant des volumes en niveau de gris, séléctionne un volume au hasard et extrait toutes les coupes. Ce code crée les coupes celon la fonction `slicer` de nibabel, et du coup n'a pas besoin de recréer une image nifti.

IXI_424_IXI_305_axial_80.nii.gz  
![Alt text](image-6.png)  

IXI_424_IXI_305_coronal_94.nii.gz  
![Alt text](image-7.png)  

IXI_424_IXI_305_sagittal_104.nii.gz  
![Alt text](image-8.png)  

### CSV

#### slice_csv.py
Prend un dossier en entrée contenant des volumes en niveau de gris et créer tout les csv regroupant toutes les informations dans les coupes de tout les volume du dossier.
Ce code applique la fonction `fdata` de nibabel sur le volume segmenté de l'image fixe avant de créer les coupes, et extrait les informations avec `np.unique`

IXI_035_IXI_233.csv
![Alt text](image.png)

coronal,90,"(256, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26787), (2, 832), (3, 1916), (7, 28), (8, 1072), (41, 764), (42, 1909), (46, 58), (47, 1033), (73, 417)]"  
coronal,91,"(256, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26648), (2, 813), (3, 1988), (7, 55), (8, 1073), (41, 792), (42, 1931), (46, 69), (47, 1043), (73, 404)]"


#### slice_csv_ fdata_after_slicer.py
Prend un dossier en entrée contenant des volumes en niveau de gris et créer tout les csv regroupant toutes les informations dans les coupes de tout les volume du dossier.
Ce code applique la fonction `slicer` de nibabel sur le volume segmenté de l'image fixe, applique la fonction `fdata` sur ces coupes et extrait les informations avec `np.unique`

*met plus longtemps à s'éxecuter*  
IXI_035_IXI_233.csv
![Alt text](image-1.png)

coronal,90,"(256, 1, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26787), (2, 832), (3, 1916), (7, 28), (8, 1072), (41, 764), (42, 1909), (46, 58), (47, 1033), (73, 417)]"  
coronal,91,"(256, 1, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26648), (2, 813), (3, 1988), (7, 55), (8, 1073), (41, 792), (42, 1931), (46, 69), (47, 1043), (73, 404)]"


#### Conclusion
Se sont les même éléments mais comment savoir si c'est bien la coronal dans les deux cas sans regader le niveau de gris à chaque fois ?

## LIbrairie SimpleITK
### Niveau de gris
*choisis un fichier au hasard dans le dossier et exporte toutes les coupes de ce volume*
#### slice_NG_sitk.py
Prend un dossier en entrée contenant des volumes en niveau de gris, séléctionne un volume au hasard et extrait toutes les coupes. Ce code crée les coupes selon `image_slice = image[i, :, :]`

Apparition de cette erreur:  
WARNING: In /tmp/SimpleITK-build/ITK/Modules/IO/NIFTI/src/itkNiftiImageIO.cxx, line 2191
NiftiImageIO (0x55b245dbfc10): Non-orthogonal direction matrix coerced to orthogonal

IXI_476_IXI_293_axial_93.nii.gz  
![Alt text](image-9.png)  

IXI_476_IXI_293_coronal_103.nii.gz  
![Alt text](image-10.png)  

IXI_476_IXI_293_sagittal_103.nii.gz  
![Alt text](image-11.png)  

### CSV

#### slice_csv_sitk.py
Prend un dossier en entrée contenant des volumes en niveau de gris et créer tout les csv regroupant toutes les informations dans les coupes de tout les volume du dossier.
Ce code crée les coupes selon `image_slice = image[i, :, :]` du le volume segmenté de l'image fixe, applique la fonction `GetArrayFromImage` de SimpleITK sur ces coupes et extrait les informations avec `np.unique` 

IXI_035_IXI_233.csv
![Alt text](image-2.png)

coronal,90,"(256, 136)","(0.9375132322311401, 0.9375060200691223, 1.2000031471252441)","[(0, 26787), (2, 832), (3, 1916), (7, 28), (8, 1072), (41, 764), (42, 1909), (46, 58), (47, 1033), (73, 417)]"  
coronal,91,"(256, 136)","(0.9375132322311401, 0.9375060200691223, 1.2000031471252441)","[(0, 26648), (2, 813), (3, 1988), (7, 55), (8, 1073), (41, 792), (42, 1931), (46, 69), (47, 1043), (73, 404)]"

### Conclusion
A première vue, le csv semblent être la même chose.
