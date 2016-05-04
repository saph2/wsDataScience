

# coding: utf-8

# In[ ]:

import csv
import os


# In[1]:

# remove comma from the tables
def cleanData(data):
    for row in data:
        for i in range (0,len(row)): #clean the data
            row[i]=row[i].replace(',', '-')
    return data


# In[3]:

# clean all files in the given dir
def cleanFilesInDir(dirpath):
    for filename in os.listdir(dirpath):
        filepath=dirpath+"/"+filename
        with open(filepath) as f:
            data = list(csv.reader(f))
            f.close
        data=cleanData(data)
        data.reverse
        with open(filepath,'w') as f:
            for row in data:
                for i in range (0,len(row)):
                    if (i<len(row)-1):
                        f.write('%s,' % row[i])
                    else:
                        f.write('%s' % row[i])    
                f.write('\n')
            f.close()


# In[ ]:



