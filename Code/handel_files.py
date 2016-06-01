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
    countFiles=0
    for filename in os.listdir(rawdataDirPath):
        if "empty" not in filename:
            countFiles+=1

    if countFiles==0 or countFiles==1:
        print("Need 2 or more files in RawData dir\n")
        exit(0)
    else:
        trainSize=round(0.8*countFiles)
        if trainSize==countFiles:
            trainSize-=1

        count=0
        while count!=trainSize:
            for filename in os.listdir(rawdataDirPath):
                prob = random.random()
                if prob < 0.8 and "empty" not in filename:
                    filePath = rawdataDirPath + "/" + filename
                    destPath = trainDirPath + "/" + filename
                    shutil.move(filePath, destPath)
                    count+=1
                if trainSize==count:
                    break

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
def remove_all_files_from_all_folders(header):

    delete_files_from_dir(header+"Train/TrainLabeledData")
    delete_files_from_dir(header+"Train/TrainRawData")
    delete_files_from_dir(header+"Train/TrainVectors")

    delete_files_from_dir(header+"Validation/ValidationLabeledData")
    delete_files_from_dir(header+"Validation/ValidationRawData")
    delete_files_from_dir(header+"Validation/ValidationVectors")

    delete_files_from_dir(header+"Features")

    delete_files_from_dir(header+"Selection/FeatureSelection/TrainNewVectors")
    delete_files_from_dir(header+"Selection/FeatureSelection/ValidationNewVectors")