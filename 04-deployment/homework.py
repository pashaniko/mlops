#!/usr/bin/env python
# coding: utf-8
# In[3]:

import sys
import pickle
import pandas as pd

# variables
year = int(sys.argv[1]) # 2023
month = int(sys.argv[2]) # 4

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

print('input file:', input_file)
df = read_data(input_file)

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

# Q5. Parametrize the script
# What's the mean predicted duration?
print('predicted mean duration:', y_pred.mean())

# Q1. Standard deviation
print('standard deviation of the predicted duration:', y_pred.std())

# Q2. Preparing the output
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

print('output file:', output_file)
df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)
