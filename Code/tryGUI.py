#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
import matplotlib.pyplot as plt;
from sklearn.externals import joblib

plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ----- requests and durations --------
requests = ["req1", "req2", "req3", "req4"]
currDurations = []#4, 2, 4, 4,    2, 4, 4, 4,     4, 2]
allDurations = []

# ------------- constants -------------

# classifier consts
pathToClassifier = '../Data/Classify/'
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

#other consts
FONT_DEFAULT = 'Helvetica'
FONT_BUTTON = 'Helvetica 12 bold'
FONT_STATS = 'Helvetica 12 bold'
APP_TITLE = 'workload prediction app'.upper()
MAX_NUM_OF_BARS = 10

# text fields
TEXT_BUTTON = u"Evaluate request"
TEXT_ENTRY_DEFAULT = u"Enter request here..."
TEXT_TOP_LABEL_DEFAULT = 'waiting for a request...'
TEXT_RED_REQ = 'BUSY!! :-('
TEXT_ORANGE_REQ = 'MEDIUM LOAD :-|'
TEXT_GREEN_REQ = 'ALL GOOD :-)'
TEXT_LEFT_STATS_DEFAULT = 'avg of all requests will be here'
TEXT_RIGHT_STATS_DEFAULT = 'avg of last ' + str(MAX_NUM_OF_BARS) + ' requests will be here'
TEXT_LAST10_REQS = 'last 10 avg is '
TEXT_ALL_REQS = 'all avg is '

# canvas sizes

# highest y = max_data_value * y_stretch
y_stretch = 60
# gap between lower canvas edge and x axis
y_gap = 100
# distance between bars
x_stretch = 40
# width of a bar
x_width = 40
CANVAS_WIDTH = WINDOW_WIDTH
# gap between left canvas edge and y axis
x_gap = CANVAS_WIDTH / 2
# height of the stats bar
stats_height_gap = 30
CANVAS_HEIGHT = WINDOW_HEIGHT - y_gap - stats_height_gap
BAR_NAME_LOCATION = CANVAS_HEIGHT - 80

def calculateX_GAP():
    total_width_of_bars = len(currDurations) * x_width + (len(currDurations) - 1) * x_stretch
    return (CANVAS_WIDTH - total_width_of_bars) / 2

def OnButtonClick():
    OnPressEnter(None)

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

        # put the y value above each bar

        # if we want to print the name of the request at the top of the bar then the second argument should be y0
        # if not, use the constant
        canvas.create_text(x0 + 2, BAR_NAME_LOCATION, anchor=SW, text='req' + str(x + 1), font=FONT_DEFAULT, fill='white')


# TODO decide what to write above the bar. currently just 'req' + val
def updateTopLabel(val):
    if(val>4):
        bgColor, message, fontColor = BG_LABEL_RED, TEXT_RED_REQ, 'white'
        val = '\'' + str(val) + '\' '
    elif(val>2 and val <=4):
        bgColor, message, fontColor = BG_LABEL_ORANGE, TEXT_ORANGE_REQ, 'white'
        val = '\'' + str(val) + '\' '
    elif(val>=0 and val<=2):
        bgColor, message, fontColor = BG_LABEL_GREEN, TEXT_GREEN_REQ, COLOR_LABEL_DEFAULT
        val = '\'' + str(val) + '\' '
    else:# val < 0 means not a valid input
        bgColor, message, fontColor = BG_LABEL_DEFAULT, 'invalid. ' + TEXT_TOP_LABEL_DEFAULT, COLOR_LABEL_DEFAULT
        val = ''

    topLabel = Label(app, textvariable=labelText, anchor="center", bd=4, fg=fontColor, bg=bgColor, font=FONT_DEFAULT, relief=GROOVE)
    topLabel.grid(column=0, row=1, rowspan=2, columnspan=2, sticky='EW')
    labelText.set('request ' + val + 'is ' + message)

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


