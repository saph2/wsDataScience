import svm_classify
import linear_regression_classify
import naive_bayes_classify


def run_code(header,numberOfClasses):

    # classify ####################################################################
    useSVM=True
    svmModel={'kernel':'poly','C':1,'d':2,'gamma':2}

    useLinearRegression=True

    useBAYES=True


    # SVM ##########################################################################
    if useSVM:

        print ("classifying with SVM:\n")

        # build svm model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        svm_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_validation_set"
        svm_classify.predict_validation_set(header+"Validation/ValidationVectors", header+"Classify/SVM")
        print "\nfinished predict_validation_set"

    # Linear Regression #####################################################################
    if useLinearRegression:

        print ("classifying with Linear Regression:\n")

        # build linear regression model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        linear_regression_classify.build_train_model(header+"Train/TrainVectors", header+"Classify/LinearRegression",numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_validation_set"
        linear_regression_classify.predict_validation_set(header+"Validation/ValidationVectors", header+"Classify/LinearRegression")
        print "\nfinished predict_validation_set"

    # NAIVE BAYES ####################################################################
    if useBAYES:
            print ("classifying with Naive Bayes:\n")

            # build naive bayes model and run cross val on our labeled vectors, export classifier
            print "\nstarting build_train_model"
            naive_bayes_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/NaiveBayes" ,numberOfClasses)
            print "\nfinished build_train_model"


            # load classifier and execute prediction
            print "\nstarting predict_validation_set"
            naive_bayes_classify.predict_validation_set(header+"Validation/ValidationVectors", header+"Classify/NaiveBayes")
            print "\nfinished predict_validation_set"

    ###################################################################################