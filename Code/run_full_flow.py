# coding: utf-8

# The main script for creating the train classifier
# Creates the needed directories in "Data"
# Then reads, labels and vectorizes the requests files from "DailyData"
# Finally, train a classifier by the train vectors and classify the test vectors
# Saves the classifier and the features file in the "Model" directory for our final app

import handel_files
import vectorize_full
import classify_full
import features_charts


header="../Data/"

delete_files_at_the_end=True  # if this flag is 'True': all files created will be deleted at the end of the run, 'Flase': will save them

featuresOfInterest = ['TimeOfDay','BrowserVer','OsVer','OpName','Continent','Country']
numberOfClasses=3

# create directories
handel_files.create_directories(header)

try:

    # create vectors from row data

     vectorize_full.run_code(header, featuresOfInterest, numberOfClasses)

    # classify test by train vectors

     classify_full.run_code(header, numberOfClasses)

    # create the features charts

     features_charts.featuresToCharts(header+"Features",header+"Results/Features")


finally:
     # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Test/TestRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    if delete_files_at_the_end:
        handel_files.remove_all_files_from_all_folders(header)
        print "\nfinished removing all files from all directories"



