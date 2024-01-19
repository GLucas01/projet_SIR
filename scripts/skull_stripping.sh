#!/bin/bash

# Vérifier si le nombre d'arguments est correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dossier>"
    exit 1
fi

# Récupérer le nom du dossier passé en paramètre
dossier="$1"

# Vérifier si le dossier existe
if [ ! -d "$dossier" ]; then
    echo "Le dossier '$dossier' n'existe pas."
    exit 1
fi

# Parcourir tous les fichiers du dossier et appliquer la commande
for fichier in "$dossier"/*; do
    # Vérifier si le fichier est un fichier régulier
    if [ -f "$fichier" ]; then
        # Extraire le nom du fichier sans le chemin ni l'extension
        nom_fichier=$(basename "$fichier" .nii.gz)
        
        # Appliquer la commande sur le fichier
        bet "$fichier" "${nom_fichier}_brain.nii.gz"
        
        # Afficher un message indiquant le traitement du fichier
        echo "La commande a été appliquée sur le fichier $fichier."
    fi
done

echo "Le traitement du dossier '$dossier' est terminé."
