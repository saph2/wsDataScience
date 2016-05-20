
# coding: utf-8


# this program builds the bar we will use for labeling our data
# the input are requests files found in the Dir: "Data/DataForBar"
# the program finds the minimum request's duration per Host and Url and saves it in a dictionary
# for exmp: host_name:url_base:minimum_duration
# output: the dictionary is saved to a file called "barFile" in the same Dir



import numpy as np
import csv
import os
from collections import OrderedDict
barDict = OrderedDict()
allfiles=list()



def readFileToList(filepath):
    with open(filepath) as f:
        data = list(csv.reader(f))
        f.close
    return data


#add/update to dictionary from a single request file: (Host->URL->MinDuration)
def insertToDict (data,hostplace,urlplace,durplace):
    for line in data:
        try:
            hostname=line[hostplace]
            urlname=line[urlplace]
            dur=float(line[durplace])
            urldict={urlname:[dur,dur]}
        except:
            print ("index out of bounds in build_duration_bar.py: insertToDict")
            exit(0)
        if hostname not in barDict.keys(): #update new host
            barDict[hostname]=urldict
        else:
            allurls=barDict[hostname] #all the host's urls
            if urlname not in allurls.keys(): #update new url
                barDict[hostname].update(urldict)
            else: #update min and max dur for existing host and url
                mindur=np.minimum(dur,allurls[urlname][0])
                maxdur=np.maximum(dur,allurls[urlname][1])
                barDict[hostname].update({urlname:[mindur,maxdur]})  #update min and max duration time

#fill the dictionary from all the requests files
def createDictFromAllFiles (allfiles):
    for filepath in allfiles:
        data=readFileToList(filepath)
        #find the place of the host, url and reqDuration in the data
        data.reverse
        headline=data.pop(0)
        hostplac=-1
        urlplace=-1
        durplace=-1
        i=0
        for title in headline:
            if title=='RoleInst':
                hostplace=i
            if title =='UrlBase':
                urlplace=i
            if title=='ReqDuration':
                durplace=i
            i+=1
        #add data to dict
        if hostplace<0 or urlplace<0 or durplace<0:
            print "indexs not found in request file in build_duration_bar.py: createDictFromAllFiles"
            exit(0)
        insertToDict(data,hostplace,urlplace,durplace)



#save dictionary to File
def saveDictToFile(dirpath):
    barPath=dirpath+"/barFile.csv"
    with open(barPath,'w') as f2:
        f2.write("Host,URL,MinDuration,MaxDuration\n")
        for host in barDict:
            hostdict=barDict[host]
            for url in hostdict:
                dur=hostdict[url]
                f2.write("%s,%s,%f,%f\n" % (host, url, dur[0], dur[1]))
        f2.close()



#create a dictionary from files in the form of: (Host->URL->MinDuration)
#dirpath="Data/DataForBar"
def buildBar(dirpath, barFolder):
    for filename in os.listdir(dirpath): #add all requests files in the diractory
        if "empty" not in filename and "bar" not in filename:
            allfiles.append(dirpath+"/"+filename)
    createDictFromAllFiles(allfiles)
    saveDictToFile(barFolder)





