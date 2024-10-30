################################################ CHICAGO CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################
st.set_page_config(
    page_title="CHICAGO CITI BIKES DASHABOARD",  # Title of the tab in the browser
    page_icon="🚴‍♂️",  # Optional: set a custom emoji/icon
    layout="wide"  # Use wide screen layout for better visibility
)

st.title("Bike Rides and Weather Dashboard")
st.write("""
Welcome to the Chicago Citi Bikes Dashaboard. 

This dashboard is designed to provide insights into daily bike rides and weather patterns. 
You can explore the number of trips taken from various stations, observe trends over time, 
and understand how temperature correlates with biking activity. 
Use the interactive charts and visualizations below to dive deeper into the data.
""")

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top_20_stations = pd.read_csv('top_20_stations.csv', index_col = 0)



# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

# Adding blue color to the palette
fig = go.Figure(go.Bar(x = top_20_stations['start_station_name'], y = top_20_stations['trip_count'], marker = {'color': top_20_stations['trip_count'],'colorscale': 'Blues'}))
fig.update_layout(
     title = 'Top 20 most popular bike stations in Chicago',
     xaxis_title = 'Start stations',
     yaxis_title ='Sum of trips',
     width = 900, height = 600)

st.plotly_chart(fig, use_container_width=True)


## Line chart 

# Create subplots with secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add the line for daily bike rides (in blue)
fig_2.add_trace(
    go.Scatter(x=df['date'], y=df['bike_rides_daily'], name='Daily Bike Rides', line=dict(color='blue')),
    secondary_y=False
)

# Add the line for daily temperature (in red)
fig_2.add_trace(
    go.Scatter(x=df['date'], y=df['avgTemp'], name='Daily Temperature', line=dict(color='red')),
    secondary_y=True
)

# Update layout with title
fig_2.update_layout(
    title_text='Daily Bike Rides and Temperature Over Time',  # Set the title
    xaxis_title='Date',
    yaxis_title='Bike Rides',
    legend=dict(x=0.1, y=1.1)  # Position legend above plot
)

# Update y-axis titles
fig_2.update_yaxes(title_text='Daily Bike Rides', secondary_y=False)
fig_2.update_yaxes(title_text='Daily Temperature', secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)


### Add the kepler map ###

path_to_html = "kepler_map.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in Chicago")
st.components.v1.html(html_data,height=1000)


