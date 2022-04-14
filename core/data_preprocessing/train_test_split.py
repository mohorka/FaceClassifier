from typing import List, Tuple
from core.models.photo import Photo
from random import shuffle

def train_test_split(data: List[Photo], proportion:float = 30, _shuffe:bool = True,with_labels:bool=False) -> Tuple[List[Photo], List[Photo], str] :
    """Split data to train and split

    Args:
        data (List[Photo]): List of photos
        proportion (float, optional): Define the size of train data. Defaults to 0.3.
        _shuffe (bool, optional): Shuffle data. Defaults to True
    Returns:
        Tuple[List[Photo], List[Photo], str] : Returns lists of train and test and error message, if smth wrong with split
    """ 
    proportion /= 100
    train= []
    test = []
    err = None
    if _shuffe:
        shuffle(data)
    border = int(len(data) * proportion)
    print("Border is ", border)
    if border == 0:
        err = 'Attention, according to given proportion, train contains no elements'
    if border == len(data):
        return data, data, err
    train = data[0:border:1]
    test = data[border::1]

    return train, test, err