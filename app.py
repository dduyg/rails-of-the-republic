import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd

# Load data
railways = gpd.read_file("data/synthetic_railways.geojson")
regions = gpd.read_file("data/synthetic_regions.geojson")

st.set_page_config(layout="wide")
st.title("🚂 Rails of the Republic")
st.subheader("How Railway Development Embodied Kemalist Ideology")

# Sidebar filters
ideologies = railways["ideology_tag"].unique().tolist()
selected_ideologies = st.sidebar.multiselect("Select Ideological Tags", ideologies, default=ideologies)

# Filter data
filtered_railways = railways[railways["ideology_tag"].isin(selected_ideologies)]

# Base map
m = folium.Map(location=[39.0, 35.5], zoom_start=6)

# Add railway lines
color_map = {"Halkçılık": "green", "Devletçilik": "blue", "Yabancı sermaye": "red"}
for _, row in filtered_railways.iterrows():
    coords = list(row.geometry.coords)
    folium.PolyLine(coords, color=color_map.get(row.ideology_tag, "gray"), weight=5,
                    tooltip=f"{row['name']} ({row['year_built']}) - {row['ideology_tag']}").add_to(m)

# Add region literacy bubbles
for _, row in regions.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=(row.literacy_1938 - row.literacy_1923) / 2,
        popup=(f"{row['region']}<br>"
               f"Literacy 1923: {row['literacy_1923']}%<br>"
               f"Literacy 1938: {row['literacy_1938']}%"),
        color='orange',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

# Render map
st_data = st_folium(m, width=1000, height=600)

# Region comparison
selected_region = st.selectbox("Compare Literacy in a Region", regions["region"])
region_data = regions[regions["region"] == selected_region].iloc[0]
st.write(f"📘 **{selected_region} Literacy Rates**")
st.metric("1923", f"{region_data['literacy_1923']}%")
st.metric("1938", f"{region_data['literacy_1938']}%")
