
# coding: utf-8


import build_duration_bar
import clean_data
import execute_svm_prediction
import handel_files
import label_data
import scale_features
import vectorize_data

featuresOfInterest = ["continent", "country", "opName", "osVer", "brwVer"]

try:
    # full feature list from file :
    # featuresNames = {'TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', ''}

    # move all request files from daily folders to one folder.
    # file name is according to the date
    handel_files.move_data_to_one_folder("DataSplitToDailyFolder", "RawData")
    print "finished move_data_to_one_folder"


    # split raw data to train and validation
    handel_files.split_files_to_test_and_train_dir("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
    print "finished split_files_to_test_and_train_dir"


    # # build the dictionary which contains for each "host name"+"url" the min duration
    build_duration_bar.buildBar("Train/TrainRawData", "MinDurationBar")
    print "finished buildBar"


    # # clean the data from 'comma'
    clean_data.cleanFilesInDir("Train/TrainRawData")
    clean_data.cleanFilesInDir("Validation/ValidationRawData")
    print "finished cleanFilesInDir"


    # # label the data
    label_data.labelAllfiles("Train/TrainRawData", "Train/TrainLabeledData", "MinDurationBar")
    label_data.labelAllfiles("Validation/ValidationRawData", "Validation/ValidationLabeledData", "MinDurationBar")
    # print "t0 = " + str(label_data.t0) + " t1 = " + str(label_data.t1)
    print "finished labelAllfiles"


    # # scaleFeatures: create the files of features ordered by workloads and numbered in folder Features"
    scale_features.buildFeaturesFiles("Train/TrainLabeledData", "Features", featuresOfInterest)
    print "finished buildFeaturesFiles"


    # # vectorizes the data
    vectorize_data.dataToVectors("Features", "Train/TrainLabeledData", "Train/TrainVectors", True, featuresOfInterest)
    vectorize_data.dataToVectors("Features", "Validation/ValidationLabeledData", "Validation/ValidationVectors", True, featuresOfInterest)
    print "finished dataToVectors"


    # #  build svm model and run cross val on our labeled vectors
    # print "starting build_train_model"
    # execute_svm_prediction.build_train_model("Train/TrainVectors")
    # print "finished build_train_model"


    #  build classifier and execute prediction
    print "starting predict_validation_set"
    execute_svm_prediction.predict_validation_set("Validation/ValidationVectors", "Train/TrainVectors")
    print "finished predict_validation_set"

finally:
    # # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
    print "finished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders()
    print "finished removing all files from all directories"
#
