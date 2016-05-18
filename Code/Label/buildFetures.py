from Code.Label import scale_features

featuresOfInterest = ['BrowserVer', 'OsVer', 'Continent', 'Country', 'OpName']

scale_features.buildFeaturesFiles("Data/Train/TrainLabeledData", "Data/Features", featuresOfInterest)