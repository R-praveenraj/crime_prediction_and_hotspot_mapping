import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Load crime data
crime_data = pd.read_csv("crime.csv")
crime_gdf = gpd.GeoDataFrame(crime_data, geometry=gpd.points_from_xy(crime_data.longitude, crime_data.latitude))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        location = request.form["location"]

        geolocator = Nominatim(user_agent="crime_detection_app")
        location_info = geolocator.geocode(location)
        if location_info:
            latitude, longitude = location_info.latitude, location_info.longitude

            filtered_crimes = crime_gdf[(crime_gdf["date"] == date) & (crime_gdf["latitude"] == latitude) & (crime_gdf["longitude"] == longitude)]
            if not filtered_crimes.empty:
                m = folium.Map(location=[latitude, longitude], zoom_start=15)
                for idx, row in filtered_crimes.iterrows():
                    popup_text = f"Date: {row['date']}<br>Location: {row['location']}<br>Crime Type: {row['crime_type']}<br>Previous Activity: {row['previous_activity']}"
                    folium.Marker([row["latitude"], row["longitude"]], popup=popup_text).add_to(m)

                result_html = os.path.join(app.root_path, 'templates', 'map.html')
                m.save(result_html)
                return redirect(url_for('show_map'))

    return render_template("index.html")

@app.route("/map")
def show_map():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
