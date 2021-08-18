import pandas as pd
import numpy as np
from pmdarima import auto_arima

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


def train(data: pd.DataFrame):
    auto_arima(y=data['India_AQI'], start_p=1, start_P=1, start_q=1,
               start_Q=1, seasonal=True, m=12, stepwise=True).summary()
