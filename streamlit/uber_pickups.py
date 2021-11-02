import streamlit as st
import numpy as np
import pandas as pd
import altair as alt


'''
# Uber pickups excercise
'''

DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'


@st.cache(suppress_st_warning = True)
def download_data():
    return pd.read_csv(DATA_URL)


nrow = st.sidebar.slider('No. rows to display:', 0, 10000, value = 1000)
hour_range = st.sidebar.slider('Select the hour range:', min_value = 0, max_value = 23, value = (8, 17))
st.sidebar.write('Hours selected from {} to {}'.format(hour_range[0], hour_range[1]))

data = (download_data()
        .rename(columns = {'Date/Time': 'date_time', 'Lat': 'lat', 'Lon': 'lon', 'Base': 'base'})
        .assign(date_time = lambda df: pd.to_datetime(df.date_time))
        .loc[lambda df: (df.date_time.dt.hour >= hour_range[0]) & (df.date_time.dt.hour < hour_range[1])]
        .loc[1:nrow]
        .sort_values(by = 'date_time')
        )
data

st.map(data)

'''
# Uber Trips Hist
'''


trips_per_hour = data.date_time.dt.hour.value_counts()
trips_per_hour.index.name = 'hour'
st.bar_chart(trips_per_hour)