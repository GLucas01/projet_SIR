# Rangement des fichiers

/data
    /IBSR_seg
    /Keywords
    /Keywords_csv
    /Slice_csv
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

# Extraction des informations des coupes pour chaque volume
*run in script*
python3 slice_csv.py <InputFolder>

En paramètre, le dossier contenant les volumes en format .nii.gz

### Attention : 
- Les volumes en niveau de gris recalé sur les IBSR doivent contenir "reg_IBSR" dans leurs noms et les labels seront extrait sur les segmentations de l'IBSR correspondant;
- Les volumes recalé sur les images IXI, OASIS ou Kirby21 doivent être les volume segmenté et doivent contenir "seg_IBSR" dans leurs noms;
- Les segmentations des images IXI, OASIS ou Kirby21 réalisé en majority voting après recalage de tout les IBSR doivent contenir "majority" dans leurs noms.


> output: ./data/Slice_csv/{modalite}/{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}.csv
Avec, Im_mov et Im_fix = T1, T2, FL ou IBSR
Avec modalite = T1, T2 ou FL en fonction de la base de donnée utilisée, respectivement OASIS, IXI ou Kirby21

Le contenu du fichier: [coupe, num coupe, dimensions,voxel, labels]
Exemple:IBSR_01_T2_035.csv
...
Coronal,33,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34750), (42, 66)]"
Coronal,34,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34555), (3, 19), (41, 10), (42, 232)]"
Coronal,35,"(256, 136)","(0.93750185, 0.93749905, 1.1999967)","[(0, 34273), (3, 129), (41, 23), (42, 391)]"
...


# Création des mot-clés pour chaque coupe
*run in script*
python3 getKeywords.py <InputFolder>

En paramètre, le dossier contenant les fichiers csv extraits (Slice_csv)

> output: ./data/Keywords_csv/{modalite}/{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}_header.csv
> output: ./data/Keywords_csv/{modalite}/{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}_coupes.csv

Le contenu du fichier header: [modalite, genre_mov, age_mov, genre_fix, genre_fix, Sx, Sy, Sz]
Exemple:IBSR_01_T2_035_header.csv
modalite,genre_mov,age_mov,genre_fix,genre_fix,Sx,Sy,Sz
T2,M,37,F,"37,14",0.93750185,0.93749905,1.1999967

Le contenu du fichier coupes: [coupe, num coupe, dimensions, labels]
Exemple:IBSR_01_T2_035_coupes.csv
...
Coronal,31,"(256, 136)","[('Unknown', '36719.9343')]"
Coronal,32,"(256, 136)","[('Unknown', '36719.9343')]"
Coronal,33,"(256, 136)","[('Unknown', '36650.3250'), ('cortex of right cerebral hemisphere', '69.6093')]"
...

# Création des descriptions
*run in script*
python3 ./Caption_Generation/en/gen_leg.py <InputFolder>

En paramètre, le dossier contenant les fichiers csv header et coupes (Keywords_csv)

> output: ./data/Keywords_csv/{modalite}/{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}/{Im_mov}_{ID_mov}_{Im_fix}_{ID_fix}_{coupe}_{num coupe}.csv

Les fichiers de sorties contiennent une seule colonne avec 5 descriptions différentes associées à une coupe

### La version française n'est pas à jour

