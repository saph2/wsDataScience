# coding: utf-8


import numpy as np
from sklearn import svm
import random
from sklearn.externals import joblib
import common_classify
import confusionMatrix


def build_classifier(train_samples, train_out,svmModel):
    clf = svm.SVC(kernel=svmModel['kernel'],C=svmModel['C'],degree=svmModel['d'],gamma=svmModel['gamma'])
    clf.fit(train_samples, train_out)
    return clf


def cross_val_model(scaled_filtered_data, labels, svmModel_dir_path, svmModel, numberOfClasses):

    print ("\nCross Validation...\n")

    # divide to train and test
    training_size_fraction = .09

    succ=0
    supvec=[0,0]

    for j in range (0,10):

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

        succ+=sum(c) * 100.0 / len(a)
        supvec[0]+=clf.n_support_[0]
        supvec[1]+=clf.n_support_[1]

    succ=succ/10
    supvec[0]=supvec[0]/10
    supvec[1]=supvec[1]/10

    resultsStr = "Accuracy                                    : " + str(succ) + " %" + "\n" + \
                "Number of support vectors for positive class: " + str(supvec[0]) + "\n" + \
                "Number of support vectors for negative class: " + str(supvec[1])

    print resultsStr

    # save to file
    with open(svmModel_dir_path+"/svm_results.txt", 'w') as f2:
        f2.write("SVM model: kernel={0}, C={1}, d={2}\n".format(svmModel['kernel'],svmModel['C'],svmModel['d']))
        f2.write("Number of classes={0}\n\n".format(numberOfClasses))
        f2.write(" -- cross val prediction --\n")
        f2.write(resultsStr)
        f2.write("\n")

    return succ


# build the SVM classifier
def build_train_model(vec_dir_path,svmModel_dir_path,svmModel,numberOfClasses):
    # read the vectors from all data files
    data_vectors = common_classify.read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = common_classify.scale_and_filter_vectors_with_negative(data_vectors)

    # cross val the train set
    succ=cross_val_model(vectors, labels,svmModel_dir_path,svmModel,numberOfClasses)

    return succ


# classify test vectors
def predict_test_set(test_dir_path, svmModel_dir_path, numberOfClasses):
    test_vectors = common_classify.read_vectors(test_dir_path)
    (test_vectors, test_labels) = common_classify.scale_and_filter_vectors_with_negative(test_vectors)

    # load classifier
    clf = joblib.load(svmModel_dir_path+"/"+'svm_model.pkl')

    a = np.array(clf.predict(test_vectors).astype(int))
    c = np.array(a) == np.array(test_labels)

    print ("\nClassify Test Data...\n")

    resultsStr = "Accuracy                                    : " + str(sum(c) * 100.0 / len(a)) + " %" + "\n" + \
                 "Number of support vectors for positive class: " + str(clf.n_support_[0]) + "\n" + \
                 "Number of support vectors for negative class: " + str(clf.n_support_[1])

    print resultsStr

    # save to file
    with open(svmModel_dir_path+"/svm_results.txt", 'a') as f2:
        f2.write("\n")
        f2.write(" -- test prediction -- \n")
        f2.write(resultsStr)
        f2.write("\n")

    succ= sum(c) * 100.0 / len(a)

    confusionMatrix.create_matrix("SVM",test_vectors, test_labels, a,numberOfClasses)

    return succ



