# coding: utf-8

# Handle the files we're using in the model construction (creating dir, moving, deleting...)


import os
import random
import shutil

# create all directories
def create_directories(header):
    dir="../Data"
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir="../Model"
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir="../DailyData"
    if not os.path.exists(dir):
        os.makedirs(dir)
    directories=["Classify","Train","Test","DurationBar","RawData","Results","Selection","Features",
                 "Classify/LinearRegression","Classify/SVM","Classify/NaiveBayes",
                 "Results/Classifier","Results/Features",
                 "Selection/ClassifierSelection","Selection/FeatureSelection",
                 "Selection/FeatureSelection/TrainNewVectors","Selection/FeatureSelection/TestNewVectors",
                 "Train/TrainRawData","Train/TrainLabeledData","Train/TrainVectors",
                 "Test/TestRawData","Test/TestLabeledData","Test/TestVectors"]
    for dir in directories:
        if not os.path.exists(header+dir):
            os.makedirs(header+dir)

    print("finish creating all the directories\n")

# move all files from daily folders to one folder,
# each files name according to the folder (day) he came from
def move_data_to_one_folder(dataFolder, rawdatafolder):

    for foldername in os.listdir(dataFolder):
        try:
            filePath = dataFolder + "/" + foldername + "/requests.csv"
            destPath = rawdatafolder + "/" + foldername + ".csv"
            shutil.copy(filePath, destPath)
        except:
            pass

# move random 80% of the data files to "Data/Train/TrainData" directory.
# the rest 20% to the "Data/Test/TestData" directory.
def split_files_to_test_and_train_dir(rawdataDirPath, trainDirPath, testDirPath):
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
                destPath = testDirPath + "/" + filename
                shutil.move(filePath, destPath)


# remove files from test and train directories to rawData.
def return_files_from_train_test_to_rawdata(rawdataDirPath, testDirPath, trainDirPath):
    for filename in os.listdir(testDirPath):
        if "empty" not in filename:
            filePath = testDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)

    for filename in os.listdir(trainDirPath):
        if "empty" not in filename:
            filePath = trainDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)

# delete file from directory
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

    delete_files_from_dir(header+"Test/TestLabeledData")
    delete_files_from_dir(header+"Test/TestRawData")
    delete_files_from_dir(header+"Test/TestVectors")

    delete_files_from_dir(header+"DurationBar")
    delete_files_from_dir(header+"Features")

    delete_files_from_dir(header+"Selection/FeatureSelection/TrainNewVectors")
    delete_files_from_dir(header+"Selection/FeatureSelection/TestNewVectors")


# save the classifiers to the "Model" directory
def save_to_model_dir(destDir,fileName):
    try:
        shutil.copy(fileName, destDir)
    except:
        pass

