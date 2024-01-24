import sys
import os

if len(sys.argv) != 2:
    print("Usage: {} <InputFolder>".format(sys.argv[0]))
    sys.exit(1)

input_folder = sys.argv[1]

# Exécute le premier script
os.system("python3 slice_csv.py {}".format(input_folder))

# Exécute le deuxième script
folder_keywords = os.path.dirname(input_folder)
keywords = "Slice_csv"
folder_keywords = "{}/{}".format(folder_keywords, keywords)
os.system("python3 getKeywords.py {}".format(folder_keywords))

# Exécute le troisième script
folder_captions = os.path.dirname(input_folder)
slice_name = "Keywords"
folder_captions = "{}/{}".format(folder_captions, slice_name)
os.system("python3 ./Caption_Generation/en/gen_leg.py {}".format(folder_captions))
