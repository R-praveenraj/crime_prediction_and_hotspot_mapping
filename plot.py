import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load crime data
crime_data = pd.read_csv('crime.csv')

# Convert 'date' column to strings
crime_data['date'] = crime_data['date'].astype(str)

# Convert 'location' column to strings
crime_data['location'] = crime_data['location'].astype(str)

# Plot data
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(crime_data['date'], crime_data['location'], marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel('Location')
ax.set_title('Crime Data')
ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility
fig.tight_layout()  # Adjust layout to prevent labels from being cut off
ax.grid(True)
st.pyplot(fig)  # Display the plot in Streamlit
