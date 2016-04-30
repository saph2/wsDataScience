
# coding: utf-8

# In[1]:

# this program vectorize the rows of the requests files in the given folder
# input: name of folder that contains requests files, and output folder for the vectors
# uses: the files from the "Features" folder
# output: writes vectors files to the Folders "TrainVectors" or "TestVectors" (chosen by input)


# In[2]:

import os
import csv
from collections import OrderedDict

dict=OrderedDict()
dict.update({"country":{}})
dict.update({"continent":{}})
dict.update({"opName":{}})
dict.update({"osVer":{}})
dict.update({"brwVer":{}})


# In[3]:

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


# In[4]:

#create a vectorized data for the current file
def vectorizeFile (data,newdata,isLabeled):
    data.reverse
    headline=data.pop(0)
    i=0
    for title in headline:
        if title=='Continent':
            continentPlace=i
        if title =='Country':
            countryPlace=i
        if title=='OpName':
            opNamePlace=i
        if title == "OsVer":
            osVerPlace=i
        if title == "BrowserVer":
            brwVerPlace=i
        if title == "Label":
            labelPlace=i
        i+=1
    for row in data:
        newRow=[]
        addToNewRow(row,newRow,'continent',continentPlace)
        addToNewRow(row,newRow,'country',countryPlace)
        addToNewRow(row,newRow,'opName',opNamePlace)
        addToNewRow(row,newRow,'osVer',osVerPlace)
        addToNewRow(row,newRow,'brwVer',brwVerPlace)
        if isLabeled:
            newRow.append(row[labelPlace])
        newdata.append(newRow)


# In[5]:

# create a new vector from the given row
def addToNewRow (row,newRow,featureTitle,featurePlace):
    tempDict=dict[featureTitle] #dict -> country:[]
    currentField=row[featurePlace] #country-> England
    if currentField in tempDict:
        index=tempDict[currentField] #index = 3 (country[England]=3)
    else:
        index=0
    newRow.append(index)


# In[6]:

# write output to file (vectors)
def writeVectorsFile (filepath,newdata,isLabeled):
    newdata.reverse
    
    if isLabeled:
        headline="Continent,Country,OpName,OsVer,BrowserVer,Label\n"
    else:
        headline="Continent,Country,OpName,OsVer,BrowserVer\n"
   
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


# In[7]:

#vectorizes all files in the Dir
def vectorizeFilesInDir (dataDirPath,vectorsDirPath,isLabeled):
    for filename in os.listdir(dataDirPath):
        
        filepath=dataDirPath+"/"+filename #oldpath
        
        filename=filename.split(".csv")[0]+"_vectors.csv" #newpath
        newpath=vectorsDirPath+"/"+filename
        
        with open(filepath) as f:
            data = list(csv.reader(f))
            newdata=list()
            vectorizeFile(data,newdata,isLabeled)
            f.close
        
        writeVectorsFile(newpath,newdata,isLabeled)


# In[8]:

#read all "Features" to dictionary
def readFeatures (featuresDirPath):
    for filename in os.listdir(featuresDirPath):
        if "features" in filename:
            filepath=featuresDirPath+"/"+filename
            filename=filename.split("_")[0]
            with open(filepath) as f:
                data = list(csv.reader(f))
                updateDict(data,filename)
                f.close


# In[9]:

#vectorizes the data in dataDirPath and save to vectorsDirPath

#featuresDirPath="Data/Features"
#dataDirPath="Data/LabeledData"

def dataToVectors (featuresDirPath, dataDirPath, vectorsDirPath,isLabeled):
    readFeatures(featuresDirPath)
    vectorizeFilesInDir(dataDirPath,vectorsDirPath,isLabeled) 


# In[ ]:



