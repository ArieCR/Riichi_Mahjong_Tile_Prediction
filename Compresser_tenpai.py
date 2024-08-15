
from dataset_to_data import *
dataset = MahjongDataset(data_path='tenhou_dataprocess/existingdata/2016-2020.db')

from Data_Skimmer import *
import time

start_time = time.time()
X, y = [], []
counter = 0
for i in dataset:
    temp1,temp2 = tenpai_data_proccecising(i)
    X.append(temp1)
    y.append(temp2)
    counter += 1
    if(counter % 1000 == 0):
        print(f"Processed {counter} entries")
X = np.array(X)
y = np.array(y)

# zipping data into a database
# Zip corresponding rows of X and y together
zipped_data = [(X[i].tolist(), y[i].tolist()) for i in range(X.shape[0])]

# Connect to SQLite database (or create it)
conn = sqlite3.connect('temp/2016-2020_tenpai.db')
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

