
import torch
import sqlite3
import pandas as pd
from dataset_to_data import *
dataset = MahjongDataset(data_path='2016-2020.db')
from Data_Skimmer import *
import time
import numpy
start_time = time.time()
X, y = [], []
count = 0
for i in dataset:
    temp = waits_data_proccessing(i)
    if(temp == None):
        continue
    X.append(temp[0])
    y.append(temp[1])
    count+=1
    if count%1000 == 0: print("count is ", count)
X_np = numpy.array(X)
y_np = numpy.array(y)
numpy.save("X.npy",X_np)
numpy.save("y.npy",y_np)
X_torch = torch.tensor(X)
y_torch = torch.tensor(y)
torch.save(X_torch, 'X.pt')
torch.save(y_torch, 'y.pt')
# zipping data into a database
# Zip corresponding rows of X and y together

X = torch.tensor(X, dtype=torch.float)  # Use long for input data
y = torch.tensor(y, dtype=torch.float)     # Use long for integer labels
# until here!!!

