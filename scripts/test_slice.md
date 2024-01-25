# Nibabel

## Niveau de gris
*choisis un fichier au hasard dans le dossier et exporte toutes les coupes de ce volume*
### slice_NG.py

### slice_NG_without_fdata.py

### Conclusion

## CSV

### slice_csv.py
IXI_035_IXI_233.csv
![Alt text](image.png)

coronal,90,"(256, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26787), (2, 832), (3, 1916), (7, 28), (8, 1072), (41, 764), (42, 1909), (46, 58), (47, 1033), (73, 417)]"
coronal,91,"(256, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26648), (2, 813), (3, 1988), (7, 55), (8, 1073), (41, 792), (42, 1931), (46, 69), (47, 1043), (73, 404)]"


### slice_csv_ fdata_after_slicer.py
*met plus longtemps à s'éxecuter*
IXI_035_IXI_233.csv
![Alt text](image-1.png)

coronal,90,"(256, 1, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26787), (2, 832), (3, 1916), (7, 28), (8, 1072), (41, 764), (42, 1909), (46, 58), (47, 1033), (73, 417)]"
coronal,91,"(256, 1, 136)","(0.93751323, 0.937506, 1.2000031)","[(0, 26648), (2, 813), (3, 1988), (7, 55), (8, 1073), (41, 792), (42, 1931), (46, 69), (47, 1043), (73, 404)]"


### Conclusion
Se sont les même éléments mais comment savoir si c'est bien la coronal dans les deux cas sans regader le niveau de gris à chaque fois ?