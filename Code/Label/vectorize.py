from Code.Label import vectorize_data

featuresOfInterest = ['BrowserVer', 'OsVer', 'Continent', 'Country', 'OpName']

vectorize_data.dataToVectors("Data/Features", "Data/Train/TrainLabeledData", "Data/Train/TrainVectors", True, featuresOfInterest)
vectorize_data.dataToVectors("Data/Features", "Data/Validation/ValidationLabeledData", "Data/Validation/ValidationVectors", True, featuresOfInterest)