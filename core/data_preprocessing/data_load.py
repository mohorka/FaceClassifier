from typing import List
from core.models.photo import Photo
import os
from PIL import Image
import numpy as np
from core.config.config import DATA_DIR

def load_data(with_labels:bool=False) -> List[Photo]:
    """Loads data from local directory.

    Returns:
        List[Photo]: List of objects, which consist of image and its label
    """   
    faces = []
    for i in range(1,42,1):
        directory = os.fsdecode(DATA_DIR+str(i))
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            photo = Image.open(DATA_DIR+str(i)+'/'+filename)
            photo = photo.convert('L')
            photo = np.array(photo, dtype=np.uint8)
            faces.append(Photo(photo,i))
    return faces
    #add saving by groups