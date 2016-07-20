# coding: utf-8

# This program gives a numerical representation to the values of the selected features
# The input are the labeled train set.
# It calculates the probability for each feature's value to appear in a busy request
# The values are then ordered by their probabilities and numbered accordingly
# The output is a file for each feature with the numerical representation for each of its values
# (for example: 'England'->17)
# Results are saved to: "Data/Features" and "Model/all_features.json"


import json
import os
import csv
from collections import OrderedDict

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
    for key in dictName:
        total=dictName[key][0]
        onlyBusy=0
        for i in range (1,numberOfClasses):
            onlyBusy+=dictName[key][i]*i
        total+=onlyBusy
        busy = (float(onlyBusy) / total)
        tempDict.update({key: busy})
    return tempDict


allDictsForJson = {}
# save dictionary to file
def dictToFile(dictName, fileName, featuresDirPath,numberOfClasses):
    # call for probability analysis function
    dictName = getBusyPerDict(dictName,numberOfClasses)

    # order keys by busy values
    dictName = OrderedDict(sorted(dictName.items(), key=lambda t: t[1]))

    dictOfKeys = {}

    filepath = featuresDirPath + "/" + fileName + "_features.csv"
    with open(filepath, 'w') as f2:
        fieldID = 1  # number each field
        f2.write('fieldName,busyFromTotal,fieldID\n')
        for key in dictName:
            dictOfKeys[key] = fieldID
            f2.write('%s,' % key)
            f2.write('%f,' % dictName[key])
            f2.write('%d,' % fieldID)
            f2.write('\n')
            fieldID += 1
        f2.close()

    allDictsForJson[fileName] = convertDictToUTF8(dictOfKeys)


# write all updated dictionaries to files
def writeDictsToFiles(featuresOfInterest, allFeaturesDicts, featuresDirPath,numberOfClasses):
    for feature in featuresOfInterest:
        dictToFile(allFeaturesDicts[feature], feature, featuresDirPath,numberOfClasses)


def convertDictToUTF8(oldDict):
    newDict = {}
    for key, val in oldDict.iteritems():
        try:
            k = key.encode('utf-8')
            newDict[k] = val
        except:
            pass
    return newDict


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

    # write all dicts to one json file.
    # keys are the featuresOfInterest
    # values are the dicts holding (key = one feature, value = num of 0's and num of 1's)
    with open('../Model/all_features.json', 'w') as f2:
        # jsonStr = json.dumps(allDictsForJson, indent=4, ensure_ascii=False)
        # f2.write(jsonStr)
        # json.dump(allDictsForJson, f2, indent=4)
        json.dump(allDictsForJson, f2, sort_keys=True, indent=4)
        print 'finished writing JSON file'




