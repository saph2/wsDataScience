
# coding: utf-8

# In[11]:

import build_duration_bar
import clean_data
import execute_svm_prediction
import handel_files
import label_data
import scale_features
import vectorize_data

# move all request files from daily folders to one folder.
# file name is according to the date
handel_files.move_data_to_one_folder("Data/DataSplitToDailyFolder", "Data/RawData")
print "finished move_data_to_one_folder"


# split raw data to train and validation
handel_files.split_files_to_test_and_train_dir("Data/RawData", "Data/Train/TrainRawData", "Data/Validation/ValidationRawData")
print "finished split_files_to_test_and_train_dir"
#
#
# # In[12]:
#
# # build the dictionary which contains for each "host name"+"url" the min duration
#
build_duration_bar.buildBar("Data/Train/TrainRawData", "Data/MinDurationBar")
print "finished buildBar"
#
#
# # In[ ]:
#
# # clean the data from 'comma'
#
clean_data.cleanFilesInDir("Data/Train/TrainRawData")
clean_data.cleanFilesInDir("Data/Validation/ValidationRawData")
print "finished cleanFilesInDir"
#
#
# # In[13]:
#
# # label the data
#
label_data.labelAllfiles("Data/Train/TrainRawData", "Data/Train/TrainLabeledData", "Data/MinDurationBar")
label_data.labelAllfiles("Data/Validation/ValidationRawData", "Data/Validation/ValidationLabeledData", "Data/MinDurationBar")
print "finished labelAllfiles"
#
#
# #  In[10]:
#
# # scaleFeatures: create the files of features ordered by workloads and numbered in folder Data/Features"
#
scale_features.buildFeaturesFiles("Data/Train/TrainLabeledData", "Data/Features")
print "finished buildFeaturesFiles"
#
#  # In[3]:
#
#  # vectorizes the data
#
vectorize_data.dataToVectors("Data/Features", "Data/Train/TrainLabeledData", "Data/Train/TrainVectors", True)
vectorize_data.dataToVectors("Data/Features", "Data/Validation/ValidationLabeledData", "Data/Validation/ValidationVectors", True)
print "finished dataToVectors"


#  In[6]:

#  build svm model and run cross val on our labeled vectors

print "starting build_train_model"
execute_svm_prediction.build_train_model("Data/Train/TrainVectors")
print "finished build_train_model"


#  In[7]:
#  build classifier and execute prediction

print "starting predict_validation_set"
execute_svm_prediction.predict_validation_set("Data/Validation/ValidationVectors", "Data/Train/TrainVectors")
print "finished predict_validation_set"

#  In[8]:
##  delete all files needed for next time

handel_files.delete_files_from_dir("Data/Validation/ValidationVectors")
handel_files.delete_files_from_dir("Data/Train/TrainVectors")
handel_files.delete_files_from_dir("Data/Train/TrainLabeledData")
handel_files.delete_files_from_dir("Data/Validation/ValidationLabeledData")
handel_files.delete_files_from_dir("Data/MinDurationBar")
handel_files.delete_files_from_dir("Data/Features")
print "finished delete_files_from_dir"


# # return data to rawData dir (when we want to start the procedure from the start)
handel_files.return_files_from_train_test_to_rawdata("Data/RawData", "Data/Train/TrainRawData", "Data/Validation/ValidationRawData")
print "finished remove_files_to_rawdata"
#
