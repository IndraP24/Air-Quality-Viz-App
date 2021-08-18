import pandas as pd
import numpy as np


import warnings
warnings.filterwarnings('ignore')


def preprocess(data: str):
    df = pd.read_csv(data)
    df['Date'] = pd.to_datetime(df['Date'])
    cities_all = df.pivot_table(values='AQI', index=['Date'], columns='City')
    cities_all = cities_all.add_suffix('_AQI')
    cities = cities_all.resample(rule='MS').mean()
    cities['India_AQI'] = cities.mean(axis=1)
    cities.reset_index()
    return cities
