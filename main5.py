import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from sklearn.cluster import KMeans

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

# Report an incident and save it to the CSV file (code omitted for brevity)

# Create a heatmap of crime hotspots (code omitted for brevity)

# Predict major possible crime occurrence areas using K-Means clustering
st.subheader("Major Possible Crime Occurrence Areas")
k = st.slider("Number of Clusters", 1, 10, 3)  # Adjust the number of clusters
kmeans = KMeans(n_clusters=k, random_state=0)
crime_data['cluster'] = kmeans.fit_predict(crime_data[['latitude', 'longitude']])
clustered_map = folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)

# Generate color-coded clusters on the map
for cluster in crime_data['cluster'].unique():
    cluster_data = crime_data[crime_data['cluster'] == cluster]
    color = "#{:02x}{:02x}{:02x}".format(int(255 * (cluster / k)), 0, 0)  # Adjust colors as needed
    for idx, row in cluster_data.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=5,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=f"Cluster {cluster}").add_to(clustered_map)

folium_static(clustered_map)

# Location Data Table
st.subheader("Location Data Table")
st.write(crime_data[['latitude', 'longitude', 'crime_type', 'cluster']])
