
# coding: utf-8

# In[11]:

import buildDurationBar
import labelData
import scaleFeatures
import vectorizeData
import trainSvmModel
import cleanData


# In[12]:

#build the bar from folder: "Data/DataForBar"

buildDurationBar
buildDurationBar.buildBar("Data/DataForBar")


# In[ ]:

#clean the data from 'comma'

#dirpath="Data/DataToLabel"

cleanData
cleanData.cleanFilesInDir("Data/DataToLabel")


# In[13]:

#label the data in folder: "Data/DataToLabel" and save to "Data/LabeledData"

#dataDir="Data/DataToLabel"
#labelDir="Data/LabeledData"
#barDir="Data/DataForBar"

labelData
labelData.labelAllfiles("Data/DataToLabel","Data/LabeledData","Data/DataForBar")


# In[10]:

#scaleFeatures: create the files of features ordered by workloads and numbered in folder Data/Features"

#dataDirPath="Data/LabeledData"
#featuresDirPath="Data/Features"

scaleFeatures
scaleFeatures.buildFeaturesFiles("Data/LabeledData","Data/Features")


# In[3]:

# vectorizes the data in "Data/LabeledData" and save to "Data/TrainVectors"
# if data in "Data/testData" save to "Data/TestVectors"

#featuresDirPath="Data/Features"
#dataDirPath="Data/LabeledData"

vectorizeData
vectorizeData.dataToVectors("Data/Features","Data/LabeledData", "Data/TrainVectors",True)
vectorizeData.dataToVectors("Data/Features","Data/TestData", "Data/TestVectors",False)


# In[6]:

# build svm model and run cross val on our labeled vectors

#vecDirPath="Data/TrainVectors"

trainSvmModel
trainSvmModel.buildTrainModel ("Data/TrainVectors")


# In[ ]:



