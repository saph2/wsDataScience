# coding: utf-8


import handel_files
import vectorize_full
import classify_full


header="../Data/"

featuresOfInterest = ['BrowserVer','OsVer','Continent','OpName','Host']
numberOfClasses=2

try:
 # create vectors from row data

     vectorize_full.run_code(header, featuresOfInterest, numberOfClasses)

 # classifty test by train vectors

     classify_full.run_code(header, numberOfClasses)


finally:
     # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Validation/ValidationRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders(header)
    print "\nfinished removing all files from all directories"

