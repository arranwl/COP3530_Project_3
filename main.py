from tkinter import *
import pandas as pd
import time
import sys

#Required to allow deep recursion for sorting. Otherwise the program fails.
sys.setrecursionlimit(5000)

#Defining my own class. This is just for ease of loading in the data and conceptualizing it.
class node:
    def __init__(self, name, age, count, rating, a_color, c_color, r_color):
        self.name = name
        self.age = age
        self.count = count
        self.rating = rating
        self.a_color = a_color
        self.c_color = c_color
        self.r_color = r_color

    #Getter functions
    def getColor(self, in_color):
        if (in_color == "age"):
            return self.a_color
        elif (in_color == "count"):
            return self.c_color
        elif (in_color == "rating"):
            return self.r_color
        else:
            return "error"

    def getVal(self, in_val):
        if (in_val == "age"):
            return self.age
        elif (in_val == "count"):
            return self.count
        elif (in_val == "rating"):
            return self.rating
        else:
            return "error"

    def getName(self):
        return self.name

#Function to load in data. The only reason there's an input file string is due to me using a smaler piece of data for testing earlier in the process.
def loadData(file):
    df = pd.read_csv(file)
    cap = df.shape[0] - (df.shape[0] % 1000)
    #Limits data to 110,000. This was solely done for aesthetics in display, and functionality of display. When it's a rectangle it works better.
    df = df.iloc[:cap,:]
    #Vectorized approach to creating a list of nodes
    nodes = [node(df.loc[i, 'name'], df.loc[i, 'age'], df.loc[i, 'count'], df.loc[i, 'rating'], df.loc[i, 'a_color'],
                  df.loc[i, 'c_color'], df.loc[i, 'r_color']) for i in range(df.shape[0])]
    nrows = int(len(nodes) / 1000)
    #This stores colors in three seperate matrices. When they're put in this shape, then they becomes quicker to display with tkinter, reducing time later.
    cm_age = []
    cm_count = []
    cm_rating = []
    for i in range(nrows):
        age_row = [nodes[j].getColor('age') for j in range(i * 1000, (i + 1) * 1000)]
        count_row = [nodes[j].getColor('count') for j in range(i * 1000, (i + 1) * 1000)]
        rating_row = [nodes[j].getColor('rating') for j in range(i * 1000, (i + 1) * 1000)]
        cm_age.append(age_row)
        cm_count.append(count_row)
        cm_rating.append(rating_row)
    cm = [cm_age, cm_count, cm_rating]
    return nodes, df, cm

#Function to display the correct color based on user input.
def displayNodes():
    if color.get() == 'age':
        cval = 0
    elif color.get() == 'count':
        cval = 1
    else:
        cval = 2
    img.put(cm[cval], (0,0))

#Function that is called when sorting. Checks with algorithm, keeps track of the time, and makes sure the nodes were actually sorted.
#With such small pixels, this brought to my attention my Quick Sort was off by one small typo, so it paid off
def sortNodes():
    algo = sort_algo.get()
    start = time.time()
    if algo == 'merge':
        mergeSortInitial()
    elif algo == 'quick':
        quickSortInitial()
    end = time.time()
    time_val.set(round(end-start, 2))
    displayNodes()
    checkInOrder()

#Merge Sort functions. Taken from the class slides and adapted to Python and my specific data structures.
def mergeSortInitial():
    left = 0
    right = len(data)-1
    mergeSort(left, right, 0)

