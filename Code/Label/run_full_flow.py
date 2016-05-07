
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
# handel_files.move_data_to_one_folder("DataSplitToDailyFolder", "RawData")
# print "finished move_data_to_one_folder"


# split raw data to train and validation
handel_files.split_files_to_test_and_train_dir("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
print "finished split_files_to_test_and_train_dir"
#
#
# # In[12]:
#
# # build the dictionary which contains for each "host name"+"url" the min duration
#
build_duration_bar.buildBar("Train/TrainRawData", "MinDurationBar")
print "finished buildBar"
#
#
# # In[ ]:
#
# # clean the data from 'comma'
#
clean_data.cleanFilesInDir("Train/TrainRawData")
clean_data.cleanFilesInDir("Validation/ValidationRawData")
print "finished cleanFilesInDir"
#
#
# # In[13]:
#
# # label the data
#
label_data.labelAllfiles("Train/TrainRawData", "Train/TrainLabeledData", "MinDurationBar")
label_data.labelAllfiles("Validation/ValidationRawData", "Validation/ValidationLabeledData", "MinDurationBar")
print "finished labelAllfiles"
#
#
# #  In[10]:
#
# # scaleFeatures: create the files of features ordered by workloads and numbered in folder Data/Features"
#
scale_features.buildFeaturesFiles("Train/TrainLabeledData", "Features")
print "finished buildFeaturesFiles"
#
#  # In[3]:
#
#  # vectorizes the data
#
vectorize_data.dataToVectors("Features", "Train/TrainLabeledData", "Train/TrainVectors", True)
vectorize_data.dataToVectors("Features", "Validation/ValidationLabeledData", "Validation/ValidationVectors", True)
print "finished dataToVectors"


#  In[6]:

#  build svm model and run cross val on our labeled vectors

print "starting build_train_model"
execute_svm_prediction.build_train_model("Train/TrainVectors")
print "finished build_train_model"


#  In[7]:
#  build classifier and execute prediction

print "starting predict_validation_set"
execute_svm_prediction.predict_validation_set("Validation/ValidationVectors", "Train/TrainVectors")
print "finished predict_validation_set"

#  In[8]:
##  delete all files needed for next time

handel_files.delete_files_from_dir("Validation/ValidationVectors")
handel_files.delete_files_from_dir("Train/TrainVectors")
handel_files.delete_files_from_dir("Train/TrainLabeledData")
handel_files.delete_files_from_dir("Validation/ValidationLabeledData")
handel_files.delete_files_from_dir("MinDurationBar")
handel_files.delete_files_from_dir("Features")
print "finished delete_files_from_dir"


# # return data to rawData dir (when we want to start the procedure from the start)
handel_files.return_files_from_train_test_to_rawdata("RawData", "Train/TrainRawData", "Validation/ValidationRawData")
print "finished remove_files_to_rawdata"
#
