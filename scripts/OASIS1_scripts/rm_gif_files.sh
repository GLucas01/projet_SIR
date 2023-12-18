#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <dossier>"
    exit 1
fi

dossier=$1

if [ ! -d "$dossier" ]; then
    echo "Le paramètre doit être un dossier existant."
    exit 1
fi

find "$dossier" -type f -name "*.gif" -exec echo {} \;
find "$dossier" -type f -name "*.gif" -exec rm {} \;


echo "Opération terminée : les fichiers .gif ont été supprimés."
