# Author:- Indrashis Paul | Email:- indrashis985@mail.com


import pandas as pd
import folium
from folium.plugins import HeatMap


def load_data():
    """ Function to download Data from API and create a Pandas DataFrame """
    # See details of API at:- https://aqicn.org/api/
    base_url = "https://api.waqi.info"

    # Get token from:- https://aqicn.org/data-platform/token/#/
    tok = '2136d1645754b9864a6e0d4560abdff99836ee48'

    # (lat, long)-> bottom left, (lat, lon)-> top right
    # India is 8N 61E to 37N, 97E approx
    latlngbox = "8.0000,61.0000,37.0000,97.0000"  # For India

    trail_url = f"/map/bounds/?latlng={latlngbox}&token={tok}"
    my_data = pd.read_json(base_url + trail_url)  # Join parts of URL

    all_rows = []
    for each_row in my_data['data']:
        all_rows.append([each_row['station']['name'],
                        each_row['lat'],
                        each_row['lon'],
                        each_row['aqi']])
    df = pd.DataFrame(all_rows,
                      columns=['station_name', 'lat', 'lon', 'aqi'])

    df['aqi'] = pd.to_numeric(df.aqi,
                              errors='coerce')  # Invalid parsing to NaN
    # Remove NaN (Not a Number) entries in col
    df1 = df.dropna(subset=['aqi'])

    return df1


def plot(df1: pd.DataFrame):
    """ Function to plot stations with their labelled AQI on Geo Map """
    centre_point = [22.1671, 80.2340]  # Approx over Jabalpur for map centering
    m = folium.Map(location=centre_point,
                   tiles='OpenStreetMap',
                   zoom_start=5)
    for idx, row in df1.iterrows():
        lat = row['lat']
        lon = row['lon']
        station = row['station_name'] + ' AQI=' + str(row['aqi'])
        station_aqi = row['aqi']
        if station_aqi > 151:  # Red for very bad AQI
            pop_color = 'red'
        elif station_aqi > 101:
            pop_color = 'orange'  # Orange for moderate AQI
        else:
            pop_color = 'green'  # Green for good AQI
        folium.Marker(location=[lat, lon],
                      popup=station,
                      icon=folium.Icon(color=pop_color)).add_to(m)

    return m
