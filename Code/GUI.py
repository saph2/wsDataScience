#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import csv
import random
from Tkinter import *
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import json
from tkFileDialog import askopenfilename
from tkFileDialog import askopenfile
plt.rcdefaults()
import numpy as np


# ----- requests and durations --------
currDurations = []
allDurations = []


# ------------- constants -------------

# classifier consts
modelDir = '../Model/'
classifierSuffix = '_model.pkl'
classifierType = 'svm'


# background colors
BG_APP = 'dim gray'
BG_LABEL_DEFAULT = 'snow2'
BG_LABEL_RED = 'red2'
BG_LABEL_GREEN = 'green'
BG_LABEL_ORANGE = 'orange'
BG_CANVAS = 'black'
BG_BUTTON_DEFAULT = 'brown3'



# text colors
COLOR_LABEL_DEFAULT = 'brown'
COLOR_BUTTON_TEXT = 'white'
COLOR_STATS_TEXT = 'black'

# window size
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
STAT_HEIGHT = 50

# other consts
FONT_DEFAULT = 'Helvetica'
FONT_BUTTON = 'Helvetica 12 bold'
FONT_STATS = 'Helvetica 12 bold'
APP_TITLE = 'workload prediction app'.upper()
MAX_NUM_OF_BARS = 10
FLOAT_PERCISION = 4

# text fields
TEXT_BUTTON = u"Evaluate text request"
TEXT_BUTTON_FILE = u"Evaluate requests file"
TEXT_ENTRY_DEFAULT = u"Enter request here..."
TEXT_TOP_LABEL_DEFAULT = 'Waiting for a request...'
TEXT_RED_REQ = 'Will cause a High workload'
TEXT_ORANGE_REQ = 'Will cause a Moderate workload'
TEXT_GREEN_REQ = 'Will NOT cause an overload'
TEXT_LEFT_STATS_DEFAULT = 'Avg of all requests will be here'
TEXT_RIGHT_STATS_DEFAULT = 'Avg of last ' + str(MAX_NUM_OF_BARS) + ' requests will be here'
TEXT_LAST10_REQS = 'Avg of last 10 requests : '
TEXT_ALL_REQS = 'Avg of all requests is '


# canvas sizes

# highest y = max_data_value * y_stretch
y_stretch = 40
# gap between lower canvas edge and x axis
y_gap = 130
# distance between bars
x_stretch = 40
# width of a bar
x_width = 40
CANVAS_WIDTH = WINDOW_WIDTH
# gap between left canvas edge and y axis
x_gap = CANVAS_WIDTH / 2
# height of the stats bar
stats_height_gap = 75
CANVAS_HEIGHT = WINDOW_HEIGHT - y_gap - stats_height_gap
# location of the reqs names
BAR_NAME_LOCATION = CANVAS_HEIGHT - 70

FILE=None

def calculateX_GAP():
    total_width_of_bars = len(currDurations) * x_width + (len(currDurations) - 1) * x_stretch
    return (CANVAS_WIDTH - total_width_of_bars) / 2


def drawBar():
    for x, y in enumerate(currDurations):
        # x is the location of the bar along the x-axis
        # y is the height of the bar at location x
        x_gap = calculateX_GAP()
        # calculate rectangle coordinates (integers) for each bar
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = CANVAS_HEIGHT - (y * y_stretch + y_gap)
        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = CANVAS_HEIGHT - y_gap

        # draw the bar
        if (y > 4):
            canvas.create_rectangle(x0, y0, x1, y1, fill=BG_LABEL_RED)
        elif (y > 2):
            canvas.create_rectangle(x0, y0, x1, y1, fill=BG_LABEL_ORANGE)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill=BG_LABEL_GREEN)

        # the text to be displayed above/beneath each bar
        textStr = 'req\n' + str(1 + x + max(len(allDurations) - 10, 0))

        # put the y value above each bar.
        # if we want to print the name of the request at the top of the bar then the second argument should be y0
        # if not, use the constant
        canvas.create_text(x0 + 2, BAR_NAME_LOCATION, anchor=SW, text=textStr, font=FONT_DEFAULT, fill='white')


