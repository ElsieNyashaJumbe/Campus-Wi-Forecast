# Generate a realistic 500-row WiFi usage dataset and a simple Streamlit dashboard app

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

rows = 500

hours = np.random.randint(7, 22, rows)  # campus active hours
days = np.random.choice(
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], 
    rows, 
    p=[0.18,0.18,0.18,0.18,0.18,0.05,0.05]
)
locations = np.random.choice(
    ["Library","LectureHall","Hostel","Cafeteria","Lab"], 
    rows, 
    p=[0.3,0.25,0.25,0.1,0.1]
)
exam_period = np.random.choice([0,1], rows, p=[0.85,0.15])

# Base usage influenced by location
location_base = {
    "Library": 220,
    "LectureHall": 180,
    "Hostel": 200,
    "Cafeteria": 120,
    "Lab": 150
}

# Peak hours multiplier
def hour_multiplier(h):
    if 11 <= h <= 14:  # lunch / peak study time
        return 1.6
    elif 17 <= h <= 20:  # evening usage
        return 1.4
    elif 8 <= h <= 10:  # morning classes
        return 1.2
    else:
        return 0.9

users = []
for i in range(rows):
    base = location_base[locations[i]]
    mult = hour_multiplier(hours[i])
    exam_boost = 1.3 if exam_period[i] == 1 else 1.0
    noise = np.random.normal(0, 20)
    
    val = int(max(30, base * mult * exam_boost + noise))
    users.append(val)

df = pd.DataFrame({
    "hour": hours,
    "day": days,
    "location": locations,
    "exam_period": exam_period,
    "users_connected": users
})

data_path = "/mnt/data/wifi_usage_500rows.csv"
df.to_csv(data_path, index=False)

# Create a simple Streamlit dashboard
dashboard_code = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Campus WiFi Usage Dashboard")

data = pd.read_csv("wifi_usage_500rows.csv")

st.subheader("Dataset Preview")
st.write(data.head())

location = st.selectbox("Select Location", data["location"].unique())
filtered = data[data["location"] == location]

st.subheader("WiFi Usage by Hour")
hourly = filtered.groupby("hour")["users_connected"].mean().reset_index()

fig, ax = plt.subplots()
ax.plot(hourly["hour"], hourly["users_connected"])
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Average Users Connected")
ax.set_title(f"Average WiFi Usage at {location}")
st.pyplot(fig)

st.subheader("Peak Usage Insight")
peak_hour = hourly.loc[hourly["users_connected"].idxmax(), "hour"]
st.write(f"Peak WiFi usage at **{location}** occurs around **{int(peak_hour)}:00**.")
"""

dashboard_path = "/mnt/data/dashboard.py"
Path(dashboard_path).write_text(dashboard_code)

data_path, dashboard_path