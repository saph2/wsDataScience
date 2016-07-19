# coding: utf-8

# This is the main vectorizing script
# This script gets, as an input, the requests files as given in the course site ("DailyData" directory)
# The output are the vectors representing the input requests files.
# Output is saved to: "Data/Train/TrainVectors" or "Data/Test/TestVectors"

import build_duration_bar
import clean_data
import handel_files
import label_data
import scale_features
import vectorize_data


def run_code(header,featuresOfInterest,numberOfClasses):

    # move all request files from "DailyData" folders to one folder "Data/RawData".
    handel_files.move_data_to_one_folder(header + "../DailyData", header + "RawData")
    print "finished move_data_to_one_folder"

    # clean the data and add "TimeOfDay" feature
    clean_data.cleanFilesInDir(header+"RawData")
    print "finished cleanFilesInDir"

    # split raw data to train and test: "Data/Train", "Data/Test"
    handel_files.split_files_to_test_and_train_dir(header + "RawData", header + "Train/TrainRawData", header + "Test/TestRawData")
    print "finished split_files_to_test_and_train_dir"

    # build the dictionary which contains for each "host"+"url"+"continent" the average duration
    build_duration_bar.buildBar(header+"Train/TrainRawData", header+"DurationBar")
    print "finished buildBar"

    # label the data
    label_data.labelAllfiles(header+"Train/TrainRawData", header+"Train/TrainLabeledData", header+"DurationBar",numberOfClasses)
    label_data.labelAllfiles(header+"Test/TestRawData", header+"Test/TestLabeledData", header+"DurationBar",numberOfClasses)
    print "finished labelAllfiles"


    # scaleFeatures: create the feature scaling files in directory: "Data/Features"
    scale_features.buildFeaturesFiles(header+"Train/TrainLabeledData", header+"Features", featuresOfInterest,numberOfClasses)
    print "finished buildFeaturesFiles"


    # vectorizes the data
    vectorize_data.dataToVectors(header+"Features", header+"Train/TrainLabeledData", header+"Train/TrainVectors", True)
    vectorize_data.dataToVectors(header+"Features", header+"Test/TestLabeledData", header+"Test/TestVectors", True)
    print "finished dataToVectors"