def updateTopLabel(val):
    reqName = str(len(allDurations)) + ' '
    if(val>4):
        bgColor, message, fontColor = BG_LABEL_RED, TEXT_RED_REQ, 'white'
    elif(val>2 and val <=4):
        bgColor, message, fontColor = BG_LABEL_ORANGE, TEXT_ORANGE_REQ, 'white'
    elif(val>=0 and val<=2):
        bgColor, message, fontColor = BG_LABEL_GREEN, TEXT_GREEN_REQ, COLOR_LABEL_DEFAULT
    else:# val < 0 means not a valid input
        bgColor, message, fontColor = BG_LABEL_DEFAULT, 'invalid. ' + TEXT_TOP_LABEL_DEFAULT, COLOR_LABEL_DEFAULT
        reqName = ''

    topLabel = Label(app, textvariable=labelText, anchor="center", bd=4, fg=fontColor, bg=bgColor, font=FONT_DEFAULT, relief=GROOVE)
    topLabel.grid(column=0, row=3, rowspan=2, columnspan=2, sticky='EW')
    labelText.set('Request ' + reqName + 'is ' + message)


# get the current middle part of the path to the classifier
# type = svm/nb/lr
def getClassifierMiddle(type):
    classifierMiddle = ''
    if(type.lower() == 'svm'):
        classifierMiddle = 'SVM/svm'
    elif type.lower() == 'nb':
        classifierMiddle = 'NaiveBayes/naive_bayes'
    elif type.lower() == 'lr':
        classifierMiddle = 'LinearRegression/linearRegression'
    return classifierMiddle


# selectedFeatures = feature_selection.selectedFeatures
# allFeatures = feature_selection.allFeatures

#selectedFeatures=['BrowserVer','OsVer','Continent','OpName','Host']
selectedFeatures=['TimeOfDay','BrowserVer','OsVer','Continent','OpName','Host']

#allFeatures = ['TimeStamp','Browser','BrowserVer','Os','OsVer','RoleInst','Continent','Country','Province','City','OpName','Opid','Pid','Sid','IsFirst','Aid','Name','Success','Response','UrlBase','Host','ReqDuration']
allFeatures = ['TimeStamp','Browser','BrowserVer','Os','OsVer','RoleInst','Continent','Country','Province','City','OpName','Opid','Pid','Sid','IsFirst','Aid','Name','Success','Response','UrlBase','Host','ReqDuration','TimeOfDay']

# 2015-10-01 06:56:20.746844800,Internet Explorer,Internet Explorer 9.0,Windows,Windows 7,InsightsPortal_IN_2,North America,United States,Washington,Redmond,GET insightsextension/Index,10376790725597904948,,bd1c032c-c539-4c06-84ec-a321403c5645,False,emea-au-syd-edge,GET insightsextension/Index,True,200,/insightsextension,stamp2.app.insightsportal.visualstudio.com,4.6762
def getSelectedFeatures(vector):
    vector = vector.split(',')

    for featureName in mapOfSelectedFeatures.keys():

        # index in the original vector (e.g '4' for OsVer)
        index = mapOfSelectedFeatures[featureName]

        # the value in the vector in index 'index' (e.g OsVer = 'mac is x 10.6')
        currValInVector = (vector[index]).lower()

        try:
            # new value from json dict (from all_features.json)
            valFromJsonData = data[featureName][currValInVector]
        except:
            # value not in dict. probably have not encountered this value during training
            valFromJsonData = '0'
        vector[index] = valFromJsonData

    res = []
    for i in range(0, len(selectedFeatures)):
        res.append(vector[mapOfSelectedFeatures[selectedFeatures[i]]])

    return res

def predictRequestLine(val):
    try:
        requestPredictionVal = getPredictionForRequest(val)
        if(requestPredictionVal >= 0):
            # add request to list of all reqs
            allDurations.append(normalizePredictionVal(requestPredictionVal))

            # remove the first element and add this one to the list of the last 10 reqs
            currDurations.append(requestPredictionVal)
            if(len(currDurations) > MAX_NUM_OF_BARS):
                currDurations.pop(0)

            labelText.set("")

            # auto select the text field
            entryField.focus_set()
            entryField.selection_range(0, END)

            # redraw canvas
            canvas.delete('all')
            drawBar()

            updateTopLabel(requestPredictionVal)
            updateStatsLabel()
        else:
            print 'the prediction value(%d) is negative' % requestPredictionVal
    except:
        labelText.set('\'' + val + '\'' + " is not a valid request. please try again")

        # auto select the text field
        entryField.focus_set()
        entryField.selection_range(0, END)
        updateTopLabel(-1)