# TODO mising code
# this func checks a request that a user entered and if it's a legal request returns it's value, otherwise returns -1
# later should be changed to running the classifier
# vector is a list of numbers divided by a space(' ') of the form -0.49692562 -0.25001743 -0.4923626 -0.98941777 -1.19655191
def getPredictionForRequest(vector):
    prediction = 0
    # vector = -0.49692562 -0.25001743 -0.4923626 -0.98941777 -1.19655191

    # convert to float array
    vector = [float(x) for x in vector.split()]
    # make the array to be 2D array
    vector = np.array(vector).reshape((1, -1))
    # get prediction
    prediction = classifier.predict(vector)
    try:
        print prediction[0]
        prediction = int(prediction[0])
        if(prediction == 0):
            prediction = 2
        elif(prediction == 1):
            prediction = 4
        elif(prediction == 2):
            prediction = 6
        # prediction += 2
        # if prediction > 2:
        #     prediction += 2
        # print 'predicton = ' + str(prediction)
        # prediction = 4

    except:
        print 'could not predict this request'
    return prediction

# this func is executed whenever 'Enter' is pressed
def updateStatsLabel():
    last10Avg = TEXT_LAST10_REQS + str(float(sum(currDurations)) / max(len(currDurations), 1))
    allAvg = TEXT_ALL_REQS + str(float(sum(allDurations)) / max(len(allDurations), 1))
    statsLeftText.set(allAvg)
    statsRightText.set(last10Avg)

def OnPressEnter(self):
    try:
        val = entryVariable.get()
        requestPredictionVal = getPredictionForRequest(val)
        if(requestPredictionVal >= 0):
            # add request to list of all reqs
            allDurations.append(requestPredictionVal)

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



# initialize the window
app = Tk()
app.title(APP_TITLE)
app.configure(bg=BG_APP)
app.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
app.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)

# load classifier
classifier = joblib.load(pathToClassifier + getClassifierMiddle(classifierType) + classifierSuffix)

# add text entry field
entryVariable = StringVar()
entryField = Entry(master=app, textvariable=entryVariable, bd=4, relief=GROOVE, font=14)
entryField.grid(column=0, row=0, sticky='EW')
entryVariable.set(TEXT_ENTRY_DEFAULT)

# catch pressing 'Enter' event
entryField.bind("<Return>", OnPressEnter)

# add button
button = Button(master=app, text=TEXT_BUTTON, command=OnButtonClick, font=FONT_BUTTON, fg=COLOR_BUTTON_TEXT, bg=BG_BUTTON_DEFAULT, bd=8)
button.grid(column=1, row=0)

# add text label
labelText = StringVar()
labelBGColor = StringVar()
labelBGColor.set(BG_LABEL_DEFAULT)
topLabel = Label(app, textvariable=labelText, anchor="center", bd=4, fg=COLOR_LABEL_DEFAULT,
                 bg=BG_LABEL_DEFAULT, font=FONT_DEFAULT, relief=GROOVE)
topLabel.grid(column=0, row=1, rowspan=2, columnspan=2, sticky='EW')

# TODO change this to something more meaningful
labelText.set(TEXT_TOP_LABEL_DEFAULT)


# ---------------- canvas ----------------------

# add canvas that will hold the bar chart
canvas = Canvas(app, bg=BG_CANVAS, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.grid(column=0, columnspan=2, sticky='NSEW')

drawBar()
# ------------ end canvas -----------

# ------------ bottom statistics -----------

statsText = StringVar()
statsLabel = Label(app, anchor="center", bd=4, fg='red')
statsLabel.grid(column=0, columnspan=2, sticky='NSEW')
statsText.set("")

# width of app in pixels
# pixels ='123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,123456789,'
widthOfStatsCellInCharactars = 34

# avg of all reqs label
statsLeftText = StringVar()
statsLeft = Label(statsLabel, textvariable=statsLeftText, font=FONT_STATS, anchor="center", bd=4, fg=COLOR_STATS_TEXT, width=widthOfStatsCellInCharactars)
statsLeft.grid(column=0,row=0, sticky='W')
statsLeftText.set(TEXT_LEFT_STATS_DEFAULT)

# avg of last 10 reqs label
statsRightText = StringVar()
statsRight = Label(statsLabel, textvariable=statsRightText, font=FONT_STATS, anchor='center', bd=4, fg=COLOR_STATS_TEXT, width=widthOfStatsCellInCharactars)
statsRight.grid(column=1, row=0)
statsRightText.set(TEXT_RIGHT_STATS_DEFAULT)

# ----------- end statistics ----------------

# allow resizing of the window when long text is entered in the entry field
app.grid_columnconfigure(0,weight=1)
# allow only horizontal resizing (and not vertical)
app.resizable(True,False)

# prevent constant resizing of the window
app.update()
app.geometry(app.geometry())

# auto select the text field
entryField.focus_set()
entryField.selection_range(0, END)


mainloop()



