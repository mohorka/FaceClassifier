DATA_DIR = './data/'
RESULTS_PATH = './results/'
METHODS = ['hist', 'grad', 'dft', 'dct','scale']
NUM_IMG_PER_GROUP = 10

#change
METHODS_PARAMS = {
    "scale": {"name": "l", "default": "2", "range": (2, 10)},
    "hist": {"name": "BIN", "default": "32", "range": (8, 65)},
    "grad": {"name": "W", "default": "10", "range": (4, 31)},
    "dft": {"name": "P", "default": "20", "range": (6, 31)},
    "dct": {"name": "P", "default": "20", "range": (6, 31)},
}