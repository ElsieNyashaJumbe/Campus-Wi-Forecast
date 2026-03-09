
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
