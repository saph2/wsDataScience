
# coding: utf-8


# this program builds the bar we will use for labeling our data
# the input are requests files found in the Dir: "Data/DataForBar"
# the program finds the minimum request's duration per Host and Url and saves it in a dictionary
# for exmp: host_name:url_base:minimum_duration
# output: the dictionary is saved to a file called "barFile" in the same Dir



import numpy as np
import csv
import os
dict = {}
allfiles=list()



def readFileToList(filepath):
    with open(filepath) as f:
        data = list(csv.reader(f))
        f.close
    return data



#add/update to dictionary from a single request file: (Host->URL->MinDuration) 
def insertToDict (dict,data,hostplace,urlplace,durplace):
    for line in data:
        try:
            #FIXME: round over cause line length was less then the host place
            if len(line) < hostplace:
                return 0
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
                else: #update min dur for existing host and url
                    mindur=np.minimum(dur,allurls[urlname])
                    (dict[hostname])[urlname]=mindur  #update min duration time

        except:
            print "index out of bounds in build_duration_bar.pyinsertToDict"


#fill the dictionary from all the requests files
def createDictFromAllFiles (dict,allfiles):
    for filepath in allfiles:
        data=readFileToList(filepath)
        #find the place of the host, url and reqDuration in the data
        data.reverse
        headline=data.pop(0)
        i=0
        # featuresIndex = {}
        for title in headline:
            if title=='RoleInst':
                hostplace=i
            if title =='UrlBase':
                urlplace=i
            if title=='ReqDuration':
                durplace=i
            # if title in featuresOfInterest:
            #     featuresIndex[title] = i
            i+=1
        #add data to dict
        insertToDict(dict,data,hostplace,urlplace,durplace)        



#save dictionary to File
def saveDictToFile(dirpath):
    barPath=dirpath+"/barFile.csv"
    with open(barPath,'w') as f2:
        f2.write("Host,URL,MinDuration\n")
        for host in dict:
            hostdict=dict[host]
            for url in hostdict:
                dur=hostdict[url]
                f2.write("%s,%s,%f\n" % (host, url, dur))
        f2.close()



#create a dictionary from files in the form of: (Host->URL->MinDuration) 
#dirpath="Data/DataForBar"
def buildBar(dirpath, barFolder):
    for filename in os.listdir(dirpath): #add all requests files in the diractory
        if "empty" not in filename and "bar" not in filename:
            allfiles.append(dirpath+"/"+filename)
    createDictFromAllFiles(dict, allfiles)
    saveDictToFile(barFolder)




