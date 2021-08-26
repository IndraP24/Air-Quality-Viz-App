import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet

import warnings
warnings.filterwarnings('ignore')


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
    train_data = data['India_AQI'][:'2018-12']
    test_data = data['India_AQI']['2018-12':]
    print(train_data)
    print(forecast)
    train_data.plot(legend=True, ax=ax)
    test_data.plot(legend=True, ax=ax)

    model.plot(forecast, ax=ax)
    plt.savefig(
        f"artifacts/plots/prophet_model_plot.png")
    model.plot_components(forecast).savefig(
        f"artifacts/plots/prophet_model_plot_components.png")

    prediction_list = forecast.tail(periods).to_dict("records")
    output = {}
    for data in prediction_list:
        date = data['ds'].strftime("%d/%m/%Y")
        output[date] = data['yhat']
    return output


# df = preprocess("../data/city_day.csv")

# print(predict_prophet(df, 36))
