
# coding: utf-8

# In[40]:

# this program labels our data
# the input are requests files found in the Dir: "Data/DataToLabel"
# and it uses the bar file from the path: ""Data/DataForBar/barFile.csv"
# the program goes over each request file and label the row according to the results from the func: "isBusy"
# the function uses the min duration per host+url info found in the barFile in order to choose a label
# output: each file is saved as it was, with the exception of an additional label column, to the Dir: "Data/labeledData"


# In[49]:

import numpy as np
import csv
import os
allfiles=list()
dict = {}


# In[50]:

#read dictionary File into dictionary DataStruct
def readBarFile(barDirPath):
    barPath=barDirPath+"/barFile.csv"
    with open(barPath) as f:
        dictdata = list(csv.reader(f))
        f.close
    dictdata.reverse
    headline=dictdata.pop(0)
    i=0
    for title in headline:
        if title=='Host':
            hostplace=i
        if title =='URL':
            urlplace=i
        if title=='MinDuration':
            durplace=i
        i+=1
    for line in dictdata:
        hostname=line[hostplace]
        urlname=line[urlplace]
        dur=float(line[durplace])
        urldict={urlname:dur}
        if hostname not in dict: #update new host
            dict.update({hostname:urldict})
        else:
            allurls=dict[hostname] #the current host url's list
            if urlname not in allurls: #update new url
                dict[hostname].update(urldict)


# In[51]:

#read the file intended to be labeled into DataStructure
def readFileToList(filepath,newpath):
    with open(filepath) as f:
        with open(newpath,'w') as f2:
            writer=csv.writer(f2)
            for row in csv.reader(f):
                writer.writerow(row+["Label"])
            f2.close
        f.close
    with open(newpath,'r') as f2:
        data = list(csv.reader(f2))
        f2.close
    return data


# In[52]:

#function for deciding busy row or not
def isBusy(lineDur,minDur):
    if lineDur>=(2*minDur): #twice as minimum duration
        return 1
    else:
        return 0


# In[53]:

#save labeled data to file
def labeledDataToFile(filepath,data):
    with open(filepath,'w') as f2:
        for line in data:
            for word in line:
                f2.write('%s,' % word)
            f2.write('\n')
        f2.close()


# In[54]:

# label the data from a single file

def labelTheData (dict,data):
    data.reverse
    headline=data.pop(0)
    i=0
    #find indexes
    for title in headline:
        if title=='Host':
            hostplace=i
        if title =='UrlBase':
            urlplace=i
        if title=='ReqDuration':
            durplace=i
        if title=='Label':
            labelplace=i
        i+=1
    #label the rows
    for line in data:
        lineHost=line[hostplace]
        lineUrl=line[urlplace]
        lineDur=float(line[durplace])
        minDur=(dict[lineHost])[lineUrl]
        #check if busy row
        line[labelplace]=isBusy(lineDur,minDur) #label row
    data.insert(0,headline)


# In[55]:

#label all files in the dir

#dataDir="Data/DataToLabel"
#labelDir="Data/LabeledData"
#barDir="Data/DataForBar"

def labelAllfiles(dataDir,labelDir,barDir):
    
    readBarFile(barDir)#update bar dictionary
    
    for filename in os.listdir(dataDir): #add all requests files in the diractory
            
        filepath=dataDir+"/"+filename #oldpath
            
        newpath=labelDir+"/"+filename #newpath
        newpath=newpath.split(".csv")[0]+"_labeled.csv"
              
        #copy the file to the labelDir and add "Label" column then save to Data
        data=readFileToList(filepath,newpath) 
        
        #label the data of the file
        labelTheData (dict,data)
        
        #save data to file
        labeledDataToFile(newpath,data)


# In[ ]:



