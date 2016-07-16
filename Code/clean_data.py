
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
    timeofday=-1
    for filename in os.listdir(dirpath):
        addTimeOfDay=False
        filepath=dirpath+"/"+filename
        with open(filepath) as f:
            data = list(csv.reader(f))
            f.close
        data=cleanData(data)
        data.reverse
        with open(filepath,'w') as f:
            headline=data[0]
            if 'TimeOfDay' not in headline:
                addTimeOfDay=True
                coindex=-1
                for i in range (0,len(headline)):
                    if headline[i]=="TimeStamp":
                        coindex=i
                if coindex<0:
                    print ("indexs not found in request file in cleanData")
            for i in range (0,len(data)):
                row=data[i]
                if addTimeOfDay:
                    timeofday=row[coindex]
                    if timeofday!='TimeStamp':
                        timeofday=timeofday.split(' ')[1]
                        timeofday=timeofday.split(':')[0]+':'+timeofday.split(':')[1]
                for j in range(0,len(row)):
                    if j<len(row)-1:
                        f.write('%s,' % row[j])
                    else:
                        f.write('%s' % row[j])
                if i==0:
                    if addTimeOfDay:
                        f.write(',TimeOfDay')
                else:
                    if addTimeOfDay:
                        f.write(',%s' % timeofday)
                f.write('\n')
            f.close()