# load all data from 'all_features.json' to 'data'
def loadJsonWithAllFeatures():
    with open(modelDir+'all_features.json', 'r') as f:
        data = json.load(f)
    return data


# this func checks a request that a user entered and if it's a legal request returns it's value, otherwise returns -1
# later should be changed to running the classifier
# vector is a list of numbers divided by a space(' ') of the form -0.49692562 -0.25001743 -0.4923626 -0.98941777 -1.19655191
def getPredictionForRequest(vectorFromUser):

    # get only relevant subVector of features from the vector, converted to the values from the json dict
    subVectorWithConvertedData = getSelectedFeatures(vectorFromUser)

    # convert to float array
    floatVector = [float(x) for x in subVectorWithConvertedData]

    # make the array to be 2D array
    floatVector2D = np.array(floatVector).reshape((1, -1))

    # get prediction
    prediction = classifier.predict(floatVector2D)
    try:
        # print prediction[0]
        prediction = int(prediction[0])
        # TODO remove this line
        # prediction = random.randint(0,2)
        if(prediction == 0):
            prediction = 2
        elif(prediction == 1):
            prediction = 4
        elif(prediction == 2):
            prediction = 6
    except:
        print 'could not predict this request'
    finally:
        return prediction if prediction > 0 else 0

# this func is executed whenever 'Enter' is pressed
def updateStatsLabel():
    last10AvgFloat = round(float(sum([normalizePredictionVal(x) for x in currDurations])) / max(len(currDurations), 1), FLOAT_PERCISION)
    last10Avg = TEXT_LAST10_REQS + str(last10AvgFloat)

    allAvgFloat = round(float(sum(allDurations)) / max(len(allDurations), 1), FLOAT_PERCISION)
    allAvg = TEXT_ALL_REQS + str(allAvgFloat)

    statsLeftText.set(allAvg)
    statsRightText.set(last10Avg)


def normalizePredictionVal(bigPrediction):
    smallPrediction = 0

    if bigPrediction == 4:
        smallPrediction = 1

    elif bigPrediction == 6:
        smallPrediction = 2

    return smallPrediction

def OnPressEnterFile(Self):
    global FILE
    try:
        newLine=FILE.readline()
        predictRequestLine(newLine)
    except:
        labelText.set("not a valid request file or EOF. please try another file")

def OnButtonClickLine():
    global FILE
    OnPressEnterFile(None)

def OnButtonClickFile():
    global FILE
    global buttonLine
    if FILE!=None:
        FILE.close()
    FILE=askopenfile()
    FILE.readline()
    buttonLine=Button(master=app, width=17, text='Next request', command=OnButtonClickLine, font=FONT_BUTTON,
                fg=COLOR_BUTTON_TEXT, bg='purple', bd=8)
    buttonLine.grid(column=1, row=2)

def OnPressEnter(self):
    # runReqsFromFile()
    predictRequestLine(entryVariable.get())

def OnButtonClick():
    OnPressEnter(None)

# map features to their indices in the request vector
def getMapOfSelectedFeatures():

    # sort all selected features for later use
    selectedFeatures.sort()

    res = {}
    for feature in selectedFeatures:
        res[feature] = allFeatures.index(feature)
    return res


# convert array of strings to string with commas ( ['a','b','c'] --> 'a,b,c' )
def arrayToStrWithCommas(arr):
    res = arr[0]
    for i in range(1, len(arr)):
        res += ',' + arr[i]
    return res

# TODO remove this func
def runReqsFromFile():
    with open('requests.csv', 'r') as f:
        reqs = list(csv.reader(f))
    i = 0
    cnt=[0,0,0,0,0,0,0,0,0,0]
    for row in reqs:
        try:
            v = int(getPredictionForRequest(arrayToStrWithCommas(row)))
            cnt[v] += 1
            i += 1
        except:
            pass

    print cnt


