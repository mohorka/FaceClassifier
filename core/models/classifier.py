from typing import Callable, List, Optional, Tuple
import core.data_preprocessing.feature_extraction as fe


import numpy as np

from core.models.photo import Photo

class Classifier:
    def __init__(self, method: str) -> None:
        self.method = method,
        self.references: List[Photo] = []
    
    
    def __get_feature(self,image:np.array):
        print(self.method)
        if self.method[0] == 'scale':
            #print('shape of original ', image.shape)
            #print('Shape of sifted ',fe.sift(image).shape)
            return fe.scale(image, self.param)
        elif self.method[0] == 'hist':
            return fe.histogram(image, self.param)
        elif self.method[0] == 'dft':
            return fe.dft(image, self.param)
        elif self.method[0] == 'dct':
            return fe.dct(image, self.param)
        elif self.method[0] == 'grad':
            return fe.laplac_grad(image, self.param)
        else:
            print('smth wrong')
            return

    
    def __loss(self, reference_feature:np.array, test_feature:np.array):
        #return np.linalg.norm(reference_feature-test_feature)
        return np.linalg.norm(np.subtract(reference_feature,test_feature))
    
    def __multi_loss(self, reference_features:dict, test_features:dict, weights:Optional[np.array]):
        ref_values = np.array(reference_features.values())
        test_values = np.array(test_features.values())
        diff = ref_values - test_values
        losses = []
        for each in diff:
            losses.append(np.linalg.norm(each))
            if len(weights) == len(diff):
                losses *= weights
                loss = np.sum(losses) / np.sum(weights)
            else:
                loss = np.sum(losses) / len(losses)
        return loss
    
    def __search(self, test:np.array):
        min_loss = np.inf
        reference = None
        #template_group= None
        for ref in (self.references):
            if (loss := self.__loss(ref.image,test)) < min_loss:
                min_loss = loss
                reference = ref

        return reference
    
    def fit(self, data: List[Photo], param: int):
        self.param = param
        references = []
        for photo in data:
            references.append(Photo(self.__get_feature(photo.image),photo.label))
        self.references = references
    
    def predict(self,images:List[Photo]):
        pred_labels = []
        for image in images:
            img_feature = self.__get_feature(image.image)
            #print('img_feature:', img_feature)
            ref = self.__search(img_feature)
            #print('reference: ', ref.image)
            pred_labels.append(ref.label)
        return pred_labels
    
    def score(self, true_labels: np.array, pred_labels: np.array) -> float:
        if len(true_labels) != len(pred_labels):
            raise Exception("Received arguments have different length")
        true = 0
        for idx, true_label in enumerate(true_labels):
            if true_label == pred_labels[idx]:
                true += 1
        return true / len(pred_labels)



        