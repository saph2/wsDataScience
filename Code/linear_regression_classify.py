
# coding: utf-8

# Linear regression classifier
# Results saved to: "Data/Classify/LinearRegression"

import numpy as np
from sklearn import linear_model
import random
from sklearn.externals import joblib
import common_classify
import confusionMatrix
import handel_files

def build_classifier(train_X, train_Y):
    regr = linear_model.LinearRegression()
    regr.fit(train_X, train_Y)
    return regr


def cross_val_model(scaled_filtered_data, labels, regr_dir_path, numberOfClasses):

    print ("\nCross Validation...\n")

    # divide to train and test
    training_size_fraction = .09

    succ=0
    resultsOther=[0,0,0]

    for j in range(0,10):  # 10-fold cross validation

        # train and test indexes
        test_idx = np.array(random.sample(xrange(len(labels)), int((1 - training_size_fraction) * len(labels))))
        train_idx = np.array([x for x in xrange(len(labels)) if x not in test_idx])


        # build train and test samples
        test_X=scaled_filtered_data[test_idx]
        train_X=scaled_filtered_data[train_idx]

        # keep train and test labels
        test_Y=labels[test_idx]
        train_Y=labels[train_idx]

        # build classifier
        regr = build_classifier(train_X, train_Y)

        # dump classifier
        classPath=regr_dir_path+"/"+'linearRegression_model.pkl'
        joblib.dump(regr, classPath, compress=9)

        resultsOther[0]+=regr.coef_
        resultsOther[1]+=np.mean(regr.predict(test_X) - test_Y) ** 2
        resultsOther[2]+=regr.score(test_X,test_Y)

        prdarr=regr.predict(test_X)
        curSucc=0
        for i in range(0,len(prdarr)):
            prdarr[i]=round(prdarr[i])
            if prdarr[i]==test_Y[i]:
                curSucc+=1

        succ+=(float(curSucc)/len(prdarr))*100

    succ=succ/10
    resultsOther[0]=resultsOther[0]/10
    resultsOther[1]=resultsOther[1]/10
    resultsOther[2]=resultsOther[2]/10



    # The coefficients
    resultsStr=("Coefficients:              {0}\n").format(resultsOther[0])+\
                ("Residual sum of squares:   %.2f" % (resultsOther[1])+"\n"+\
                ('Variance score:            %.2f' % resultsOther[2])+"\n")

    resultsStr+=("Success:                    {0}%\n".format(succ))

    print resultsStr

    # save to file
    with open(regr_dir_path+"/linearRegression_results.txt", 'w') as f2:
        f2.write("Linear Regression:\n")
        f2.write("Number of classes={0}\n\n".format(numberOfClasses))
        f2.write(" -- cross val prediction --\n")
        f2.write(resultsStr)
        f2.write("\n")

    handel_files.save_to_model_dir("../Model",classPath)
    print ("Classifier saved to 'Model'\n")

# build the LR classifier
def build_train_model(vec_dir_path, regr_dir_path, numberOfClasses):
    # read the vectors from all data files
    data_vectors = common_classify.read_vectors(vec_dir_path)

    # return vectors in range [0,1] and labels
    (vectors, labels) = common_classify.scale_and_filter_vectors_without_negative(data_vectors)

    # cross val the train set
    cross_val_model(vectors, labels, regr_dir_path, numberOfClasses)


# classify test vectors
def predict_test_set(test_dir_path, regr_dir_path,numberOfClasses):
    test_X = common_classify.read_vectors(test_dir_path)
    (test_X, test_Y) = common_classify.scale_and_filter_vectors_without_negative(test_X)

    print ("\nClassify Test Data...\n")

    # load classifier
    regr = joblib.load(regr_dir_path+"/"+'linearRegression_model.pkl')

    # The coefficients
    resultsStr=("Coefficients:                 {0}\n").format(regr.coef_)+\
               ("Residual sum of squares:       %.2f" % (np.mean(regr.predict(test_X) - test_Y) ** 2))+"\n"+\
               ("Variance score:                %.2f" % regr.score(test_X,test_Y))+"\n"


    prdarr=regr.predict(test_X)
    succ=0
    for i in range(0,len(prdarr)):
        prdarr[i]=round(prdarr[i])
        if prdarr[i]==test_Y[i]:
            succ+=1

    succ=(float(succ)/len(prdarr))*100
    resultsStr+=("Success:                     {0}%\n".format(succ))

    print resultsStr

    # save to file
    with open(regr_dir_path+"/linearRegression_results.txt", 'a') as f2:
        f2.write("\n")
        f2.write(" -- test prediction -- \n")
        f2.write(resultsStr)
        f2.write("\n")