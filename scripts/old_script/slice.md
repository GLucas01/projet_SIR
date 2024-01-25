# Coupe celon quel axe ?

Taille IXI: (256, 256, 136)

Taille IBSR: (256, 256, 128)
Taille IBSR seg: (256, 128, 256)
Taille array IBSR seg: (256, 128, 256)
Résolution spatiale IBSR seg: (0.9375, 1.5, 0.9375)

## IXI recalé sur l'IBSR
Taille Transformé direct: (256, 256, 128)


## IBSR recalé sur IXI
Taille Transformé inverse: (256, 256, 136) -> nombre de pixel dans l'image
Taille array Transformé inverse: (136, 256, 256) -> 
Résolution spatiale Transformé inverse: (0.937501847743988, 0.9374990463256836, 1.1999967098236084)

Matrice de direction Transformé inverse :
(0.9993601557127837, -0.005650310282313015, -0.03531789292883241, 4.327564225095288e-06, -0.9874239323427557, 0.1580948432144248, 0.035767012106032114, 0.15799383478630602, 0.9867921093057412)

Résolution spatiale Transformé inverse: (0.937501847743988, 0.9374990463256836, 1.1999967098236084)

Taille array Transformé inverse après transposition : (256, 256, 136)
=> il faut transposé les dimension numphy dans les directions de simpleITK

# Passage en array ne conserve pas la direction !

Utilisation de la bibliothèque nibabel

slice_data = nifti_data[slice_index, :, :] # sagittal plane
slice_data = nifti_data[:, slice_index, :] # coronal plane
slice_data = nifti_data[:, :, slice_index] # axial plane

Taille Transformé inverse: (256, 256, 136)
Taille array Transformé inverse: (136, 256, 256)
Taille nib Transformé inverse: (256, 256, 136)
