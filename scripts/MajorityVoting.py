import SimpleITK as sitk
import sys
import os
import glob

if len(sys.argv) > 1:
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
else:
    print("Usage: MajorityVoting.py <input_folder> <output_folder>\nThe images in the input_folder msut be segmented")
    sys.exit(1)

all_files = glob.glob(os.path.join(input_folder, "*.nii"))

file_groups = {}
for filename in all_files:
    prefix=os.path.basename(filename).split('_')[0]
    if prefix not in file_groups:
        file_groups[prefix] = []
    file_groups[prefix].append(filename)

for prefix, files in file_groups.items(): #itération sur chaque patient
    images = []

    reference_image=files[0]


    # itération sur chque fichier de recalage
    for filename in files:
        path=os.path.join(input_folder, filename)
        img=sitk.ReadImage(path, sitk.sitkUInt32)
        images.append(img)
        #print(f"Image: {filename}")
        #print(f"Origin: {img.GetOrigin()}")
        #print(f"Spacing: {img.GetSpacing()}")

    for i in range(1, len(images)):
        images[i].SetOrigin(images[0].GetOrigin())
        images[i].SetSpacing(images[0].GetSpacing())


    label_voting_filter = sitk.LabelVotingImageFilter()
    result_image = label_voting_filter.Execute(images)
    sitk.WriteImage(result_image, os.path.join(output_folder, prefix + "_majority.nii.gz"))
    print(f"Majority Voting effectué sur les images du patient: {prefix}")
