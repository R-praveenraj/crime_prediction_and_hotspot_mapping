import streamlit as st
import plotly.express as px
import pandas as pd

# Create a Streamlit web app
st.title("Crime Detection App")

# User input for location
location = st.text_input("Enter Location")

# Define a sample data frame (replace this with your data)
data = {
    "latitude": [13.2923988],
    "longitude": [77.7519261],
}
df = pd.DataFrame(data)

# Create a map using Plotly Express
fig = px.scatter_geo(df, lat="latitude", lon="longitude")
fig.update_geos(projection_type="orthographic")

# Add a marker to the map
if location:
    st.write(f"Location: {location}")
    st.plotly_chart(fig)
else:
    st.write("Please enter a location to display on the map.")
