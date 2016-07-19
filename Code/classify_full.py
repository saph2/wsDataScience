
# The full classifying process from vectors to a trained classifier
# Choose classifier: SVM, LR, NB
# Results saved to: "Data/Classify/SVM" OR "Data/Classify/LinearRegression" OR "Data/Classify/NaiveBase"

import svm_classify
import linear_regression_classify
import naive_bayes_classify


def run_code(header,numberOfClasses):

    # classify ####################################################################
    useSVM=True
    svmModel={'kernel':'poly','C':1,'d':2,'gamma':'auto'}

    useLinearRegression=False

    useBAYES=False


    # SVM ##########################################################################
    if useSVM:

        print ("classifying with SVM:\n")

        # build svm model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        svm_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_test_set"
        svm_classify.predict_test_set(header + "Test/TestVectors", header + "Classify/SVM", numberOfClasses)
        print "\nfinished predict_test_set"

    # Linear Regression #####################################################################
    if useLinearRegression:

        print ("classifying with Linear Regression:\n")

        # build linear regression model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        linear_regression_classify.build_train_model(header+"Train/TrainVectors", header+"Classify/LinearRegression",numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_test_set"
        linear_regression_classify.predict_test_set(header + "Test/TestVectors", header + "Classify/LinearRegression",numberOfClasses)
        print "\nfinished predict_test_set"

    # NAIVE BAYES ####################################################################
    if useBAYES:
            print ("classifying with Naive Bayes:\n")

            # build naive bayes model and run cross val on our labeled vectors, export classifier
            print "\nstarting build_train_model"
            naive_bayes_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/NaiveBayes" ,numberOfClasses)
            print "\nfinished build_train_model"


            # load classifier and execute prediction
            print "\nstarting predict_test_set"
            naive_bayes_classify.predict_test_set(header + "Test/TestVectors", header + "Classify/NaiveBayes",numberOfClasses)
            print "\nfinished predict_test_set"

    ###################################################################################