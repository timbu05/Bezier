import csv
import os
from encodings import utf_8 
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def draw_fig(x, y, mark, fig):
    cs = CubicSpline(x, y)
    fig.add_trace(go.Scatter(x=np.arange(0, 1.01, 0.01), y = cs(np.arange(0, 1.01, 0.01))))


fig = go.Figure()
listx2 = [0]
listPdelkPa = [] 
listPdelPa = []
listy1 = []
listy2 = []
listG = [0]


def dr(res):
    fig = go.Figure()
    listx2 = [0]
    listPdelkPa = [] 
    listPdelPa = []
    listy1 = []
    listy2 = []
    listG = [0]
    with open(res, encoding='utf-8') as file1:
        file_reader = csv.reader(file1, delimiter = ";")
        row = file_reader.__next__()
        row = file_reader.__next__()
        mark = row[-1]
        for row in file_reader:
            print(row)
            if row[0] != '':
                listx2.append(float(row[0]))
                listPdelkPa.append(float(row[1]))
                listPdelPa.append(float(row[2]))
                listy1.append(float(row[3]))
                listy2.append(float(row[4]))
                listG.append(float(row[5]))
            if row[0] == '':
                listx2 = np.array(listx2)
                listPdelkPa = np.array(listPdelkPa)
                listPdelPa = np.array(listPdelPa)
                listy1 = np.array(listy1)
                listy2 = np.array(listy2)
                listG = np.array(listG)
                draw_fig(listx2, listG, mark, fig)
                mark = row[-1]
                listx2 = [0]
                listPdelkPa = [] 
                listPdelPa = []
                listy1 = []
                listy2 = []
                listG = [0]
    return fig.show()


