# Author:- Indrashis Paul | Email:- indrashis985@mail.com

import streamlit as st
from streamlit_folium import folium_static

from utils import *

st.set_page_config(layout='centered', page_icon="😷",
                   page_title="Air Quality-India", initial_sidebar_state="expanded")

st.markdown("<p style='text-align: right; color: red;'>😵In beta mode</p>",
            unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: darkblue;'>Automated Air Quality Forecasting - India 2015-20</h1>",
            unsafe_allow_html=True)
"""---"""

"""
This data app uses Facebook's open-source **Prophet** library and a popular Python module, **statsmodels** to automatically generate future forecast values of the Cumulative Air Quality Index of India from datasets that can be chosen from.

You'll be able to select a CSV file from the given options, visualize trends and features, analyze forecast performance of the Cumulative Air Quality Index of India, and finally download the created forecast 


Created by Indrashis Paul: https://twitter.com/PaulIndrashis

---
"""

st.markdown("<h3 style='text-align: left; color: green;'>Step 1: Import Data</h3>",
            unsafe_allow_html=True)

"""
Choose the data you wish to forecast on from the given two options: City Daily Data and the Stations Daily Data.
Both contain identical columns but the number of samples is different.

The city data contains the data from various cities throughout India while the stations data contains the data only from specific weather stations in India.

Although you will forecast the Cumulative AQI of India from both the datasets, it still might lead to different results.

"""
data_names = ['City Data', 'Station Data']
data = st.radio("Dataset", data_names)

if data == 'City Data':
    path = "data/city_day.csv"
elif data == 'Station Data':
    path = "data/station_day.csv"

df = pd.read_csv(path)

st.write("**The chosen data is: **", data)
st.write(df)
st.write("#### ❗Note: Only the **Date** and the **AQI** column will be used from the chosen data ", data)


"""---"""


st.markdown("<h3 style='text-align: left; color: green;'>Step 2: Select the Model for Training and the Forecast Horizon</h3>",
            unsafe_allow_html=True)
model_names = ['FB Prophet', 'statsmodels sARIMA']
model = st.radio("Time Series Models", model_names)

if model == 'FB Prophet':
    model_in = "Prophet"
elif model == 'statsmodels sARIMA':
    model_in = "Arima"

st.write(
    'How many periods [months] would you like to forecast into the future?')
periods_input = st.number_input('', min_value=1, max_value=500)

st.write("**The chosen model is: **", model)
st.write("**The forecasting period is: **", periods_input)
"""---"""


st.markdown("<h1 style='text-align: center; color: darkblue;'>Air Quality Marker Map</h1>",
            unsafe_allow_html=True)
df = load_data()
map = plot(df)
folium_static(map, height=700, width=700)
