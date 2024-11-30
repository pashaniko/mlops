import pandas as pd

import os
import batch
from helpers import dt


def test_prepare_data():

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    data_columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    data_df = pd.DataFrame(data, columns=data_columns)
    # print("Initial data frame:", data_df)
    print(os.linesep, "Initial data frame:", data_df.head(n=10).to_string(index=False))

    expected_data = [
        ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
        ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    ]
    expected_columns = data_columns + ['duration']
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)
    expected_df = expected_df.astype(
        {"PULocationID": "object", "DOLocationID": "object"}
    )
    # print("Expected data frame:", expected_df.head())
    print(os.linesep, "Expected data frame:", expected_df.head(n=10).to_string(index=False))

    actual_df = batch.prepare_data(data_df, categorical=["PULocationID", "DOLocationID"])
    # print("Actual data frame:", actual_df)
    print(os.linesep, "Actual data frame:", actual_df.head(n=10).to_string(index=False))
    
    # print(actual_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)

