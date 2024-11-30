import os
import sys
import pandas as pd

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from helpers import dt
import batch

def prepare_test_data(year=2023, month=1):
    # print(year, month)
    input_file = batch.get_input_path(year, month)
    print(input_file)

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    print(os.linesep, "Initial data frame:", os.linesep, df.head())

    batch.save_data(df, input_file)

def e2e(year=2023, month=1):
    batch.main(year, month)
