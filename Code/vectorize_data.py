# coding: utf-8


# This script vectorizes the rows of the requests files in the given folder
# Input: the requests files
# Uses: the files from the "Data/Features" folder
# Output: writes vectors files to the Folders "Data/Train/TrainVectors" or "Data/Test/TestVectors"


import os
import csv
from collections import OrderedDict

allFeaturesDict=OrderedDict()

#update dict from the scaled Features file
def updateDict (data,featureDict):
    data.reverse
    headline=data.pop(0)
    fieldIDPlace=-1
    fieldNamePlace=-1
    i=0
    for title in headline:
        if title=='fieldID':
            fieldIDPlace=i
        if title =='fieldName':
            fieldNamePlace=i
        i+=1
    if fieldIDPlace<0 or fieldNamePlace<0:
        print ("indexs not found in request file in vectorize_data.py: updateDict")
        exit(0)
    for row in data:
        featureDict[row[fieldNamePlace]] = row[fieldIDPlace]  # example: update row "England" in CountryDict

# create a new vector from the given row
def addToNewRow (row,newRow,featureDict,featurePlace):
    currentField=row[featurePlace]  # example: countryDict-> England
    if currentField in featureDict:
        index=featureDict[currentField]  # example: index = 3 (country[England]=3)
    else:
        index=0
    newRow.append(index)

# add all features to new line
def addAllToNewRow(row, newRow, featuresPlaces):
    for feature in featuresPlaces.keys():  # add each feature id to the new vector
        addToNewRow(row, newRow, allFeaturesDict[feature], featuresPlaces[feature])

def vectorizeFile(data, newdata, isLabeled):
    headline=data.pop(0)
    # initialize featuresPlaces
    featuresPlaces = OrderedDict()
    for feature in allFeaturesDict.keys():
        featuresPlaces[feature] = -1
    labelPlace=-1
    i=0
    for title in headline:
        if title in allFeaturesDict.keys():
            featuresPlaces[title] = i
        if title == "Label":
            labelPlace=i
        i+=1

    # make sure that all is OK with the files
    for index in featuresPlaces.keys():
        if featuresPlaces[index] < 0:
            print ("indexs not found in request file in vectoriza_data.py: vectorizeFile")
            exit(0)
    if isLabeled and labelPlace<0:
        print ("indexs not found in request file in vectoriza_data.py: vectorizeFile")
        exit(0)

    # now that we have our indexes and feaures we write a new vector to each row
    for row in data:
        newRow=[]
        addAllToNewRow(row, newRow, featuresPlaces)
        if isLabeled:
            newRow.append(row[labelPlace]) # add label to vector
        newdata.append(newRow) # add new vector to newdata (file vectors)


# write output to file (vectors)
def writeVectorsFile (filepath,newdata,isLabeled):
    with open(filepath,'w') as f2:
        for row in newdata:
            for i in range (0,len(row)):
                if (i<len(row)-1):
                    f2.write('%s,' % row[i])
                else:
                    f2.write('%s' % row[i])
            f2.write('\n')
        f2.close()

# vectorizes all files in the Dir: requests files
def vectorizeFilesInDir(dataDirPath,vectorsDirPath,isLabeled):
    for filename in os.listdir(dataDirPath):
        if "empty" not in filename:
            filepath=dataDirPath+"/"+filename # oldpath
            filename=filename.split(".csv")[0]+"_vectors.csv" # newpath
            newpath=vectorsDirPath+"/"+filename
            with open(filepath) as f:
                data = list(csv.reader(f))
                f.close()
            newdata=list()
             # add headers to newdata
            headers=[]
            for key in allFeaturesDict.keys():
                headers.append(key)
            if isLabeled:
                headers.append("Label")
            newdata.append(headers)
            vectorizeFile(data,newdata,isLabeled)  # vectorize the request file
            writeVectorsFile(newpath,newdata,isLabeled)


#read all Features to dictionary
def readFeatures (featuresDirPath):
    for filename in os.listdir(featuresDirPath):
        if "empty" not in filename and "features" in filename:
            filepath=featuresDirPath+"/"+filename
            filename=filename.split("_")[0]
            allFeaturesDict[filename]=OrderedDict()  # init example: allFeaturesDict[Country]={}
            with open(filepath) as f:
                data = list(csv.reader(f))
                updateDict(data,allFeaturesDict[filename])
                f.close



#vectorizes the data in dataDirPath and save to vectorsDirPath
def dataToVectors (featuresDirPath, dataDirPath, vectorsDirPath,isLabeled):
    readFeatures(featuresDirPath)
    vectorizeFilesInDir(dataDirPath,vectorsDirPath,isLabeled)





