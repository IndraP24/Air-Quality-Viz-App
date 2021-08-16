import numpy as np
import pandas as pd
import missingno as msno


# importing day-wise data of cities
cities = pd.read_csv('../data/city_day.csv')

# converting column Date into DateTime format
cities['Date'] = pd.to_datetime(cities['Date'])

# filling missing values with zero
cities.fillna(0, inplace=True)

# extracting year and month for each record
cities['year'] = pd.DatetimeIndex(cities['Date']).year
cities['month'] = pd.DatetimeIndex(cities['Date']).month

# clubbing all particulate matter
cities['PM'] = cities['PM2.5'] + cities['PM10']

# clubbing nitrogen oxides
cities['Nitric'] = cities['NO'] + cities['NO2'] + cities['NOx']

# clubbing organic compounds - Benzene, toluene and Xylene together
cities['BTX'] = cities['Benzene'] + cities['Toluene'] + cities['Xylene']

# grouping pollutant levels in every city by year and month
cities_group_ym = cities.groupby(['City', 'year', 'month'])[
    ['PM', 'Nitric', 'CO', 'NH3', 'O3', 'SO2', 'BTX', 'AQI']].mean()

cities_group_ym = cities_group_ym.reset_index(['City', 'year', 'month'])
