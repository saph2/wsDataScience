
# coding: utf-8


import handel_files
import clean_data
import build_duration_bar
import label_data
import scale_features
import vectorize_data
import svm_classify
import linear_regression_classify

# full feature list from file :
# featuresNames = {'TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', ''}

# Model Variables #############################################################
featuresOfInterest = ['BrowserVer', 'OsVer', 'Continent', 'Country', 'OpName']
numberOfClasses=3

# classify ####################################################################
useSVM=True
svmModel={'kernel':'linear','C':1,'d':1}

useLinearRegression=True
###############################################################################

try:
    #move all request files from daily folders to one folder.
    # file name is according to the date
    handel_files.move_data_to_one_folder("Data/DataSplitToDailyFolder", "Data/RawData")
    print "finished move_data_to_one_folder"

    # clean the data from 'comma'
    clean_data.cleanFilesInDir("Data/RawData")
    print "finished cleanFilesInDir"

    # split raw data to train and validation
    handel_files.split_files_to_test_and_train_dir("Data/RawData", "Data/Train/TrainRawData", "Data/Validation/ValidationRawData")
    print "finished split_files_to_test_and_train_dir"

    # build the dictionary which contains for each "host name"+"url" the min duration
    build_duration_bar.buildBar("Data/Train/TrainRawData", "Data/DurationBar")
    print "finished buildBar"

    # label the data
    label_data.labelAllfiles("Data/Train/TrainRawData", "Data/Train/TrainLabeledData", "Data/DurationBar",numberOfClasses)
    label_data.labelAllfiles("Data/Validation/ValidationRawData", "Data/Validation/ValidationLabeledData", "Data/DurationBar",numberOfClasses)
    # print "t0 = " + str(label_data.t0) + " t1 = " + str(label_data.t1)
    print "finished labelAllfiles"


    # scaleFeatures: create the files of features ordered by workloads and numbered in folder Data/Features"
    scale_features.buildFeaturesFiles("Data/Train/TrainLabeledData", "Data/Features", featuresOfInterest,numberOfClasses)
    print "finished buildFeaturesFiles"


    # vectorizes the data
    vectorize_data.dataToVectors("Data/Features", "Data/Train/TrainLabeledData", "Data/Train/TrainVectors", True)
    vectorize_data.dataToVectors("Data/Features", "Data/Validation/ValidationLabeledData", "Data/Validation/ValidationVectors", True)
    print "finished dataToVectors"

    # SVM ###########################################################
    if useSVM:

        print ("classifying with SVM:\n")

        # build svm model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        svm_classify.build_train_model("Data/Train/TrainVectors","Data/Classify/SVM" ,svmModel,numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_validation_set"
        svm_classify.predict_validation_set("Data/Validation/ValidationVectors", "Data/Classify/SVM")
        print "\nfinished predict_validation_set"

    # Linear Regression #####################################################################

    if useLinearRegression:

        print ("classifying with Linear Regression:\n")

        # build linear regression model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        linear_regression_classify.build_train_model("Data/Train/TrainVectors", "Data/Classify/LinearRegression",numberOfClasses)
        print "\nfinished build_train_model"

        #  load classifier and execute prediction
        print "\nstarting predict_validation_set"
        linear_regression_classify.predict_validation_set("Data/Validation/ValidationVectors", "Data/Classify/LinearRegression")
        print "\nfinished predict_validation_set"

    ###################################################################

finally:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata("Data/RawData", "Data/Train/TrainRawData", "Data/Validation/ValidationRawData")
    print "\nfinished remove_files_to_rawdata"

    # finally:
    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders()
    print "\nfinished removing all files from all directories"

