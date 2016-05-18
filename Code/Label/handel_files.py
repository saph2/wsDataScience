# coding: utf-8

import os
import random
import shutil

# move all files from daily folders to one folder,
# each files name according to the folder (day) he came from
def move_data_to_one_folder(dataFolder, rawdatafolder):

    # this should be the path to all the unzipped data.
    # don't change it, just comment this line and add your own.
    # dataFolder = "C:\Users\Dell\Desktop\Data Set\UnZipped"
    # dataFolder = dataFolder.replace("\\","/")

    for foldername in os.listdir(dataFolder):
        try:
            filePath = dataFolder + "/" + foldername + "/requests.csv"
            destPath = rawdatafolder + "/" + foldername + ".csv"
            shutil.move(filePath, destPath)
        except:
            print "requests file not exist in folder: " + foldername

# move random 90% of the data files to TrainData directory.
# the rest to TestData.
# this way they won't have an affect on feature selection.
def split_files_to_test_and_train_dir(rawdataDirPath, trainDirPath, validationDirPath):
    for filename in os.listdir(rawdataDirPath):
        prob = random.random()
        if prob < 0.8 and "empty" not in filename:
            filePath = rawdataDirPath + "/" + filename
            destPath = trainDirPath + "/" + filename
            shutil.move(filePath, destPath)

    for filename in os.listdir(rawdataDirPath):
        if "empty" not in filename:
            filePath = rawdataDirPath + "/" + filename
            destPath = validationDirPath + "/" + filename
            shutil.move(filePath, destPath)


# remove files from validation and train directories to rawData.
def return_files_from_train_test_to_rawdata(rawdataDirPath, validationDirPath, trainDirPath):
    for filename in os.listdir(validationDirPath):
        if "empty" not in filename:
            filePath = validationDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)

    for filename in os.listdir(trainDirPath):
        if "empty" not in filename:
            filePath = trainDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)


def delete_files_from_dir(dirPath):
    for filename in os.listdir(dirPath):
        if "empty" not in filename:
            filePath = dirPath + "/" + filename
            os.remove(filePath)


# removes all files that were added during the run
def remove_all_files_from_all_folders():

    delete_files_from_dir("Features")
    # delete_files_from_dir("LabeledData")
    delete_files_from_dir("MinDurationBar")
    # delete_files_from_dir("TrainVectors")

    delete_files_from_dir("Train/TrainLabeledData")
    delete_files_from_dir("Train/TrainRawData")
    delete_files_from_dir("Train/TrainVectors")

    delete_files_from_dir("Validation/ValidationLabeledData")
    delete_files_from_dir("Validation/ValidationRawData")
    delete_files_from_dir("Validation/ValidationVectors")