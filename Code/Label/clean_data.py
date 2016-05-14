
# coding: utf-8


import csv
import os



# remove comma from the tables
def cleanData(data):
    j=0
    for row in data:
        for i in range (0,len(row)): #clean the data
            row[i]=row[i].replace(',', '-')
            if j>0:
                row[i]=row[i].lower()
        j+=1
    return data



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





