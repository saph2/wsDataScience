# coding: utf-8


# this program reads all labeled files from "LabeledData" Dir
# the program orders fields in selected features by the prob of having a "busy" label (out of the total count for the field)
# for exmp: fot the feature "Country" we have a list of fields: "England","Isreal" ext...
# ordered as such ["England": prob(busy_in_England)] and so on for all fields under "Country"
# the output are files for each feature, containing all the fields and prob as written above
# the fields in each file are ordered in ascending order of prob(busy_for_field)
# the files are saved in Dir: "Data/Features"



import os
import csv
from collections import OrderedDict

from Code.Label import vectorize_data

# for the given feature - update its dictionary from the given row
# dictionary build for exmp: country_name: [count #label '0', count #label '1']
def updateFeature(row, featurePlace, featureDict, labelPlace,numberOfClasses):
    featureName = row[featurePlace] #row[countryName] = England
    label = int(row[labelPlace]) #row[label]=1
    if featureName not in featureDict:
        newCounter = [0 for i in range(0,numberOfClasses)]
        featureDict.update({featureName: newCounter})
    featureDict[featureName][label] += 1 #DictCountry[England][1]+=1



# update all the dictionaries with the info from current row in the current file
def updateFeaturesInAllDicts(row, featuresPlaces, allFeaturesDicts, labelPlace,numberOfClasses):
    for feature in featuresPlaces.keys():
        updateFeature(row, featuresPlaces[feature], allFeaturesDicts[feature], labelPlace,numberOfClasses)  #send: (row, countyIndex, countryDict, labelIndex)


#<type 'list'>: ['TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', '']

# update all the dictionaries with the info from the current file
def updateAllDict(data, allFeaturesDicts, featuresOfInterest,numberOfClasses):
    data.reverse
    headline = data.pop(0)

    featuresPlaces = {}
    for feature in featuresOfInterest:  # initialize featuresOfInterestIndex to -1
        featuresPlaces[feature] = -1
    labelPlace=-1

    i = 0
    for title in headline: # save only the label
        if title == "Label":
            labelPlace = i
        if title in featuresOfInterest: # save all features besides the label
            featuresPlaces[title] = i
        i += 1

    # make sure that all is OK with the files
    for index in featuresPlaces.keys():
        if featuresPlaces[index] < 0:
            print ("indexs not found in request file in label_data.py: updateAllDict")
            exit(0)
    if labelPlace<0:
        print ("indexs not found in request file in scale_features.py: updateAllDict")
        exit(0)

    for row in data:  # update all dictionaries for each row in the data
        updateFeaturesInAllDicts(row, featuresPlaces, allFeaturesDicts, labelPlace,numberOfClasses)

# return the dict tuples and busy prop:
# input: county-> England-> [busy, notBusy]
# output: country -> England -> #busy/#total

def getBusyPerDict(dictName,numberOfClasses):
    tempDict = OrderedDict()
    for key in dictName:# to change!!
        total=dictName[key][0]
        onlyBusy=0
        for i in range (1,numberOfClasses):
            onlyBusy+=dictName[key][i]*i
        total+=onlyBusy
        busy = float(onlyBusy / total)
        tempDict.update({key: busy})
    return tempDict



# save dictionary to file
def dictToFile(dictName, fileName, featuresDirPath,numberOfClasses):
    # call for probability analysis function
    dictName = getBusyPerDict(dictName,numberOfClasses)

    # order keys by busy values
    dictName = OrderedDict(sorted(dictName.items(), key=lambda t: t[1]))

    filepath = featuresDirPath + "/" + fileName + "_features.csv"
    with open(filepath, 'w') as f2:
        fieldID = 1  # number each field
        f2.write('fieldName,busyFromTotal,fieldID\n')
        for key in dictName:
            f2.write('%s,' % key)
            f2.write('%f,' % dictName[key])
            f2.write('%d,' % fieldID)
            f2.write('\n')
            fieldID += 1
        f2.close()


# write all updated dictionaries to files
def writeDictsToFiles(featuresOfInterest, allFeaturesDicts, featuresDirPath,numberOfClasses):
    for feature in featuresOfInterest:
        dictToFile(allFeaturesDicts[feature], feature, featuresDirPath,numberOfClasses)



# create features files from the labeled data
def buildFeaturesFiles(dataDirPath, featuresDirPath, featuresOfInterest,numberOfClasses):
    # create all dictionaries
    allFeaturesDicts = OrderedDict()
    for feature in featuresOfInterest:
        allFeaturesDicts[feature] = OrderedDict()
    # go over each file and update all the dictionaries
    for filename in os.listdir(dataDirPath):
        if not "empty" in filename and "labeled" in filename:
            filepath = dataDirPath + "/" + filename
            with open(filepath) as f:
                data = list(csv.reader(f))
                f.close()
            updateAllDict(data, allFeaturesDicts, featuresOfInterest,numberOfClasses)

    #write the dicts to their files
    writeDictsToFiles(featuresOfInterest, allFeaturesDicts, featuresDirPath,numberOfClasses)





