import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet
import joblib
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')


def preprocess(data_path: str):
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    cities_all = df.pivot_table(values='AQI', index=['Date'], columns='City')
    cities_all = cities_all.add_suffix('_AQI')
    cities = cities_all.resample(rule='MS').mean()
    cities['India_AQI'] = cities.mean(axis=1)
    cities.reset_index()
    return cities


def predict_prophet(data: pd.DataFrame, periods: int):
    df_forecast = data.copy()
    df_forecast.reset_index(inplace=True)
    df_forecast['ds'] = df_forecast['Date']
    df_forecast['y'] = df_forecast['India_AQI']
    df_forecast = df_forecast[["ds", "y"]]
    train_data = df_forecast[df_forecast['ds'] <= '2018-12']
    test_data = df_forecast[df_forecast['ds'] >= '2018-12']

    model = Prophet(seasonality_mode='multiplicative')
    model.fit(train_data)

    future = model.make_future_dataframe(periods=periods, freq='MS')

    forecast = model.predict(future)

    fig, ax = plt.subplots(figsize=(10, 6))

    model.plot(forecast, ax=ax).savefig(
        f"artifacts/plots/prophet_model_plot.png")
    model.plot_components(forecast).savefig(
        f"artifacts/plots/prophet_model_plot_components.png")

    prediction_list = forecast.tail(periods).to_dict("records")
    output = {}
    for data in prediction_list:
        date = data['ds'].strftime("%d/%m/%Y")
        output[date] = data['yhat']
    return output


def predict_arima(data: pd.DataFrame, steps: int):
    # dividing into train and test:
    train_data = data['India_AQI'][:'2018-12']
    test_data = data['India_AQI']['2018-12':]

    # Building the model:
    model = SARIMAX(train_data, order=(0, 1, 2),
                    seasonal_order=(1, 0, 1, 12), trend='n')
    results = model.fit()

    fig, ax = plt.subplots(figsize=(10, 6))

    # predict the next steps of months values to compare with the test dataset
    forecasts = results.get_forecast(steps=steps, dynamic=True)

    # find the confidence intervals
    confidence_intervals = forecasts.conf_int()
    lower_limits = confidence_intervals.loc[:, 'lower India_AQI']
    upper_limits = confidence_intervals.loc[:, 'upper India_AQI']

    # plot the forecasted mean data for the next 12 months and the confidence interval
    forecasts.predicted_mean.plot(legend=True, ax=ax, label='Predicted Values')
    plt.fill_between(confidence_intervals.index,
                     lower_limits, upper_limits, color='pink')

    # plotting the actual value from test data
    train_data.plot(legend=True, ax=ax, )
    test_data.plot(legend=True, ax=ax)
    ax.legend(['Forecasted Result', 'Training India_AQI', 'Testing India_AQI'])
    plt.savefig(f"artifacts/plots/arima_model_plot.png")

    prediction_list = forecasts.predicted_mean.reset_index().to_dict("records")
    output = {}
    for data in prediction_list:
        date = data['index'].strftime("%d/%m/%Y")
        output[date] = data['predicted_mean']
    return output


# df = preprocess("../data/city_day.csv")

# # print(predict_prophet(df, 36))

# print(predict_arima(df, steps=36))
