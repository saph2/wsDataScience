
# coding: utf-8

# In[127]:

import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn import datasets
import random,math
import os
import csv


# In[128]:

# read vectors
def readVectors(vecDirPath):
    filtered_data=list()
    for filename in os.listdir(vecDirPath):
        if "vectors" in filename:
            filepath=vecDirPath+"/"+filename
            data = np.array(np.genfromtxt(filepath, delimiter=',',autostrip=True))
            filtered_data.append(data)
    filtered_data=np.asarray(filtered_data)[0]
    return filtered_data


# In[129]:

def scaleAndFilterVectors (filtered_data):
    # cut headline
    sz=filtered_data.size
    headline=filtered_data[0]
    filtered_data=filtered_data[1:sz]
    
    # save labels
    labels=filtered_data[:,5]
    for i in range (0,len(labels)):
        labels[i]=int(labels[i])
        
    #cut labels
    scaled_filtered_data=preprocessing.scale(filtered_data)
    scaled_filtered_data=scaled_filtered_data[:,:-1]
    
    return (scaled_filtered_data,labels)


# In[130]:

def crossValModel(scaled_filtered_data,labels):
   # diviede to train and test
   training_size_fraction=.09

   # train and test indexes
   test_idx=np.array(random.sample(xrange(len(labels)), int((1-training_size_fraction)*len(labels))))
   train_idx=np.array([x for x in xrange(len(labels)) if x not in test_idx])

   # build train and test samples
   test_samples=scaled_filtered_data[test_idx]
   train_samples=scaled_filtered_data[train_idx]

   # keep train and test labels
   test_out=labels[test_idx]
   train_out=labels[train_idx]
   
   # build classifier
   clf = svm.SVC(kernel='linear')
   clf.fit(train_samples, train_out)
   
   # predict
   a=np.array(clf.predict(test_samples).astype(int))
   c=a==np.array(test_out)
   c=np.array(a)==np.array(test_out)
   
   # print results
   print "Accuracy                                    : ",str(sum(c)*100.0/len(a))+" %"
   print "Number of support vectors for positive class: ",clf.n_support_[0]
   print "Number of support vectors for negative class: ",clf.n_support_[1]


# In[131]:

# vecDirPath="Data/TrainVectors"
def buildTrainModel (vecDirPath):
    
    #read the vectors from all data files
    dataVectors=readVectors(vecDirPath)
    
    #retrun vectors in range [0,1] and labels
    (vectors,labels)=scaleAndFilterVectors(dataVectors)
    
    #cross val the train set
    crossValModel(vectors,labels)


# In[ ]:



