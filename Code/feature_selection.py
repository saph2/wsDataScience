# coding: utf-8

# Feature selection script
# Checks for feature subtraction and feature addition
# Output to: "Data/Selection/FeatureSelection"

import handel_files
import svm_classify
import os
import csv
from collections import OrderedDict
import vectorize_full

header="../Data/"

# full feature list from file :
selectedFeatures=['TimeOfDay','BrowserVer','OsVer','OpName','Continent']
allFeatures = ['TimeOfDay','OpName','TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City' , 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'UrlBase', 'Host']
numberOfClasses=3
svmModel={'kernel':'poly','C':1,'d':2,'gamma':'auto'}
successDict=OrderedDict()



def rewriteVectors(oldDir,newDir,newFeatures):
    for filename in os.listdir(oldDir):
        if "vectors" in filename:
            with open (oldDir+"/"+filename) as f:
                data = list(csv.reader(f))
            f.close()
            with open (newDir+"/"+filename,'w') as f:
                for vec in data:
                    for i in range(0,len(vec)):
                        if data[0][i] in newFeatures:
                            item=vec[i]
                            f.write("{0}".format(item))
                            if (i<len(vec)-1):
                                f.write(',')
                    f.write('\n')
                f.close()

def testAddFeatures(): # Adding features and testing success rate
    for feature in allFeatures:
        try:
            newFeatures=list([item for item in selectedFeatures])
            if feature not in selectedFeatures:
                newFeatures.append(feature)
                newFeatures.append('Label')
                strF=str(newFeatures).replace(",",";")
                print(strF+"\n")
                rewriteVectors(header+"Train/TrainVectors",header+"Selection/FeatureSelection/TrainNewVectors",newFeatures)
                rewriteVectors(header+"Test/TestVectors",header+"Selection/FeatureSelection/TestNewVectors",newFeatures)
                resultc=svm_classify.build_train_model(header+"Selection/FeatureSelection/TrainNewVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
                resultv=svm_classify.predict_test_set(header + "Selection/FeatureSelection/TestNewVectors", header + "Classify/SVM", numberOfClasses)
                print("Cross validation:{0}, Test:{1}\n".format(resultc,resultv))
                successDict[strF]=[resultc,resultv]
        except:
            print ("failed {0}\n".format(feature))
            continue

def testRemoveFeatures(): # Removing features and testing success rate
    for feature in selectedFeatures:
        try:
            newFeatures=list([item for item in selectedFeatures])
            newFeatures.remove(feature)
            newFeatures.append('Label')
            strF=str(newFeatures).replace(",",";")
            print(strF+"\n")
            rewriteVectors(header+"Train/TrainVectors",header+"Selection/FeatureSelection/TrainNewVectors",newFeatures)
            rewriteVectors(header+"Test/TestVectors",header+"Selection/FeatureSelection/TestNewVectors",newFeatures)
            resultc=svm_classify.build_train_model(header+"Selection/FeatureSelection/TrainNewVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
            resultv=svm_classify.predict_test_set(header + "Selection/FeatureSelection/TestNewVectors", header + "Classify/SVM", numberOfClasses)
            print("Cross validation:{0}, Test:{1}\n".format(resultc,resultv))
            successDict[strF]=[resultc,resultv]
        except:
            print ("failed {0}\n".format(feature))
            continue


def saveDictTofile(fileName):
    with open (fileName,'w') as f:
        f.write("Added,Cross validation,Test\n")
        for key in successDict:
            f.write("{0},{1},{2}\n".format(key,(successDict[key])[0],(successDict[key])[1]))
        f.close()

# run the original set first and create the vectors
def init():
    successDict.clear()
    newFeatures=list([item for item in selectedFeatures])
    newFeatures.append('Label')
    strF=str(newFeatures).replace(",",";")
    print(strF+"\n")
    rewriteVectors(header+"Train/TrainVectors",header+"Selection/FeatureSelection/TrainNewVectors",newFeatures)
    rewriteVectors(header+"Test/TestVectors",header+"Selection/FeatureSelection/TestNewVectors",newFeatures)
    resultc=svm_classify.build_train_model(header+"Selection/FeatureSelection/TrainNewVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
    resultv=svm_classify.predict_test_set(header + "Selection/FeatureSelection/TestNewVectors", header + "Classify/SVM", numberOfClasses)
    print("Cross validation:{0}, Test:{1}\n".format(resultc,resultv))
    successDict[strF]=[resultc,resultv]

# test feature subtraction
def removeFeatures():
    init()
    testRemoveFeatures()
    saveDictTofile(header+"Selection/FeatureSelection/featureRemovingSummary.csv")


# test feature addition
def addFeatures():
    init()
    testAddFeatures()
    saveDictTofile(header+"Selection/FeatureSelection/featureAdditionSummary.csv")

try:
    handel_files.create_directories(header) # create directories
    vectorize_full.run_code(header, allFeatures, numberOfClasses)
    removeFeatures()
    addFeatures()

finally:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Test/TestRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders(header)
    print "\nfinished removing all files from all directories"

