import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import datetime

@st.cache
def load_crime_data():
    data = pd.read_csv('crime.csv')
    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time_of_day'])
    return data

crime_data = load_crime_data()

# Create a Streamlit map to display the crime data
st.title("Crime Prediction and Reporting")

st.sidebar.title("Crime Data Map")

# Display a map of the crime data
st.sidebar.map(crime_data)

# Display the crime dataset
st.subheader("Crime Data")
st.write(crime_data)

# Create a form for users to report incidents
st.sidebar.subheader("Report an Incident")
user_location = st.sidebar.text_input("Your Location (latitude, longitude)")
incident_type = st.sidebar.selectbox("Incident Type", crime_data['crime_type'].unique())
report_button = st.sidebar.button("Report")

if report_button:
    if user_location:
        user_location = user_location.split(',')
        if len(user_location) == 2:
            user_latitude, user_longitude = float(user_location[0]), float(user_location[1])
            current_datetime = datetime.datetime.now()
            new_report = {
                'datetime': current_datetime,
                'date': current_datetime.date(),
                'time_of_day': current_datetime.time(),
                'crime_type': incident_type,
                'location': "User-reported",
                'latitude': user_latitude,
                'longitude': user_longitude,
                'victim_gender': None,
                'victim_age': None,
                'perpetrator_gender': None,
                'perpetrator_age': None,
                'weapon': None,
                'injury': None,
                'weather': None,
                'temperature': None,
                'previous_activity': None,
            }
            crime_data = crime_data.append(new_report, ignore_index=True)

# Display the updated crime dataset with the user-reported incident
st.subheader("Updated Crime Data")
st.write(crime_data)

# Create a heatmap of crime hotspots
st.sidebar.subheader("Crime Hotspot Map")
st.sidebar.map(crime_data)

# Create a time slider to explore crime data over time
st.sidebar.subheader("Time Slider")
time_slider = st.sidebar.slider("Select Hour of the Day", 0, 23, 12)
filtered_crime_data = crime_data[crime_data['datetime'].dt.hour == time_slider]

# Display crime data for the selected time
st.sidebar.write("Crime Data for Selected Hour:")
st.sidebar.write(filtered_crime_data)

# Create a heatmap for the selected time
st.sidebar.map(filtered_crime_data)

