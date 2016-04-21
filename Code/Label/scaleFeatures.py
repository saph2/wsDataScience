
# coding: utf-8

# In[28]:

# this program reads all labeled files from "LabeledData" Dir
# the program orders fields in selected features by the prob of having a "busy" label (out of the total count for the field)
# for exmp: fot the feature "Country" we have a list of fields: "England","Isreal" ext...
# ordered as such ["England": prob(busy_in_England)] and so on for all fields under "Country"
# the output are files for each feature, containing all the fields and prob as written above
# the fields in each file are ordered in ascending order of prob(busy_for_field)
# the files are saved in Dir: "Data/Features"


# In[29]:

import os
import csv
from collections import OrderedDict

continentDict=OrderedDict()
countryDict=OrderedDict()
opNameDict=OrderedDict()
osVerDict=OrderedDict()
brwVerDict=OrderedDict()
tempDict=OrderedDict()


# In[30]:

#for the given feature - update its dictionary
#dictionary build for exmp: country_name: [count #label '0', count #label '1']
def updateFeature(row, featurePlace, featureDict, labelPlace):
    featureName=row[featurePlace]
    label=int(row[labelPlace])
    if featureName not in featureDict:
        newCounter=[0,0]
        featureDict.update({featureName:newCounter})
    featureDict[featureName][label]+=1


# In[31]:

#update all the dictionaries with the info from the current file
def updateAllDict(data):
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
    for row in data:#update all dictionaries for each row in the data
        updateFeature(row,continentPlace,continentDict,labelPlace) 
        updateFeature(row,countryPlace,countryDict,labelPlace)
        updateFeature(row,opNamePlace,opNameDict,labelPlace)
        updateFeature(row,osVerPlace,osVerDict,labelPlace)
        updateFeature(row,brwVerPlace,brwVerDict,labelPlace)      


# In[32]:

#return the dictionary build for exmp: country_name: #busy/#total
def getBusyPerDict(dictName):
    tempDict.clear()
    for key in dictName:
        busy=float(dictName[key][1])/float(dictName[key][0]+dictName[key][1])
        tempDict.update({key:busy})
    return tempDict


# In[33]:

#save dictionary to file
def dictToFile(dictName, fileName):
    
    #call for probability analysis function
    dictName=getBusyPerDict(dictName)
    
    #order keys by busy values
    dictName=OrderedDict(sorted(dictName.items(), key=lambda t: t[1]))
    
    filepath="Data/Features/"+fileName+"_Features.csv"
    with open(filepath,'w') as f2:
        fieldID=1 #number each field
        f2.write('%s,busyFromTotal,fieldID\n' % fileName)
        for key in dictName:
            f2.write('%s,' % key)
            f2.write('%f,' % dictName[key])
            f2.write('%d,' % fieldID)
            f2.write('\n')
            fieldID+=1
        f2.close()


# In[34]:

#read all the files from Dir to list
allfiles=list()
dirpath="Data/LabeledData"
for filename in os.listdir(dirpath): #add all requests files in the diractory
    if "labeled" in filename:
        allfiles.append("Data/LabeledData/"+filename)


# In[35]:

#go over each file and update all the dictionaries 
for filename in allfiles:
    with open(filename) as f:
        data = list(csv.reader(f))
        f.close
    updateAllDict(data)


# In[36]:

#send all the updated dictionaries to files
dictToFile(continentDict,"continent")
dictToFile(countryDict,"country")
dictToFile(opNameDict,"opName")
dictToFile(osVerDict,"osVer")
dictToFile (brwVerDict,"brwVer")


# In[ ]:



