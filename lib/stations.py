# Author:- Indrashis Paul | Email:- indrashis985@mail.com

# %%
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(layout='centered', page_icon="😷",
                   page_title="Air Quality-India")

# -STEP 1 DOWNLOAD DATA
# See details of API at:- https://aqicn.org/api/
base_url = "https://api.waqi.info"
# Get token from:- https://aqicn.org/data-platform/token/#/
tok = '2136d1645754b9864a6e0d4560abdff99836ee48'
# (lat, long)-> bottom left, (lat, lon)-> top right
# India is 8N 61E to 37N, 97E approx
latlngbox = "8.0000,61.0000,37.0000,97.0000"  # For India
trail_url = f"/map/bounds/?latlng={latlngbox}&token={tok}"
my_data = pd.read_json(base_url + trail_url)  # Join parts of URL
print('columns->', my_data.columns)  # 2 cols 'status' and 'data'
print(my_data['data'].head())

# %%
# -STEP 2: Create table like DataFrame
all_rows = []
for each_row in my_data['data']:
    all_rows.append([each_row['station']['name'],
                     each_row['lat'],
                     each_row['lon'],
                     each_row['aqi']])
df = pd.DataFrame(all_rows,
                  columns=['station_name', 'lat', 'lon', 'aqi'])
print(df.head())

# %%
# -STEP 3:- Clean the DataFrame
df['aqi'] = pd.to_numeric(df.aqi,
                          errors='coerce')  # Invalid parsing to NaN
print('with NaN ->', df.shape)  # Comes out as (147, 4)
# Remove NaN (Not a Number) entries in col
df1 = df.dropna(subset=['aqi'])
print('without NaN ->', df1.shape)  # (139, 4)

# %%
# -STEP 4: Make plotly heat map
init_loc = dict(lat=23, lon=80)  # Approx over Bhopal
max_aqi = int(df1['aqi'].max())
print('max_aqi->', max_aqi)
df2 = df1[['lat', 'lon', 'aqi']]
fig = px.density_mapbox(df2, lat='lat', lon='lon', z='aqi', radius=20,
                        center=init_loc, zoom=4,
                        mapbox_style="open-street-map", width=800, height=800)
st.plotly_chart(fig)

# %%
# -STEP 5: Plot stations on map
centre_point = [23.25, 77.41]  # Approx over Bhopal
m2 = folium.Map(location=centre_point,
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
                  icon=folium.Icon(color=pop_color)).add_to(m2)


site_lat = df1.lat
site_lon = df1.lon
locations_name = df1.station_name

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=17,
        color='rgb(255, 0, 0)',
        opacity=0.7
    ),
    text=locations_name,
    hoverinfo='text'
))


st.plotly_chart(fig)
# %%
# streamlit-folium
st.title("Air Quality Marker Map")
folium_static(m2)
