# coding: utf-8


import numpy as np
from sklearn import preprocessing
from sklearn import svm
import random
import os



# read vectors
def read_vectors(vec_dir_path):
    filtered_data = list()
    for filename in os.listdir(vec_dir_path):
        if "vectors" in filename:
            filepath = vec_dir_path + "/" + filename
            # convert the file to array of objects
            data = np.array(np.genfromtxt(filepath, delimiter=',', autostrip=True))
            filtered_data.append(data)
    filtered_data = np.asarray(filtered_data)[0]
    return filtered_data



def scale_and_filter_vectors(filtered_data):
    # cut headline
    sz = filtered_data.size
    filtered_data = filtered_data[1:sz]

    # save labels
    labels = filtered_data[:, 5]
    for i in range(0, len(labels)):
        labels[i] = int(labels[i])

    # cut labels
    scaled_filtered_data = preprocessing.scale(filtered_data)
    scaled_filtered_data = scaled_filtered_data[:, :-1]

    return scaled_filtered_data, labels



def build_classifier(train_samples, train_out):
    clf = svm.SVC(kernel='linear')
    clf.fit(train_samples, train_out)
    return clf



def cross_val_model(scaled_filtered_data, labels):
    # divide to train and test
    training_size_fraction = .09

    # train and test indexes
    test_idx = np.array(random.sample(xrange(len(labels)), int((1 - training_size_fraction) * len(labels))))
    train_idx = np.array([x for x in xrange(len(labels)) if x not in test_idx])

    # build train and test samples
    test_samples = scaled_filtered_data[test_idx]
    train_samples = scaled_filtered_data[train_idx]

    # keep train and test labels
    test_out = labels[test_idx]
    train_out = labels[train_idx]

    # build classifier
    clf = build_classifier(train_samples, train_out)

    # predict
    a = np.array(clf.predict(test_samples).astype(int))
    c = np.array(a) == np.array(test_out)

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n" + \
                 "Number of support vectors for positive class: " + str(clf.n_support_[0]) + "\n" + \
                 "Number of support vectors for negative class: " + str(clf.n_support_[1])

    # print results
    # print "Accuracy                                    : ", str(sum(c) * 100.0 / len(a)) + " %"
    # print "Number of support vectors for positive class: ", clf.n_support_[0]
    # print "Number of support vectors for negative class: ", clf.n_support_[1]

    print resultsStr

    # save to file
    with open(pathToResultsFile, 'w') as f2:
        f2.write(" -- train model --\n")
        f2.write(resultsStr)


# this is where we save all the results
pathToResultsFile = "results.txt"


# vecDirPath="Data/TrainVectors"
def build_train_model(vec_dir_path):
    # read the vectors from all data files
    data_vectors = read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = scale_and_filter_vectors(data_vectors)

    # cross val the train set
    cross_val_model(vectors, labels)


def predict_validation_set(validation_dir_path, train_dir_path):
    train_vectors = read_vectors(train_dir_path)
    (train_vectors, train_labels) = scale_and_filter_vectors(train_vectors)
    validation_vectors = read_vectors(validation_dir_path)
    (validation_vectors, validation_labels) = scale_and_filter_vectors(validation_vectors)

    clf = build_classifier(train_vectors, train_labels)

    a = np.array(clf.predict(validation_vectors).astype(int))
    c = np.array(a) == np.array(validation_labels)

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n" + \
                 "Number of support vectors for positive class: " + str(clf.n_support_[0]) + "\n" + \
                 "Number of support vectors for negative class: " + str(clf.n_support_[1])

    # print results
    # print "Accuracy                                    : ", str(sum(c) * 100.0 / len(a)) + " %"
    # print "Number of support vectors for positive class: ", clf.n_support_[0]
    # print "Number of support vectors for negative class: ", clf.n_support_[1]
    print resultsStr

    # save to file
    with open(pathToResultsFile, 'a') as f2:
        f2.write("\n\n\n")
        f2.write(" -- prediction SVM -- \n")
        f2.write(resultsStr)





