'''
 ____        _ _              ____            _       
|  _ \  __ _| | |       ___  | __ ) _ __ __ _(_)_ __  
| | | |/ _` | | |_____ / _ \ |  _ \| '__/ _` | | '_ \ 
| |_| | (_| | | |_____|  __/ | |_) | | | (_| | | | | |
|____/ \__,_|_|_|      \___| |____/|_|  \__,_|_|_| |_|
                                                      
 ____                _           
|  _ \ ___ _ __   __| | ___ _ __ 
| |_) / _ \ '_ \ / _` |/ _ \ '__|
|  _ <  __/ | | | (_| |  __/ |   
|_| \_\___|_| |_|\__,_|\___|_| 

Afficher une image .mgz
'''

# --------------------------------------------------------------------------------------------
# ** IMPORTS ** 

import nibabel as nib
from mayavi import mlab
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------------------
# ** CONSTANTES ** 

file_path = 'file.mgz'
img = nib.load(file_path).get_fdata()

# --------------------------------------------------------------------------------------------
# ** FUNCTIONS ** 

def hist(img):
    '''
    Affiche l'histogramme des niveaux de gris d'une image 3D MGZ.
    '''
    plt.hist(img.flatten(), bins=50, color='c', edgecolor='k', alpha=0.7)
    plt.title('Histogramme des niveaux de gris')
    plt.xlabel('Niveau de gris')
    plt.ylabel('Fréquence')
    plt.show()

def plot_2d(img, plane='axial', coord=None):
    """
    Affiche une coupe 2D d'une image 3D MGZ.
    Paramètres :
    - img : np.ndarray, Image 3D MGZ.
    - plane : str, optionnel, valeurs possibles : 'axial', 'coronal', 'sagittal', Plan de coupe.
    - coord : int, optionnel, Coordonnée de la coupe dans le plan spécifié (compris entre 0 et 256)
    """
    if plane not in ['axial', 'coronal', 'sagittal']:
        raise ValueError("Le plan doit être 'axial', 'coronal' ou 'sagittal'.")

    if coord is None:
        coord = img.shape[2] // 2

    if plane == 'axial':
        img_slice = img[:, :, coord]
    elif plane == 'coronal':
        img_slice = img[:, coord, :]
    elif plane == 'sagittal':
        img_slice = img[coord, :, :]

    plt.imshow(img_slice, cmap='gray')
    plt.title(f'Coupe {plane.capitalize()} à la coordonnée {coord}')
    plt.colorbar()
    plt.show()

# Afficher le volume en 3D
def plot_3d(img):
    mlab.pipeline.volume(mlab.pipeline.scalar_field(img))
    mlab.show()


# --------------------------------------------------------------------------------------------
# ** MAIN ** 

if __name__ == '__main__':

    plot_2d(img, plane='axial', coord=150) 