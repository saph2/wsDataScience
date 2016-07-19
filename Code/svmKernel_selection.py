# coding: utf-8

# This script tests different kernels for the SVM classifier
# Results saved to: "Data/Selection/ClassifierSelection"

import handel_files
import svm_classify
import vectorize_full

header="../Data/"

# full feature list from file :
selectedFeatures=['TimeOfDay','BrowserVer','OsVer','Continent','OpName']
numberOfClassesOpt=[2,3,4]
selectedModels=[{'kernel': 'linear', 'C': 1, 'd': 1, 'gamma': 2},{'kernel': 'linear', 'C': 10, 'd': 1, 'gamma': 2}
                ,{'kernel': 'poly', 'C': 1, 'd': 2, 'gamma': 'auto'},{'kernel':'poly','C':1,'d':3,'gamma':'auto'},
                 {'kernel':'poly','C':1,'d':2,'gamma':2},{'kernel':'poly','C':1,'d':3,'gamma':2},{'kernel':'poly','C':10,'d':2,'gamma':2},
                 {'kernel':'rbf','C':1,'d':1,'gamma':'auto'},{'kernel':'rbf','C':10,'d':1,'gamma':'auto'}]

handel_files.create_directories(header) # create directories

try:
    with open (header+"Selection/ClassifierSelection/kernelSelectionSummary.csv",'w') as f:
        f.write("Model,Success\n")
        for numberOfClasses in numberOfClassesOpt:  # for each number of classes
            print(numberOfClasses)
            vectorize_full.run_code(header, selectedFeatures, numberOfClasses)
            for svmModel in selectedModels:  # for each SVM kernel option
                try:
                    strLine=str(svmModel)+" Num Classes={0}".format(numberOfClasses)
                    print ("\n"+strLine+"\n")
                    svm_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
                    result=svm_classify.predict_test_set(header + "Test/TestVectors", header + "Classify/SVM", numberOfClasses)
                    f.write("{0},{1}\n".format(strLine,result))
                except:
                    print ("Failed: "+str(svmModel)+"\n")
                    continue
            handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Test/TestRawData")
            print "\nfinished remove_files_to_rawdata"
            handel_files.remove_all_files_from_all_folders(header)
            print "\nfinished removing all files from all directories\n"
        f.close()

except:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Test/TestRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders(header)
    print "\nfinished removing all files from all directories"


