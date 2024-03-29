from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
from folium.plugins import HeatMapWithTime
from twilio.rest import Client

crime_data=pd.read_csv('crime.csv')

gdf=gpd.GeoDataFrame(crime_data, 
geometry=gpd.points_from_xy(crime_data.longitude, crime_data.latitude))

TWILIO_ACCOUNT_SID='AC2776decd32fa03fef35143e82e177b29'
TWILIO_AUTH_TOKEN='4da9dff9e37f98ef56b99de78271226e'
TWILIO_PHONE_NUMBER='+13344630998'
POLICE_PHONE_NUMBER='+919361117846'
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = twilio_client.messages.create(
        body="Emergency: Crime reported!",
        from_=+13344630998,
        to=+919361117846
    )
    st.success("SMS to police sent successfully!")
except Exception as e:
    st.error(f"Error sending SMS: {str(e)}")

st.title("Crime Prediction and Reporting")

st.subheader("Crime Data Map")
m=folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
for idx,row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['crime_type']).add_to(m)
folium_static(m)

st.subheader("Report an Incident")
date=st.date_input("Your Location (latitude, longitude)")
location=st.text_input("Location")
user_location=st.text_input("Your Location (latitude, longitude)")
incident_type=st.selectbox("Incident Type", crime_data['crime_type'].unique())
time=st.text_input("Time")
gender=st.text_input("Victim_Gender")
report_button=st.button("Report")

if report_button:
    if user_location:
        user_location = user_location.split(',')
        if len(user_location) == 2:
            user_latitude, user_longitude = float(user_location[0]), float(user_location[1])
            new_report = {
                'date':date,
                'latitude': user_latitude,
                'longitude': user_longitude,
                'crime_type': incident_type,
                'time_of_day':time,
                'location':location,
                'victim_gender':gender,
            }

            crime_data=pd.concat([crime_data, pd.DataFrame([new_report])], ignore_index=True)
            crime_data.to_csv('crime.csv', index=False)

            st.success("Incident reported and saved to the CSV file.")

st.subheader("Crime Hotspot Map")
heatmap=folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)
HeatMapWithTime(data=crime_data[['latitude', 'longitude']].values, radius=15).add_to(heatmap)
folium_static(heatmap)

st.subheader("Major Possible Crime Occurrence Areas")
k=st.slider("Number of Clusters", 1, 10, 3)
kmeans = KMeans(n_clusters=k, random_state=0)
crime_data['cluster'] = kmeans.fit_predict(crime_data[['latitude', 'longitude']])
clustered_map=folium.Map(location=[crime_data['latitude'].mean(), crime_data['longitude'].mean()], zoom_start=12)

for cluster in crime_data['cluster'].unique():
    cluster_data=crime_data[crime_data['cluster'] == cluster]
    color = "#{:02x}{:02x}{:02x}".format(int(255 * (cluster / k)), 0, 0)
    for idx, row in cluster_data.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=5,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=f"Cluster {cluster}").add_to(clustered_map)

folium_static(clustered_map)

st.subheader("Location Data Table")
st.write(crime_data[['location','latitude', 'longitude', 'crime_type', 'cluster']])


# Assume you have a labeled dataset with 'cluster' as the ground truth labels
X = crime_data[['latitude', 'longitude']]
y_true = crime_data['cluster']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2, random_state=42)

# Train the KMeans model on the training set
kmeans = KMeans(n_clusters=k, random_state=0)
kmeans.fit(X_train)

# Make predictions on the test set
y_pred = kmeans.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate F1 score
f1 = f1_score(y_test, y_pred, average='weighted')

# Calculate recall
recall = recall_score(y_test, y_pred, average='weighted')

# Print the metrics
print("Accuracy:", accuracy)
print("F1 Score:", f1)
print("Recall:", recall)

import matplotlib.pyplot as plt

# Plot actual clusters
plt.scatter(X_test['latitude'], X_test['longitude'], c=y_test, cmap='viridis', s=50, alpha=0.5, label='Actual Clusters')

# Plot predicted clusters
plt.scatter(X_test['latitude'], X_test['longitude'], c=y_pred, cmap='viridis', s=50, marker='s', alpha=0.5, label='Predicted Clusters')

plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Actual vs Predicted Clusters')
plt.legend()
plt.show()

