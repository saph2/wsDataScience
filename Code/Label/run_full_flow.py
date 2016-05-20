# coding: utf-8


import build_duration_bar
import clean_data
import svm_classify
import handel_files
import label_data
import scale_features
import vectorize_data

# full feature list from file :
# featuresNames = {'TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', ''}

# Model Variables #############################################################
featuresOfInterest = ['BrowserVer', 'OsVer', 'Continent', 'Country', 'OpName']
numberOfClasses = 2
# classify
useSVM = True
svmModel = {'kernel':'linear','C':1,'d':1}
###############################################################################

try:
    #move all request files from daily folders to one folder.
    # file name is according to the date
    handel_files.move_data_to_one_folder("DataSplitToDailyFolder", "RawData")
    print "finished move_data_to_one_folder"
    print "finished move_data_to_one_folder"

    # clean the data from 'comma'
    clean_data.cleanFilesInDir("RawData")
    print "finished cleanFilesInDir"

    # split raw data to train and validation
    handel_files.split_files_to_test_and_train_dir("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
    print "finished split_files_to_test_and_train_dir"

    # build the dictionary which contains for each "host name"+"url" the min duration
    build_duration_bar.buildBar("Train/TrainRawData", "DurationBar")
    print "finished buildBar"

    # label the data
    label_data.labelAllfiles("Train/TrainRawData", "Train/TrainLabeledData", "DurationBar",numberOfClasses)
    label_data.labelAllfiles("Validation/ValidationRawData", "Validation/ValidationLabeledData", "DurationBar",numberOfClasses)
    # print "t0 = " + str(label_data.t0) + " t1 = " + str(label_data.t1)
    print "finished labelAllfiles"


    # scaleFeatures: create the files of features ordered by workloads and numbered in folder Features"
    scale_features.buildFeaturesFiles("Train/TrainLabeledData", "Features", featuresOfInterest,numberOfClasses)
    print "finished buildFeaturesFiles"


    # vectorizes the data
    vectorize_data.dataToVectors("Features", "Train/TrainLabeledData", "Train/TrainVectors", True)
    vectorize_data.dataToVectors("Features", "Validation/ValidationLabeledData", "Validation/ValidationVectors", True)
    print "finished dataToVectors"

    # SVM ###########################################################
    if useSVM:

        # build svm model and run cross val on our labeled vectors, export classifier
        print "\nstarting build_train_model"
        svm_classify.build_train_model("Train/TrainVectors","Classify/SVM" ,svmModel,numberOfClasses)
        print "\nfinished build_train_model"


        #  load classifier and execute prediction
        print "\nstarting predict_validation_set"
        svm_classify.predict_validation_set("Validation/ValidationVectors", "Classify/SVM")
        print "\nfinished predict_validation_set"

    ######################################################################

finally:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
    print "\nfinished remove_files_to_rawdata"

    # finally:
    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders()
    print "\nfinished removing all files from all directories"

