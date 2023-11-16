import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim

def load_data():
    crime_data = pd.read_csv("crime.csv")
    return gpd.GeoDataFrame(crime_data, geometry=gpd.points_from_xy(crime_data.longitude, crime_data.latitude))

crime_df = load_data()

# Create a Streamlit web app
st.title("Crime Detection App")

# User input for date and location
date = st.date_input("Select a date", pd.to_datetime('6/2/2018'))  # Default to January 1, 2023
location = st.text_input("Enter Location")
latitude, longitude = None, None

# Convert the location to latitude and longitude
if location:
    geolocator = Nominatim(user_agent="crime_detection_app")
    location_info = geolocator.geocode(location)
    if location_info:
        latitude, longitude = location_info.latitude, location_info.longitude

# Filter crime data based on user input
if latitude is not None and longitude is not None:
    filtered_crimes = crime_df[(crime_df["date"] == date) & (crime_df["latitude"] == latitude) & (crime_df["longitude"] == longitude)]
else:
    filtered_crimes = None

# Display the map with crime details
st.write(f"Crime Details in {location} on {date}")
if filtered_crimes is not None:
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    for idx, row in filtered_crimes.iterrows():
        popup_text = f"Date: {row['date']}<br>Location: {row['location']}<br>Crime Type: {row['crime_type']}<br>Previous Activity: {row['previous_activity']}"
        folium.Marker([row["latitude"], row["longitude"]], popup=popup_text).add_to(m)
    st.write(m)
else:
    st.write("No matching crime data found for the specified date and location.")