# --------------------------------------------------------------
# ------------------- actual run starts here -------------------
# --------------------------------------------------------------


# get all the data from 'all_features.json'
data = loadJsonWithAllFeatures()

# get a mapping between features of interest and their indices in the vector
mapOfSelectedFeatures = getMapOfSelectedFeatures()

# initialize the window
app = Tk()
app.title(APP_TITLE)
app.configure(bg=BG_APP)
app.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
app.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)

# load classifier
##classifier = joblib.load(pathToClassifier + getClassifierMiddle(classifierType) + classifierSuffix)
classifier = joblib.load(modelDir+classifierType+classifierSuffix)

# add text entry field
entryVariable = StringVar()
entryField = Entry(master=app, textvariable=entryVariable, bd=4, relief=GROOVE, font=14)
entryField.grid(column=0, row=0, sticky='EW')
entryVariable.set(TEXT_ENTRY_DEFAULT)

# catch pressing 'Enter' event
entryField.bind("<Return>", OnPressEnter)

# add button
button = Button(master=app, width=17, text=TEXT_BUTTON, command=OnButtonClick, font=FONT_BUTTON,
                fg=COLOR_BUTTON_TEXT, bg=BG_BUTTON_DEFAULT, bd=8)
button.grid(column=1, row=0)

buttonFile = Button(master=app, width=17, text=TEXT_BUTTON_FILE,command=OnButtonClickFile, font=FONT_BUTTON,
                fg=COLOR_BUTTON_TEXT, bg='blue', bd=8)
buttonFile.grid(column=1, row=1)

buttonLine = Button(master=app, width=17, text='No file entered', font=FONT_BUTTON,
                fg=COLOR_BUTTON_TEXT, bg='gray', bd=8)
buttonLine.grid(column=1, row=2)

# add text label
labelText = StringVar()
labelBGColor = StringVar()
labelBGColor.set(BG_LABEL_DEFAULT)
topLabel = Label(app, textvariable=labelText, anchor="center", bd=4, fg=COLOR_LABEL_DEFAULT,
                 bg=BG_LABEL_DEFAULT, font=FONT_DEFAULT, relief=GROOVE)
topLabel.grid(column=0, row=3, rowspan=2, columnspan=2, sticky='EW')

labelText.set(TEXT_TOP_LABEL_DEFAULT)


# add canvas that will hold the bar chart
canvas = Canvas(app, bg=BG_CANVAS, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.grid(column=0, columnspan=3, sticky='NSEW')

# draw bar
drawBar()

# add bottom statistics
statsText = StringVar()
statsLabel = Label(app, anchor="center", bd=4, fg='red')
statsLabel.grid(column=0, columnspan=3, sticky='NSEW')
statsText.set("")

# width of app in pixels
# pixels ='123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,'
widthOfStatsCellInCharactars = 34

# add avg of all requests label
statsLeftText = StringVar()
statsLeft = Label(statsLabel, textvariable=statsLeftText, font=FONT_STATS, anchor="center", bd=4,
                  fg=COLOR_STATS_TEXT, width=widthOfStatsCellInCharactars)
statsLeft.grid(column=0,row=4, sticky='W')
statsLeftText.set(TEXT_LEFT_STATS_DEFAULT)

# add avg of last 10 requests label
statsRightText = StringVar()
statsRight = Label(statsLabel, textvariable=statsRightText, font=FONT_STATS, anchor='center', bd=4,
                   fg=COLOR_STATS_TEXT, width=widthOfStatsCellInCharactars)
statsRight.grid(column=1, row=4)
statsRightText.set(TEXT_RIGHT_STATS_DEFAULT)


# allow resizing of the window when long text is entered in the entry field
app.grid_columnconfigure(0, weight=1)
# allow only horizontal resizing (and not vertical)
app.resizable(True,False)

# prevent constant resizing of the window
app.update()
app.geometry(app.geometry())

# auto select the text field
entryField.focus_set()
entryField.selection_range(0, END)

# run in loop
mainloop()



