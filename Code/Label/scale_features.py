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

continentDict = OrderedDict()
countryDict = OrderedDict()
opNameDict = OrderedDict()
osVerDict = OrderedDict()
brwVerDict = OrderedDict()
tempDict = OrderedDict()



# for the given feature - update its dictionary
# dictionary build for exmp: country_name: [count #label '0', count #label '1']
def updateFeature(row, featurePlace, featureDict, labelPlace):
    featureName = row[featurePlace]
    label = int(row[labelPlace])
    if featureName not in featureDict:
        newCounter = [0, 0]
        featureDict.update({featureName: newCounter})
    featureDict[featureName][label] += 1



#updateFeatureAllDicts(row, featuresIndexes, allFeatureDicts,labelPlace)

# update all the dictionaries with the info from the current file
def updateFeaturesInAllDicts(row, featuresPlaces, allFeaturesDicts, labelPlace):
    for feature in featuresPlaces.keys():
        updateFeature(row, featuresPlaces[feature], allFeaturesDicts[feature], labelPlace)


#<type 'list'>: ['TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', '']

def updateAllDict(data, allFeaturesDicts, featuresOfInterest):
    data.reverse
    headline = data.pop(0)
    i = 0
    isUpdated = False

    featuresPlaces = {}
    # initialize featuresOfInterest to -1
    for feature in featuresOfInterest:
        featuresPlaces[feature] = -1

    for title in headline:
        # save only the label
        if title == "Label":
            labelPlace = i

        # save all features besides the label
        if title in featuresOfInterest:
            # title = vectorize_data.changeFirstLetter(title)
            featuresPlaces[title] = i

        i += 1

    # make sure that all is OK with the files
    for index in featuresPlaces.keys():
        if featuresPlaces[index] > -1:
            isUpdated = True
            break

    # if all is OK then isUpdated == True
    if isUpdated:
        for row in data:  # update all dictionaries for each row in the data
            updateFeaturesInAllDicts(row, featuresPlaces, allFeaturesDicts, labelPlace)




# return the dictionary build for exmp: country_name: #busy/#total
def getBusyPerDict(dictName):
    tempDict.clear()
    for key in dictName:
        busy = float(dictName[key][1]) / float(dictName[key][0] + dictName[key][1])
        tempDict.update({key: busy})
    return tempDict



# save dictionary to file

# featuresDirPath="Data/Features"

def dictToFile(dictName, fileName, featuresDirPath):
    # call for probability analysis function
    dictName = getBusyPerDict(dictName)

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
def writeDictsToFiles(featuresOfInterest, allFeaturesDicts, featuresDirPath):
    for feature in featuresOfInterest:
        dictToFile(allFeaturesDicts[feature], feature, featuresDirPath)



# create features files from the labeled data

# dataDirPath="Data/LabeledData"


def buildFeaturesFiles(dataDirPath, featuresDirPath, featuresOfInterest):
    # create all dictionaries
    allFeaturesDicts = {}
    for feature in featuresOfInterest:
        allFeaturesDicts[feature] = {}

    # go over each file and update all the dictionaries
    for filename in os.listdir(dataDirPath):
        if not "empty" in filename and "labeled" in filename:
            filepath = dataDirPath + "/" + filename
            with open(filepath) as f:
                data = list(csv.reader(f))
                # f.close
            updateAllDict(data, allFeaturesDicts, featuresOfInterest)

    # send all the updated dictionaries to files
    # dictToFile(continentDict, "continent", featuresDirPath)
    # dictToFile(countryDict, "country", featuresDirPath)
    # dictToFile(opNameDict, "opName", featuresDirPath)
    # dictToFile(osVerDict, "osVer", featuresDirPath)
    # dictToFile(brwVerDict, "brwVer", featuresDirPath)

    writeDictsToFiles(featuresOfInterest, allFeaturesDicts, featuresDirPath)





