#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ----- requests and durations --------
requests = ["req1", "req2", "req3", "req4"]
durations = []#4, 2, 4, 4,    2, 4, 4, 4,     4, 2]


# ------------- constants -------------

# background colors
BG_APP = 'DarkOrchid4'
BG_LABEL_DEFAULT = 'plum1'
BG_LABEL_RED = 'red2'
BG_LABEL_GREEN = 'green'
BG_CANVAS = 'black'


# text colors
COLOR_BUTTON_DEFAULT = 'brown3'
COLOR_LABEL_DEFAULT = 'brown'

# window size
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
STAT_HEIGHT = 200

# text fields
TEXT_BUTTON = u"Evaluate request"
TEXT_ENTRY_DEFAULT = u"Enter request here..."
TEXT_TOP_LABEL_DEFAULT = 'waiting for a request...'
TEXT_RED_REQ = 'BUSY!! :('
TEXT_GREEN_REQ = 'ALL GOOD :)'


#other consts
TEXT_FONT = 'Helvetica'
APP_TITLE = 'workload prediction app'.upper()
MAX_NUM_OF_BARS = 10

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

CANVAS_HEIGHT = WINDOW_HEIGHT - y_gap - 200

BAR_NAME_LOCATION = CANVAS_HEIGHT - 80
# total_width_of_bars = len(durations)* bar_width + len(durations)-1)*dist_betweenBars
# (y_gap = canvas_width - total_width_of_bars) / 2

def calculateX_GAP():
    total_width_of_bars = len(durations) * x_width + (len(durations) - 1)*x_stretch
    return (CANVAS_WIDTH - total_width_of_bars) / 2

def OnButtonClick():
    OnPressEnter(None)

def drawBar():
    for x, y in enumerate(durations):
        # x is the location of the bar along the x-axis
        # y is the height of the bar at location x
        x_gap = calculateX_GAP()
        # calculate rectangle coordinates (integers) for each bar
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = CANVAS_HEIGHT - (y * y_stretch + y_gap)
        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = CANVAS_HEIGHT - y_gap

        # draw the bar
        if (y > 2):
            canvas.create_rectangle(x0, y0, x1, y1, fill=BG_LABEL_RED)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill=BG_LABEL_GREEN)

        # put the y value above each bar

        # if we want to print the name of the request at the top of the bar then the second argument should be y0
        # if not, use the constant
        canvas.create_text(x0 + 2, BAR_NAME_LOCATION, anchor=SW, text='req' + str(x + 1), font=TEXT_FONT, fill='white')

def updateTopLabel(val):
    if(val>2):
        bgColor, message, fontColor = BG_LABEL_RED, TEXT_RED_REQ, 'white'
    elif(val>0 and val<=2):
        bgColor, message, fontColor = BG_LABEL_GREEN, TEXT_GREEN_REQ, COLOR_LABEL_DEFAULT
    else:# val < 0 means not a valid input
        bgColor, message, fontColor = BG_LABEL_DEFAULT, 'invalid. ' + TEXT_TOP_LABEL_DEFAULT, COLOR_LABEL_DEFAULT

    topLabel = Label(app, textvariable=labelText, anchor="w", bd=4, fg=fontColor, bg=bgColor, font=TEXT_FONT, relief=GROOVE)
    topLabel.grid(column=0, row=1, rowspan=2, columnspan=2, sticky='EW')
    labelText.set('request \'' + str(val) + '\' is ' + message)

# TODO mising code
# this func checks a request that a user entered and if it's a legal request returns it's value, otherwise returns -1
# later should be changed to running the classifier
def validateRequest(val):
    v = -1
    try:
        v = int(val)
    except:
        print 'not an INT'
    return v

