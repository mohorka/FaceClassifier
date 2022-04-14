from typing import Counter, List, Tuple
from core.models.classifier import Classifier
from core.models.photo import Photo
from core.data_preprocessing.data_load import load_data
from core.config.config import NUM_IMG_PER_GROUP
from core.data_preprocessing.train_test_split import train_test_split
from core.figures.figures import corr_amount_accuracy_plot

def recognition(
    method: str,
    param: int,
    percantage_of_train: str,
):
    print(f'Method: {method}')
    images = load_data()
    
    classifier = Classifier(method)
    train, test, err = train_test_split(images,percantage_of_train)
    if err:  return

    print('len of train: ', len(train))
    print('len of test: ', len(test))
    classifier.fit(train,param)
    y_pred = classifier.predict(test)
    print('y_pred: ', y_pred)
    y_true = [img.label for img in test]

    score = classifier.score(y_true, y_pred)

    templates_for_test = [
        next(image for image in images if image.label == label)
        for label in y_pred
    ]
    x_test  = [photo.image for photo in test]
    # for label in y_pred:
        # templates_for_test.append(next(image for image in images if image.label == label))
    
    print(f"{param=} ; {score=}")
    return score, x_test, templates_for_test

def parallel_recognition(params:dict, size_of_train: int):
    images = load_data()
    methods = list(params.keys())
    print("Methods ", methods)
    print("Params ", params)
    classifiers = [Classifier(method) for method in methods]

    #percantage = size_of_train / 10 * 100
    #print('percantage ', percantage)
    train, test = [], []
    for label in range(1,42,1):
        particular_images = [image for image in images if image.label==label]
        percantage = size_of_train / len(particular_images) * 100
        part_train, part_test, err = train_test_split(particular_images,percantage)
        if err: continue
        train += part_train
        test += part_test
   

    #train, test, err = train_test_split(images, proportion=percantage)
    #if err: return 

    for classifier in classifiers:
        classifier.fit(train, param = params[classifier.method[0]])
    #to do -- add per class number of imgs (check research)
    accuracy_at_num_img = []
    for idx, _ in enumerate(test):
        print(f'Current number of images is {idx}')
        curr_imgs = []
        curr_true_y = []
        pred_tests = []
        for i in range(idx + 1):
            curr_imgs.append(test[i])
            curr_true_y.append(test[i].label)
        for idx, classifier in enumerate(classifiers):
            pred_y = classifier.predict(curr_imgs)
            pred_tests.append(pred_y)
        
        T_preds = list(map(list, zip(*pred_tests)))
        true = 0

        y_test_labels = [image.label for image in test]
        for idx, preds in enumerate(T_preds):
            search = Counter()
            for pred in preds:
                search[pred] += 1
            voting = search.most_common(1)[0][0]
            if voting == y_test_labels[idx]:
                true += 1
        
        score = true / len(curr_true_y)
        accuracy_at_num_img.append((
            idx,
            score
        ))
        
    corr_amount_accuracy_plot(accuracy_at_num_img)

    return accuracy_at_num_img