def merge(left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    X = []
    Y = []

    for i in range(n1):
        X.append(data[left+i])
    for j in range(n2):
        Y.append(data[mid+1+j])

    i = 0
    j = 0
    k = left

    while i < n1 and j <n2:
        if X[i].getVal(sort_var.get()) <= Y[j].getVal(sort_var.get()):
            data[k] = X[i]
            cm[0][int(k / 1000)][int(k % 1000)] = X[i].getColor('age')
            cm[1][int(k / 1000)][int(k % 1000)] = X[i].getColor('count')
            cm[2][int(k / 1000)][int(k % 1000)] = X[i].getColor('rating')
            i += 1
        else:
            data[k] = Y[j]
            cm[0][int(k / 1000)][int(k % 1000)] = Y[j].getColor('age')
            cm[1][int(k / 1000)][int(k % 1000)] = Y[j].getColor('count')
            cm[2][int(k / 1000)][int(k % 1000)] = Y[j].getColor('rating')
            j += 1
        k += 1

    while i < n1:
        data[k] = X[i]
        cm[0][int(k / 1000)][int(k % 1000)] = X[i].getColor('age')
        cm[1][int(k / 1000)][int(k % 1000)] = X[i].getColor('count')
        cm[2][int(k / 1000)][int(k % 1000)] = X[i].getColor('rating')
        i += 1
        k += 1

    while j < n2:
        data[k] = Y[j]
        cm[0][int(k / 1000)][int(k % 1000)] = Y[j].getColor('age')
        cm[1][int(k / 1000)][int(k % 1000)] = Y[j].getColor('count')
        cm[2][int(k / 1000)][int(k % 1000)] = Y[j].getColor('rating')
        j += 1
        k += 1

def mergeSort(left, right, start):
    if (left < right):
        mid = left + int((right - left)/2)
        start += 1
        mergeSort(left, mid, start)
        mergeSort(mid+1, right, start)

        merge(left, mid, right)
        #This section updates the screen depending on the input. The more frequently it updates, the slower the sorting, but more detail shown.
        if (speed_var.get() == '1') and (start % 10 == 0):
            if color.get() == 'age':
                cval = 0
            elif color.get() == 'count':
                cval = 1
            else:
                cval = 2
            img.put(cm[cval], (0, 0))
            root.update()
        elif (speed_var.get() == '2'):
            if color.get() == 'age':
                cval = 0
            elif color.get() == 'count':
                cval = 1
            else:
                cval = 2
            img.put(cm[cval], (0, 0))
            root.update()

#Quick Sort function. Taken from the class slides and adapted to Python and my specific data structure.
def quickSortInitial():
    low = 0
    high = len(data) - 1
    quickSort(low, high, 0)

def partition(low, high):
    pivot = data[low].getVal(sort_var.get())
    up = low
    down = high

    while (up < down):
        for j in range(up, high):
            if data[up].getVal(sort_var.get()) > pivot:
                break;
            up += 1

        for j in reversed(range(low+1, down+1)):
            if data[down].getVal(sort_var.get()) < pivot:
                break;
            down -= 1

        if up < down:
            temp = data[up]
            temp0 = cm[0][int(up / 1000)][int(up % 1000)]
            temp1 = cm[1][int(up / 1000)][int(up % 1000)]
            temp2 = cm[2][int(up / 1000)][int(up % 1000)]

            data[up] = data[down]
            cm[0][int(up / 1000)][int(up % 1000)] = cm[0][int(down / 1000)][int(down % 1000)]
            cm[1][int(up / 1000)][int(up % 1000)] = cm[1][int(down / 1000)][int(down % 1000)]
            cm[2][int(up / 1000)][int(up % 1000)] = cm[2][int(down / 1000)][int(down % 1000)]

            data[down] = temp
            cm[0][int(down / 1000)][int(down % 1000)] = temp0
            cm[1][int(down / 1000)][int(down % 1000)] = temp1
            cm[2][int(down / 1000)][int(down % 1000)] = temp2

            if (speed_var.get() == '2'):
                if color.get() == 'age':
                    cval = 0
                elif color.get() == 'count':
                    cval = 1
                else:
                    cval = 2
                img.put(cm[cval], (0, 0))
                root.update()

    temp = data[low]
    temp0 = cm[0][int(low / 1000)][int(low % 1000)]
    temp1 = cm[1][int(low / 1000)][int(low % 1000)]
    temp2 = cm[2][int(low / 1000)][int(low % 1000)]

    data[low] = data[down]
    cm[0][int(low / 1000)][int(low % 1000)] = cm[0][int(down / 1000)][int(down % 1000)]
    cm[1][int(low / 1000)][int(low % 1000)] = cm[1][int(down / 1000)][int(down % 1000)]
    cm[2][int(low / 1000)][int(low % 1000)] = cm[2][int(down / 1000)][int(down % 1000)]

    data[down] = temp
    cm[0][int(down / 1000)][int(down % 1000)] = temp0
    cm[1][int(down / 1000)][int(down % 1000)] = temp1
    cm[2][int(down / 1000)][int(down % 1000)] = temp2

    if (speed_var.get() == '2'):
        if color.get() == 'age':
            cval = 0
        elif color.get() == 'count':
            cval = 1
        else:
            cval = 2
        img.put(cm[cval], (0, 0))
        root.update()

    return down

def quickSort(low, high, start):
    if low < high:
        pivot = partition(low, high)

        if (speed_var.get() == '1') and (start % 1000 == 0):
            if color.get() == 'age':
                cval = 0
            elif color.get() == 'count':
                cval = 1
            else:
                cval = 2
            img.put(cm[cval], (0, 0))
            root.update()
        start += 1

        quickSort(low, pivot-1, start)
        quickSort(pivot+1, high, start)

#Check that the list is sorted.
def checkInOrder():
    counter = 0
    for i in range(len(data)-1):
        if (data[i].getVal(color.get()) > data[i+1].getVal(color.get())):
            counter += 1
    if counter > 0:
        print('Number of errors:', counter)

#Load in the data
data, df, cm = loadData('project3_data.csv')

#Starting the GUI and set the dimensions
root = Tk()
root.winfo_toplevel().title("")
root.geometry("1008x300")

#Create top frame section, with title and time
top_frame = Frame(root)
top_frame.grid(row=0, column=0)

time_val = DoubleVar()

spacer = Label(top_frame, text="", padx = 50).grid(row=0,column=0)
title = Label(top_frame, text = "IMDb Sorting App", padx = 300).grid(row=0,column=1)
time_disp = Label(top_frame, text = "Time:", padx= 5).grid(row=0, column=2)
time_disp_num = Label(top_frame, textvariable=time_val, highlightthickness=0).grid(row=0, column=3)

#Create bottom frame that holds the selections and button
bottom_frame = Frame(root)
bottom_frame.grid(row=2, column=0)

#Create a specific frame for the selections
selection_frame = Frame(bottom_frame)
selection_frame.grid(row=0,column=0)

#Create the subtitles and selection boxes
speed_title = Label(selection_frame, text = "Animation Speed", padx=50).grid(row=0,column=3)
speed_var = StringVar()
speed1 = Radiobutton(selection_frame, text='No Animation', variable=speed_var, value='0').grid(row=1,column=3)
speed2 = Radiobutton(selection_frame, text='Some Animation', variable=speed_var, value='1').grid(row=2,column=3)
speed3 = Radiobutton(selection_frame, text='Full Animation', variable=speed_var, value='2').grid(row=3,column=3)

#When a color is selected is when the ndoes are first displayed
color_title = Label(selection_frame, text = "Coloring", padx=50).grid(row=0,column=2)
color = StringVar()
color1 = Radiobutton(selection_frame, text='Age', variable=color, value='age', command=displayNodes).grid(row=1,column=2)
color2 = Radiobutton(selection_frame, text='Average Rating', variable=color, value='rating', command=displayNodes).grid(row=2,column=2)
color3 = Radiobutton(selection_frame, text='Number of Movies', variable=color, value='count', command=displayNodes).grid(row=3,column=2)

var_title = Label(selection_frame, text = "Element to Sort by", padx=50).grid(row=0,column=1)
sort_var = StringVar()
element1 = Radiobutton(selection_frame, text='Age', variable=sort_var, value='age').grid(row=1,column=1)
element2 = Radiobutton(selection_frame, text='Average Rating', variable=sort_var, value='rating').grid(row=2,column=1)
element3 = Radiobutton(selection_frame, text='Number of Movies', variable=sort_var, value='count').grid(row=3,column=1)

algo_title = Label(selection_frame, text = "Sorting Algorithm", padx=50).grid(row=0,column=0)
sort_algo = StringVar()
sort1 = Radiobutton(selection_frame, text='Merge Sort', variable=sort_algo, value='merge').grid(row=1,column=0)
sort2 =Radiobutton(selection_frame, text='Quick Sort', variable=sort_algo, value='quick').grid(row=2,column=0)

#Create the button for starting sort
button_frame = Frame(bottom_frame, padx=50)
button_frame.grid(row=0,column=1)

button = Button(button_frame, text="Sort", padx=20, pady=10, command = sortNodes )
button.grid(row=0, column=0)

#Code to display the nodes properly
WIDTH, HEIGHT = 1002, 102
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg = "#ADD8E6")
canvas.grid(row=1, column=0)
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH / 2 + 4, HEIGHT / 2 + 4), image=img, state="normal")

root.mainloop()