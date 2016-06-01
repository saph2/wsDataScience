#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ------------- constants -------------

# background colors
BG_APP = 'DarkOrchid4'
BG_LABEL_DEFAULT = 'plum1'
BG_LABEL_RED = 'red'
NG_LABEL_GREEN = 'green'
BG_CANVAS = 'black'

# text colors
COLOR_BUTTON = 'brown3'
COLOR_LABEL = 'brown'

# window size
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
STAT_HEIGHT = 200

# text fields
TEXT_BUTTON = u"Evaluate request"
TEXT_ENTRY_DEFAULT = u"Enter request here..."
APP_TITLE = 'workload prediction app'.upper()

#other consts
TEXT_FONT = 'Helvetica'


colors = ['red', 'green']


class GUI_APP(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent

        # set window size

        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.initialize()

    # initialize the window
    def initialize(self):
        self.grid()

        # add text entry field
        self.entryVariable = StringVar()
        self.entryField = Entry(self, textvariable=self.entryVariable)
        self.entryField.grid(column=0, row=0, sticky='EW')
        self.entryVariable.set(TEXT_ENTRY_DEFAULT)

        # catch pressing 'Enter' event
        self.entryField.bind("<Return>", self.OnPressEnter)

        # add button
        button = Button(self, text=TEXT_BUTTON, command=self.OnButtonClick, font=TEXT_FONT, bg=COLOR_BUTTON)
        button.grid(column=1, row=0)

        # add text label
        self.labelText = StringVar()
        self.labelBGColor = StringVar()
        self.labelBGColor.set(BG_LABEL_DEFAULT)
        topLabel = Label(self, textvariable=self.labelText, anchor="w", bd=4, fg=COLOR_LABEL, bg=BG_LABEL_DEFAULT, font=TEXT_FONT, relief=GROOVE)
        topLabel.grid(column=0, row=1, rowspan=2, columnspan=2, sticky='EW')
        # TODO change this to something more meaningful
        self.labelText.set(u"Hello !")


        # ---------------- canvas ----------------------

        requests = ["req1", "req2", "req3", "req4"]
        durations = [4, 2, 4, 4,    2, 4, 4, 4,     4, 2]

        canvasWidth = 800
        canvasHeight = 600
        # add canvas that will hold the bar chart
        canvas = Canvas(self, bg=BG_CANVAS, height=canvasHeight, width=canvasWidth)
        canvas.grid(column=0, columnspan=2, sticky='NSEW')

        # highest y = max_data_value * y_stretch
        y_stretch = 60

        # gap between lower canvas edge and x axis
        y_gap = 100

        # distance between bars
        x_stretch = 40

        # width of a bar
        x_width = 40

        # gap between left canvas edge and y axis
        x_gap = 20#c_width/2 - (len(durations)/2)*x_stretch


        for x, y in enumerate(durations):
            # x is the location of the bar along the x-axis
            # y is the height of the bar at location x
            print 'x = ' + str(x) + '; y = ' + str(y)

            # calculate reactangle coordinates (integers) for each bar
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvasHeight - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvasHeight - y_gap

            # draw the bar
            if(y > 2):
                canvas.create_rectangle(x0, y0, x1, y1, fill=colors[0])
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill=colors[1])
            # put the y value above each bar
            canvas.create_text(x0 + 2, y0, anchor=SW, text='req' + str(x+1), font=TEXT_FONT, fill='white')

        # ------------ end canvas -----------



        # ------------ bottom statistics -----------

        # ----------- end statistics ----------------

        statsLabel = Label(self, anchor="w", bd=4, fg='red', bg='blue', height=STAT_HEIGHT)
        statsLabel.grid(column=0, columnspan=2, sticky='EW')

        # allow resizing of the window when long text is entered in the entry field
        self.grid_columnconfigure(0,weight=1)
        # allow only horizontal resizing (and not vertical)
        self.resizable(True,False)

        # prevent constant resizing of the window
        self.update()
        self.geometry(self.geometry())

        # auto select the text field
        self.entryField.focus_set()
        self.entryField.selection_range(0, END)


    # this method will be executed when the button is clicked
    def OnButtonClick(self):
        self.labelText.set(self.entryVariable.get() + " (You clicked the button)")
        self.labelBGColor.set(BG_LABEL_RED)
        # self.canvas = Canvas(self, bg='black', height=100, width=100)
        # self.canvas.grid(column=0, columnspan=2, sticky='NSEW')

        # auto select the text field
        self.entryField.focus_set()
        self.entryField.selection_range(0, END)

        canvasWidth = 800
        canvasHeight = 600

        # highest y = max_data_value * y_stretch
        y_stretch = 60

        # gap between lower canvas edge and x axis
        y_gap = 100

        # distance between bars
        x_stretch = 40

        # width of a bar
        x_width = 40

        # gap between left canvas edge and y axis
        x_gap = 20  # c_width/2 - (len(durations)/2)*x_stretch
        durations = [4, 2, 4, 4,    2, 4, 4, 4,     4, 2]

        for x, y in enumerate(durations):
            # x is the location of the bar along the x-axis
            # y is the height of the bar at location x
            print 'x = ' + str(x) + '; y = ' + str(y)

            # calculate reactangle coordinates (integers) for each bar
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvasHeight - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvasHeight - y_gap

            # draw the bar
            if (y > 2):
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[1])
            else:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[0])
            # put the y value above each bar
            self.canvas.create_text(x0 + 2, y0, anchor=SW, text='req' + str(x + 1), font=TEXT_FONT, fill='white')


            # self.showBar(self)

    # this method will be executed when 'Enter' is pressed in the entry field
    def OnPressEnter(self,event):
        # self.OnButtonClick()
        self.labelText.set(self.entryVariable.get() + " (You pressed enter !)")

        # auto select the text field
        self.entryField.focus_set()
        self.entryField.selection_range(0, END)


    def OnButtonClick2(self):
        reqs = ["req1", "req2", "req3", "req4"]
        durs = [1, 0, 1, 0]
        d = {'r1':1,'r2':2,'r3':3,'r4':4}
        y_pos = np.arange(len(reqs))#/(-2),len(reqs)/2)
        # mask1 =
        # keys = np.asarray(d.keys())
        # keys = np.sort(keys)
        print str(y_pos)
        # plt.bar(range(len(d)), d.values(), align='center')
        # plt.xticks(range(len(d)), keys)

        plt.bar(y_pos, durs, align='center', alpha=0.2)
        plt.xticks(y_pos, reqs)

        plt.ylabel('is busy?')
        plt.title('workload')

        plt.show()


if __name__ == "__main__":
    app = GUI_APP(None)
    # TODO change this to something more meaningful
    app.title(APP_TITLE)
    app.configure(bg=BG_APP)
    app.mainloop()


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
