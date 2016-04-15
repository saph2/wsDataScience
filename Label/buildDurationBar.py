
# coding: utf-8

# In[7]:

import numpy as np
import csv


# In[8]:

def readFileToList(filepath):
    with open(filepath) as f:
        data = list(csv.reader(f))
        f.close
    return data


# In[9]:

#add/update to dictionary from a single request file: (Host->URL->MinDuration) 
def insertToDict (dict,data,hostplace,urlplace,durplace):
    for line in data:
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


# In[10]:

#fill the dictionary from all the reqests files
def createDictFromAllFiles (dict,allfiles):
    for filepath in allfiles:
        data=readFileToList(filepath)
        #find the place of the host, url and reqDuration in the data
        data.reverse
        headline=data.pop(0)
        i=0
        for title in headline:
            if title=='Host':
                hostplace=i
            if title =='UrlBase':
                urlplace=i
            if title=='ReqDuration':
                durplace=i
            i+=1
        #add data to dict
        insertToDict(dict,data,hostplace,urlplace,durplace)        


# In[11]:

#create a dictionary from files in the form of: (Host->URL->MinDuration) 
dict = {}
allfiles=list()
allfiles.append("DataForBar/requests1.csv")
allfiles.append("DataForBar/requests2.csv")
allfiles.append("DataForBar/requests3.csv")
createDictFromAllFiles (dict,allfiles)


# In[12]:

#save dictionary to File
with open("hostURLDurBar.csv",'w') as f2:
    f2.write("Host,URL,MinDuration\n")
    for host in dict:
        hostdict=dict[host]
        for url in hostdict:
            dur=hostdict[url]
            f2.write("%s,%s,%f\n" % (host, url, dur))
    f2.close()

