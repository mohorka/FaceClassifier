from matplotlib import image
import numpy as np
from dataclasses import dataclass

@dataclass
class Photo:
    """Class for representation of image data"""    
    image: np.array
    label: int
