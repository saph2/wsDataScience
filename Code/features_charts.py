# coding: utf-8

import os
import csv
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

#read all "Features" to charts
def showAll(featuresDirPath,resultDirPath):
    fig,((ax1,ax2,a3),(ax4,ax5,a6)) = plt.subplots(sharex=False,sharey=False,nrows=2,ncols=3)
    axAll=((ax1,ax2,a3),(ax4,ax5,a6))
    i=0
    ptAll=axAll[0]
    for filename in os.listdir(featuresDirPath):
        if "empty" not in filename and "features" in filename:
            filepath=featuresDirPath+"/"+filename
            filename=filename.split("_")[0]
            with open(filepath) as f:
                if i==3:
                    ptAll=axAll[1]
                    i=0
                ax=ptAll[i]
                data = list(csv.reader(f))
                create_charts(filename.replace(".csv",''),data,ax,45)
                f.close
            i+=1
    plt.savefig(resultDirPath+"/busyChart_All")
   # plt.show()



def showEach(featuresDirPath,resultDirPath):
    for filename in os.listdir(featuresDirPath):
        if "empty" not in filename and "features" in filename:
            filepath=featuresDirPath+"/"+filename
            filename=filename.split("_")[0]
            with open(filepath) as f:
                fig,ax = plt.subplots()
                data = list(csv.reader(f))
                create_charts(filename.replace(".csv",''),data,ax,-25)
                plt.savefig(resultDirPath+"/busyChart_{0}".format(filename))
                f.close
   # plt.show()




def create_charts(featureName,data,ax,rdegree):

    data=np.array(data)
    data=data[1:data.size-1] # cut headline
    headline=[row[0] for row in data]
    if "OpName" in featureName:
        headline=[item[0:25] for item in headline]
    X = range(len(headline))
    Y=[float(row[2]) for row in data]

    width = 1/len(data)
    ax.bar(X,Y,width)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Busy')
    ax.set_title('Busy probability for feature:{0}'.format(featureName))
    ax.set_xticklabels(headline,rotation=rdegree,size=12)



def featuresToCharts(featuresDirPath,resultDirPath):
    showAll(featuresDirPath,resultDirPath)
    showEach(featuresDirPath,resultDirPath)