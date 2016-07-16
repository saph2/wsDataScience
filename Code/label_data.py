# coding: utf-8


# this program labels our data
# the input are requests files found in the Dir: "Data/DataToLabel"
# and it uses the bar file from the path: ""Data/DataForBar/barFile.csv"
# the program goes over each request file and label the row according to the results from the func: "isBusy"
# the function uses the min duration per host+url info found in the barFile in order to choose a label
# output: each file is saved as it was, with the exception of an additional label column, to the Dir: "Data/labeledData"



import numpy as np
import csv
import os
from collections import OrderedDict

allfiles = list()
barDict = OrderedDict()


# read dictionary File into dictionary DataStruct
def readBarFile(barDirPath):
    barPath = barDirPath + "/barFile.csv"
    with open(barPath) as f:
        dictdata = list(csv.reader(f))
        f.close
    dictdata.reverse
    headline = dictdata.pop(0)
    hostplace = -1
    urlplace = -1
    avgdurplace = -1
    conplace=-1
    i = 0
    for title in headline:
        if title == 'Host':
            hostplace = i
        if title == 'URL':
            urlplace = i
        if title == 'avgDuration':
            avgdurplace = i
        if title == 'minDuration':
            mindurplace = i
        if title == 'maxDuration':
            maxdurplace = i
        if title == 'Continent':
            conplace = i
        i += 1
    if hostplace < 0 or urlplace < 0 or avgdurplace < 0 or mindurplace < 0 or maxdurplace < 0 or conplace < 0:
        print ("indexs not found in request file in label_data.py: readBarFile")
        exit(0)
    for line in dictdata:
        try:
            hostname = line[hostplace]
            urlname = line[urlplace]
            coname = line[conplace]
            avgdur = float(line[avgdurplace])
            mindur = float(line[mindurplace])
            maxdur = float(line[maxdurplace])
        except:
            print ("index out of bounds in label_data.py: readBarFile")
            exit(0)
        if hostname not in barDict.keys():  # update host
            barDict[hostname] = OrderedDict()
        codict={coname:[avgdur,mindur,maxdur]}
        if urlname not in barDict[hostname]:
            barDict[hostname].update({urlname: codict})  # update new url
        else:
            (barDict[hostname])[urlname].update(codict) # update new continent


# read the file intended to be labeled into DataStructure
def readFileToList(filepath, newpath):
    with open(filepath) as f:
        with open(newpath, 'w') as f2:
            writer = csv.writer(f2)
            for row in csv.reader(f):
                writer.writerow(row + ["Label"])
            f2.close
        f.close
    with open(newpath, 'r') as f2:
        data = list(csv.reader(f2))
        f2.close
    return data


# function for deciding busy row or not
def isBusy(lineDur,avgdur,mindur,maxdur,numberOfClasses):
    diff=(float(maxdur-avgdur)/numberOfClasses-1)
    for i in range(0, numberOfClasses-1):
      if lineDur < avgdur + (i*diff):
            return i
    return (numberOfClasses - 1)  # maxValue


# save labeled data to file
def labeledDataToFile(filepath, data):
    with open(filepath, 'w') as f2:
        for line in data:
            for word in line:
                f2.write('%s,' % word)
            f2.write('\n')
        f2.close()


def labelTheData(data, numberOfClasses):
    data.reverse
    headline = data.pop(0)
    hostplace = -1
    urlplace = -1
    durplace = -1
    labelplace = -1
    conplace=-1
    i = 0
    # find indexes
    for title in headline:
        if title == 'RoleInst':
            hostplace = i
        if title == 'UrlBase':
            urlplace = i
        if title == 'ReqDuration':
            durplace = i
        if title == 'Label':
            labelplace = i
        if title == "Continent":
            conplace=i
        i += 1
    # label the rows
    if hostplace < 0 or urlplace < 0 or durplace < 0 or labelplace < 0 or conplace < 0:
        print ("indexs not found in request file in label_data.py: labelTheData")
        exit(0)
    for line in data:
        try:
            lineHost = line[hostplace]
            lineUrl = line[urlplace]
            lineCon = line[conplace]
            lineDur = float(line[durplace])
            try:
                avgDur = float(barDict[lineHost][lineUrl][lineCon][0])
                minDur = float(barDict[lineHost][lineUrl][lineCon][1])
                maxDur = float(barDict[lineHost][lineUrl][lineCon][2])
                # check if busy row
                label = isBusy(lineDur,avgDur,minDur,maxDur,numberOfClasses)  # label row
            except:
                label = 0
            line[labelplace] = label  # label the row
        except:
            print ("index out of bounds in label_data.py: labelTheData")
            exit(0)
    data.insert(0, headline)


# label all files in the dir
def labelAllfiles(dataDir, labelDir, barDir, numberOfClasses):
    readBarFile(barDir)  # update bar dictionary

    for filename in os.listdir(dataDir):  # add all requests files in the diractory
        if "empty" not in filename:
            filepath = dataDir + "/" + filename  # oldpath

            newpath = labelDir + "/" + filename  # newpath
            newpath = newpath.split(".csv")[0] + "_labeled.csv"

            # copy the file to the labelDir and add "Label" column then save to Data
            data = readFileToList(filepath, newpath)

            # label the data of the file
            labelTheData(data, numberOfClasses)

            # save data to file
            labeledDataToFile(newpath, data)
