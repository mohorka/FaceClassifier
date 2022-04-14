from typing import  List, Tuple
from collections import Counter
from core.models.photo import Photo
from core.data_preprocessing.data_load import load_data
import core.data_preprocessing.feature_extraction as fe
from core.data_preprocessing.train_test_split import train_test_split
from core.models.classifier import Classifier
from core.config.config import METHODS_PARAMS
from core.config.config import NUM_IMG_PER_GROUP
from core.figures.figures import corr_num_ref_plot, corr_amount_accuracy_plot, multi_features_amount_plot

def research(method:str) ->Tuple[List,List, List[Photo]]:
    print(f'Chosen method: {method}')
    images = load_data()

    range_params = METHODS_PARAMS[method]['range']

    classifier = Classifier(method)
    best_scores_with_params = []
    for p in range(*range_params):
        print('##############################')
        print(f'Param value: {p}')
        train, test, err = train_test_split(images)
        if err: return 
        classifier.fit(train, p)
        y_pred = classifier.predict(test)
        true_labels = [photo.label for photo in test]
        score = classifier.score(true_labels, y_pred)
        best_scores_with_params.append((score,p))

    # templates_for_tests = [next(image for image in images if image.label == label) for label in y_pred]
    templates_for_tests = [
        next(
            filter(
                lambda image: image.label == label,
                images
            ),
            None
        ) for label in y_pred
    ]
    corr_num_ref_plot(best_scores_with_params)

    x_test  = [photo.image for photo in test]
    return best_scores_with_params, x_test, templates_for_tests
    # templates_for_tests
    # for label in y_pred:
    #     templates_for_tests.append(next(image for image in images if image.label == label))

def parallel_research(params:dict):
    images = load_data()
    methods = list(params.keys())
    print(methods)
    classifiers = [Classifier(method) for method in methods]
    best_scores = []

    for amount_img in range (1, NUM_IMG_PER_GROUP):
        print('****************************')
        print(f'Current sample size: {amount_img}')
        train, test = [], []
        for label in range(1,42,1):
            particular_images = [image for image in images if image.label==label]
            percentage = amount_img / len(particular_images) * 100
            part_train, part_test, err = train_test_split(particular_images,percentage)
            if err: continue
            train += part_train
            test += part_test
        predicted = []
        for classifier in classifiers:
            classifier.fit(train,params[classifier.method[0]])
            pred_y = classifier.predict(test)
            predicted.append(pred_y)
        
        transp_preds = list(map(list, zip(*predicted)))
        num_true = 0
        y_test = [img.label for img in test]
        for idx, preds in enumerate(transp_preds):
            class_search = Counter()
            for pr in preds:
                class_search[pr] += 1
            class_voting = class_search.most_common(1)[0][0]
            if class_voting == y_test[idx]:
                num_true += 1
        score = num_true/len(y_test)
        best_scores.append((
            amount_img,
            score
        ))
        print(f'Voting score: {score}')
    multi_features_amount_plot(best_scores)
    return best_scores
            




