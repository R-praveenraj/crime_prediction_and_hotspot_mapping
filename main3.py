import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from twilio.rest import Client
from folium.plugins import HeatMapWithTime

crime_data = pd.read_csv('crime.csv')

gdf = gpd.GeoDataFrame(crime_data, 
                     geometry=gpd.points_from_xy(crime_data.longitude, crime_data.latitude))

TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
POLICE_PHONE_NUMBER = 'police_phone_number'

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Streamlit interface
st.title("Crime Prediction and Reporting")

# Display a map of the crime data
st.subheader("Crime Data Map")
m = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
for idx, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['crime_type']).add_to(m)
folium_static(m)

# Report an incident
st.subheader("Report an Incident")
Date= st.date_input("Date")
user_location = st.text_input("Your Location (latitude, longitude)")
incident_type = st.selectbox("Incident Type", crime_data['crime_type'].unique())
report_button = st.button("Report")

if report_button:
    if user_location:
        user_location = user_location.split(',')
        if len(user_location) == 2:
            user_latitude, user_longitude = float(user_location[0]), float(user_location[1])
            new_report = {
                'latitude': user_latitude,
                'longitude': user_longitude,
                'crime_type': incident_type,
            }
            # Send a message to the police department using Twilio
            message = twilio_client.messages.create(
                body=f"Incident reported: {incident_type} at {user_location}",
                from_=TWILIO_PHONE_NUMBER,
                to=POLICE_PHONE_NUMBER
            )
            st.success(f"Incident reported. Message sent to the police department.")
# Create a heatmap of crime hotspots (simplified, not a real predictive model)
# st.subheader("Crime Hotspot Map")
# heatmap = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
# HeatMap(data=crime_data[['latitude', 'longitude']].values, radius=15).add_to(heatmap)
# folium_static(heatmap)
st.subheader("Crime Hotspot Map")
heatmap = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
HeatMapWithTime(data=crime_data[['latitude', 'longitude']].values, radius=15).add_to(heatmap)
folium_static(heatmap)
