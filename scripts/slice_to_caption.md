# Rangement des fichiers

/data
    /T1
        /OASIS_IBSR
            /reg
            /Slice_csv
            /Keywords
            /Captions

/script
    slice_csv.py
    getKeywords.py
    /Caption_Generation
        /en
            gen_leg.py
            generic_leg.txt
        /fr
            gen_leg_fr.py
            Phrases_generique.txt

# Execution
python3 slice_to_caption.py <InputFolder>

## Extraction des informations des coupes pour chaque volume
*run in script*

python3 slice_csv.py <InputFolder>

En paramètre, le dossier contenant les volumes en format .nii.gz

### Attention : 
- Les volumes en niveau de gris doivent contenir "reg" dans leurs noms et les labels seront extrait sur les segmentations correspondantes
- Les volumes segmenté doivent contenir "seg" dans leurs noms
- Les segmentations des images IXI, OASIS ou Kirby21 réalisé en majority voting après recalage de tout les IBSR doivent contenir "majority" dans leurs noms.


> output: Slice_csv/{BD_mov}_{ID_mov}_{BD_fix}_{ID_fix}.csv
Avec, BD_mov et BD_fix = OAS, IXI, KKI ou IBSR


Le contenu du fichier: [coupe, num coupe, dimensions,voxel, labels]
Exemple:
...
Coronal,33,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34750), (42, 66)]"
Coronal,34,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34555), (3, 19), (41, 10), (42, 232)]"
Coronal,35,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34273), (3, 129), (41, 23), (42, 391)]"
...


## Création des mot-clés pour chaque coupe
*run in script*

python3 getKeywords.py <InputFolder>

En paramètre, le dossier contenant les fichiers csv extraits (Slice_csv)

> output: Keywords/{BD_mov}_{ID_mov}_{BD_fix}_{ID_fix}_header.csv
> output: Keywords/{BD_mov}_{ID_mov}_{BD_fix}_{ID_fix}_coupes.csv

Le contenu du fichier header: [modalite, genre_mov, age_mov, genre_fix, genre_fix, Sx, Sy, Sz]
Exemple:
modalite,genre_mov,age_mov,genre_fix,genre_fix,Sx,Sy,Sz
T2,M,37,F,"37,14",0.93750185,0.93749905,1.1999967

Le contenu du fichier coupes: [coupe, num coupe, dimensions, labels]
Exemple:
...
Coronal,31,"(256, 136)","[('Unknown', '36719.9343')]"
Coronal,32,"(256, 136)","[('Unknown', '36719.9343')]"
Coronal,33,"(256, 136)","[('Unknown', '36650.3250'), ('cortex of right cerebral hemisphere', '69.6093')]"
...

## Création des descriptions
*run in script*

python3 ./Caption_Generation/en/gen_leg.py <InputFolder>

En paramètre, le dossier contenant les fichiers csv header et coupes (Keywords)

> output: Captions/{BD_mov}_{ID_mov}_{BD_fix}_{ID_fix}/{BD_mov}_{ID_mov}_{BD_fix}_{ID_fix}_{coupe}_{num coupe}.csv

Les fichiers de sorties contiennent une seule colonne avec 5 descriptions différentes associées à une coupe

### La version française n'est pas à jour

