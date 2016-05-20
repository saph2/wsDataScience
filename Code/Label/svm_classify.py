# coding: utf-8


import numpy as np
from sklearn import preprocessing
from sklearn import svm
import random
import os
from sklearn.externals import joblib

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


def build_classifier(train_samples, train_out,svmModel):
    clf = svm.SVC(kernel=svmModel['kernel'],C=svmModel['C'],degree=svmModel['d'])
    clf.fit(train_samples, train_out)
    return clf


def cross_val_model(scaled_filtered_data, labels, svmModel_dir_path, svmModel, numberOfClasses):
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
    clf = build_classifier(train_samples, train_out,svmModel)

    # dump classifier
    joblib.dump(clf, svmModel_dir_path+"/"+'svm_model.pkl', compress=9)

    # predict
    a = np.array(clf.predict(test_samples).astype(int))
    c = np.array(a) == np.array(test_out)

    print ("\nCross Validation...\n")

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n" + \
                 "Number of support vectors for positive class: " + str(clf.n_support_[0]) + "\n" + \
                 "Number of support vectors for negative class: " + str(clf.n_support_[1])

    print resultsStr

    # save to file
    with open(svmModel_dir_path+"/svm_results.txt", 'w') as f2:
        f2.write("SVM model: kernel={0}, C={1}, d={2}\n".format(svmModel['kernel'],svmModel['C'],svmModel['d']))
        f2.write("Number of classes={0}\n\n".format(numberOfClasses))
        f2.write(" -- cross val prediction --\n")
        f2.write(resultsStr)
        f2.write("\n")


# build the SVM classifier
def build_train_model(vec_dir_path,svmModel_dir_path,svmModel,numberOfClasses):
    # read the vectors from all data files
    data_vectors = read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = scale_and_filter_vectors(data_vectors)

    # cross val the train set
    cross_val_model(vectors, labels,svmModel_dir_path,svmModel,numberOfClasses)


# classify validation vectors
def predict_validation_set(validation_dir_path, svmModel_dir_path):
    validation_vectors = read_vectors(validation_dir_path)
    (validation_vectors, validation_labels) = scale_and_filter_vectors(validation_vectors)

    # load classifier
    clf = joblib.load(svmModel_dir_path+"/"+'svm_model.pkl')

    a = np.array(clf.predict(validation_vectors).astype(int))
    c = np.array(a) == np.array(validation_labels)

    print ("\nClassify Validation Data...\n")

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n" + \
                 "Number of support vectors for positive class: " + str(clf.n_support_[0]) + "\n" + \
                 "Number of support vectors for negative class: " + str(clf.n_support_[1])

    print resultsStr

    # save to file
    with open(svmModel_dir_path+"/svm_results.txt", 'a') as f2:
        f2.write("\n")
        f2.write(" -- validation prediction -- \n")
        f2.write(resultsStr)
        f2.write("\n")



