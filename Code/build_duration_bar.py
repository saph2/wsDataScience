
# coding: utf-8


# This program builds the file we will use for labeling our data
# The program finds the average request's duration per Host and Url and Continent
# Output saved to: "Data/DurationBar/barFile.csv"


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


#add/update to dictionary from a single request file: (Host->URL->Continent->AvgDuration)
def insertToDict (data,hostplace,urlplace,durplace,conplace):
    for line in data:
        try:
            hostname=line[hostplace]
            urlname=line[urlplace]
            coname=line[conplace]
            dur=float(line[durplace])
            codict={coname:[dur,1,dur,dur]}
            urldict={urlname:codict}
        except:
            print ("index out of bounds in build_duration_bar.py: insertToDict")
            exit(0)
        if hostname not in barDict.keys(): #update new host
            barDict[hostname]=urldict
        else:
            allurls=barDict[hostname] #all the host's urls
            if urlname not in allurls.keys(): #update new url
                barDict[hostname].update(urldict)
            elif coname not in (barDict[hostname])[urlname]:
                (barDict[hostname])[urlname].update(codict)
            else:# update sum and count dur for existing host and url
                currcodict=(allurls[urlname])[coname]
                sumdur=currcodict[0]+dur
                countdur=currcodict[1]+1
                mindur=min(dur,currcodict[2])
                maxdur=max(dur,currcodict[3])
                (barDict[hostname])[urlname].update({coname:[sumdur,countdur,mindur,maxdur]})  #update min and max duration time

#fill the dictionary from all the requests files
def createDictFromAllFiles (allfiles):
    for filepath in allfiles:
        data=readFileToList(filepath)
        #find the place of the host, url and reqDuration in the data
        data.reverse
        headline=data.pop(0)
        hostplace=-1
        urlplace=-1
        durplace=-1
        conplace=-1
        i=0
        for title in headline:
            if title=='RoleInst':
                hostplace=i
            if title =='UrlBase':
                urlplace=i
            if title=='ReqDuration':
                durplace=i
            if title=='Continent':
                conplace=i
            i+=1
        #add data to dict
        if hostplace<0 or urlplace<0 or durplace<0 or conplace<0:
            print "indexs not found in request file in build_duration_bar.py: createDictFromAllFiles"
            exit(0)
        insertToDict(data,hostplace,urlplace,durplace,conplace)



#save dictionary to File
def saveDictToFile(dirpath):
    barPath=dirpath+"/barFile.csv"
    with open(barPath,'w') as f2:
        f2.write("Host,URL,Continent,avgDuration,minDuration,maxDuration\n")
        for host in barDict:
            hostdict=barDict[host]
            for url in hostdict:
                urldict=hostdict[url]
                for continent in urldict:
                    dur=urldict[continent]
                    avgdur=float(dur[0])/dur[1]
                    f2.write("%s,%s,%s,%f, %f, %f\n" % (host, url, continent, avgdur,dur[2],dur[3]))
        f2.close()



#create a dictionary from files in the form of: (Host->URL->Continent->AvgDuration)
def buildBar(dirpath, barFolder):
    for filename in os.listdir(dirpath): #add all requests files in the diractory
        if "empty" not in filename and "bar" not in filename:
            allfiles.append(dirpath+"/"+filename)
    createDictFromAllFiles(allfiles)
    saveDictToFile(barFolder)





