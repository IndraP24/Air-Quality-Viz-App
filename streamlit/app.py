# Author:- Indrashis Paul | Email:- indrashis985@mail.com

import streamlit as st
from streamlit_folium import folium_static

from utils import *

st.set_page_config(layout='centered', page_icon="😷",
                   page_title="Air Quality-India")


df = load_data()
map = plot(df)


# streamlit-folium
st.title("Air Quality Marker Map")
folium_static(map, height=700, width=700)
