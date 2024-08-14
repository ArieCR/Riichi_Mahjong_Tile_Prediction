
import torch
import sqlite3
import pandas as pd
from dataset_to_data import *
dataset = MahjongDataset(data_path='tenhou_dataprocess/existingdata/2016-2020.db')



from Data_Skimmer import *
import time

start_time = time.time()
X, y = [], []

for i in dataset:
    temp = waits_data_proccessing(i)
    if(temp == None):
        continue
    X.append(temp[0])
    y.append(temp[1])
X = np.array(X)
y = np.array(y)

# zipping data into a database
# Zip corresponding rows of X and y together
zipped_data = [(X[i].tolist(), y[i].tolist()) for i in range(X.shape[0])]

# Connect to SQLite database (or create it)
conn = sqlite3.connect('tenhou_dataprocess/dst/test.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_table (
    id INTEGER PRIMARY KEY,
    X_values BLOB,
    y_values BLOB
)
''')

# Insert the zipped data into the table
for i, (X_row, y_row) in enumerate(zipped_data):
    cursor.execute('INSERT INTO test_table (X_values, y_values) VALUES (?, ?)', (str(X_row), str(y_row)))

# Commit and close the connection
conn.commit()
conn.close()


X = torch.tensor(X, dtype=torch.float)  # Use long for input data
y = torch.tensor(y, dtype=torch.float)     # Use long for integer labels
# until here!!!

