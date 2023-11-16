import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMapWithTime

# Load the crime data from the CSV file
crime_data = pd.read_csv('crime.csv')

# Create a GeoDataFrame from latitude and longitude columns
gdf = gpd.GeoDataFrame(crime_data, 
                     geometry=gpd.points_from_xy(crime_data.longitude, crime_data.latitude))

# Streamlit interface
st.title("Crime Prediction and Reporting")

# Display a map of the crime data
st.subheader("Crime Data Map")
m = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
for idx, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['crime_type']).add_to(m)
folium_static(m)

# Report an incident and save it to the CSV file
st.subheader("Report an Incident")
date = st.date_input("Your Location (latitude, longitude)")
location=st.text_input("Location")
user_location = st.text_input("Your Location (latitude, longitude)")
incident_type = st.selectbox("Incident Type", crime_data['crime_type'].unique())
time=st.text_input("Time")
gender=st.text_input("Victim_Gender")
report_button = st.button("Report")

if report_button:
    # Process the user's report and save it to the CSV file
    if user_location:
        user_location = user_location.split(',')
        if len(user_location) == 2:
            user_latitude, user_longitude = float(user_location[0]), float(user_location[1])

            # Create a new incident report
            new_report = {
                'date':date,
                'latitude': user_latitude,
                'longitude': user_longitude,
                'crime_type': incident_type,
                'time_of_day':time,
                'location':location,
                'victim_gender':gender,
            }

            # Append the report to the existing CSV file
            crime_data = pd.concat([crime_data, pd.DataFrame([new_report])], ignore_index=True)
            crime_data.to_csv('crime_data.csv', index=False)  # Save the updated data to the CSV file

            st.success("Incident reported and saved to Dataset.")

# Create a heatmap of crime hotspots
st.subheader("Crime Hotspot Map")
heatmap = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
HeatMapWithTime(data=crime_data[['latitude', 'longitude']].values, radius=15).add_to(heatmap)
folium_static(heatmap)
