import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')


def predict_sarima(data: pd.DataFrame, steps: int):
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
    train_data.plot(legend=True, ax=ax)
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
# print(predict_arima(df, steps=36))
