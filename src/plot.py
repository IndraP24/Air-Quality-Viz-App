import pandas as pd
import folium
from folium.plugins import HeatMap
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
print('columns->', my_data.columns)  # 2 cols ‘status’ and ‘data’
