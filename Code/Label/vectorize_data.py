
# coding: utf-8


# this program vectorize the rows of the requests files in the given folder
# input: name of folder that contains requests files, and output folder for the vectors
# uses: the files from the "Features" folder
# output: writes vectors files to the Folders "TrainVectors" or "ValidationVectors" (chosen by input)



import os
import csv
from collections import OrderedDict

dict=OrderedDict()
# dict.update({"country":{}})
# dict.update({"continent":{}})
# dict.update({"opName":{}})
# dict.update({"osVer":{}})
# dict.update({"brwVer":{}})



#update dict from the scaled Features file
def updateDict (data, filename):
    data.reverse
    headline=data.pop(0)
    i=0
    for title in headline:
        if title=='fieldID':
            fieldIDPlace=i
        if title =='fieldName':
            fieldNamePlace=i
        i+=1
    for row in data:
        tempDict={row[fieldNamePlace]:row[fieldIDPlace]}
        dict[filename].update(tempDict)



#{"continent", "country", "opName", "osVer", "brwVer"}
featuresNames = {'TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City', 'OpName', 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration', 'Label', ''}

def changeFirstLetter(str):
    if not str:
        return str
    res = str[0].lower()
    res = res + str[1:]
    return res


def vectorizeFile(data, newdata, isLabeled, featuresOfInterest):
    headline=data.pop(0)
    i=0
    isUpdated = False

    # initialize featuresPlaces
    featuresPlaces = {}
    for feature in featuresOfInterest:
        featuresPlaces[feature] = -1

    for title in headline:
        # TODO remove func call to lowerFirstLetter
        titleToLower = title #changeFirstLetter(title) # 'OsVer' --> 'osVer'
        if titleToLower in featuresOfInterest:
            featuresPlaces[titleToLower] = i
        if title == "Label":
            labelPlace=i
        i+=1

    for feature in featuresPlaces.keys():
        if featuresPlaces[feature] > -1:
            isUpdated = True
            break

    if isUpdated:
        for row in data:
            newRow=[]
            addAllToNewRow(row, newRow, featuresOfInterest, featuresPlaces)
            if isLabeled:
                newRow.append(row[labelPlace])
            newdata.append(newRow)



# add all features to new line
def addAllToNewRow(row, newRow, featuresOfInterest, featuresPlaces):
    for feature in featuresOfInterest:
        addToNewRow(row, newRow, feature, featuresPlaces[feature])


# create a new vector from the given row
def addToNewRow (row,newRow,featureTitle,featurePlace):
    tempDict=dict[featureTitle] #dict -> country:[]
    currentField=row[featurePlace] #country-> England
    if currentField in tempDict:
        index=tempDict[currentField] #index = 3 (country[England]=3)
    else:
        index=0
    newRow.append(index)



def getHeadLine(featuresOfInterest):
    headline = featuresOfInterest[0]
    for i in range(1, len(featuresOfInterest)):
      headline = headline + ',' + featuresOfInterest[i]
    return headline

# write output to file (vectors)
def writeVectorsFile (filepath,newdata,isLabeled, featuresOfInterest):
    newdata.reverse
    # headline = "Continent,Country,OpName,OsVer,BrowserVer"
    headline = getHeadLine(featuresOfInterest)
    if isLabeled:
        headline = headline + ",label"
    headline = headline + "\n"

   
    with open(filepath,'w') as f2:
        f2.write('%s' % headline)
        for row in newdata:
            for i in range (0,len(row)):
                if (i<len(row)-1):
                    f2.write('%s,' % row[i])
                else:
                    f2.write('%s' % row[i])    
            f2.write('\n')
        f2.close() 



#vectorizes all files in the Dir
def vectorizeFilesInDir(dataDirPath,vectorsDirPath,isLabeled, featuresOfInterest):
    for filename in os.listdir(dataDirPath):
        if "empty" not in filename:
            filepath=dataDirPath+"/"+filename #oldpath

            filename=filename.split(".csv")[0]+"_vectors.csv" #newpath
            newpath=vectorsDirPath+"/"+filename
            with open(filepath) as f:
                data = list(csv.reader(f))
                newdata=list()
                vectorizeFile(data,newdata,isLabeled, featuresOfInterest)

            writeVectorsFile(newpath,newdata,isLabeled, featuresOfInterest)


def initDict(featuresOfInterest):
    for feature in featuresOfInterest:
        dict.update({feature:{}})


#read all "Features" to dictionary
def readFeatures (featuresDirPath):
    for filename in os.listdir(featuresDirPath):
        if "empty" not in filename and "features" in filename:
            filepath=featuresDirPath+"/"+filename
            filename=filename.split("_")[0]
            with open(filepath) as f:
                data = list(csv.reader(f))
                dict.update({filename:{}})
                updateDict(data,filename)
                f.close



#vectorizes the data in dataDirPath and save to vectorsDirPath

#featuresDirPath="Data/Features"
#dataDirPath="Data/LabeledData"

def dataToVectors (featuresDirPath, dataDirPath, vectorsDirPath,isLabeled, featuresOfInterest):
    initDict(featuresOfInterest)
    readFeatures(featuresDirPath)
    vectorizeFilesInDir(dataDirPath,vectorsDirPath,isLabeled, featuresOfInterest)