# this func is executed whenever 'Enter' is pressed
def OnPressEnter(self):
    val = entryVariable.get()
    ret = validateRequest(val)
    if(ret > 0):
        # remove the first element and ad this one
        durations.append(ret)
        if(len(durations) > MAX_NUM_OF_BARS):
            durations.pop(0)

        labelText.set("")

        # auto select the text field
        entryField.focus_set()
        entryField.selection_range(0, END)

        # redraw canvas
        canvas.delete('all')
        drawBar()

        updateTopLabel(ret)
    else:
        labelText.set('\'' + val + '\'' + " is not a valid request. please try again")

        # auto select the text field
        entryField.focus_set()
        entryField.selection_range(0, END)
        updateTopLabel(-1)

    # canvas = Canvas(app, bg=BG_CANVAS, height=canvasHeight, width=canvasWidth)
    # canvas.grid(column=0, columnspan=2, sticky='NSEW')
    # canvas.setvar(bg='white')

#
#


# initialize the window

app = Tk()
app.title(APP_TITLE)
app.configure(bg=BG_APP)
app.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
app.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)

# self.grid()

# add text entry field
entryVariable = StringVar()
entryField = Entry(master=app, textvariable=entryVariable)
entryField.grid(column=0, row=0, sticky='EW')
entryVariable.set(TEXT_ENTRY_DEFAULT)

# catch pressing 'Enter' event
entryField.bind("<Return>", OnPressEnter)

# add button
button = Button(master=app, text=TEXT_BUTTON, command=OnButtonClick, font=TEXT_FONT, bg=COLOR_BUTTON_DEFAULT)
button.grid(column=1, row=0)

# add text label
labelText = StringVar()
labelBGColor = StringVar()
labelBGColor.set(BG_LABEL_DEFAULT)
topLabel = Label(app, textvariable=labelText, anchor="w", bd=4, fg=COLOR_LABEL_DEFAULT, bg=BG_LABEL_DEFAULT, font=TEXT_FONT, relief=GROOVE)
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

statsLabel = Label(app, anchor="w", bd=4, fg='red', bg='blue', height=STAT_HEIGHT)
statsLabel.grid(column=0, columnspan=2, sticky='EW')

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


# this method will be executed when the button is clicked

# def OnButtonClick2(self):
#     reqs = ["req1", "req2", "req3", "req4"]
#     durs = [1, 0, 1, 0]
#     d = {'r1':1,'r2':2,'r3':3,'r4':4}
#     y_pos = np.arange(len(reqs))#/(-2),len(reqs)/2)
#     # mask1 =
#     # keys = np.asarray(d.keys())
#     # keys = np.sort(keys)
#     print str(y_pos)
#     # plt.bar(range(len(d)), d.values(), align='center')
#     # plt.xticks(range(len(d)), keys)
#
#     plt.bar(y_pos, durs, align='center', alpha=0.2)
#     plt.xticks(y_pos, reqs)
#
#     plt.ylabel('is busy?')
#     plt.title('workload')
#
#     plt.show()
#
#
# # app = Tk(None)
# # TODO change this to something more meaningful

mainloop()


def showBar():
    requests = ["req1", "req2", "req3", "req4"]# + ["req1", "req2", "req3", "req4"]
    lowerVal, upperVal = 1, 2
    durations = [lowerVal,upperVal,lowerVal,upperVal]# + [s,b,s,b]
    locationsOnXAxis = np.arange(len(requests))
    yValStrings = ['','not busy','busy']
    xLabel = 'recent requests'.upper()
    yLabel = 'is busy?'.upper()
    title = 'workload'.upper()

    plt.bar(locationsOnXAxis, durations, align='center', alpha=0.5,width=0.4)
    plt.xticks(locationsOnXAxis, requests)
    plt.yticks(np.arange(len(yValStrings)), yValStrings)
    plt.ylim(0,3)

    plt.xlabel(xLabel)
    # plt.ylabel(yLabel)
    plt.title(title)


    # x = np.arange(1, 100)
    # y = np.sin(np.arange(1, 100))
    # x = [1,2,3,4]
    # y = durations
    # colors = np.array([(1, 0, 0)] * len(y))
    # colors[y >= 2] = (0, 0, 1)
    # plt.bar(x, y, color=colors)
    plt.show()

# showBar()


