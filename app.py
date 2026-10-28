import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(page_title="UK Infrastructure & Energy GIS Explorer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ UK Infrastructure & Renewable Energy GIS Explorer")
st.markdown("<p style='color: #8B949E; font-size: 16px;'>Interactive real map of UK renewable assets, ports, and regional infrastructure.</p>", unsafe_allow_html=True)
st.markdown("---")

# Open-source dataset representing real UK infrastructure nodes
data = [
    {"Name": "Avonmouth / Bristol Port Hub", "Lat": 51.4881, "Lon": -2.6917, "Type": "Port & Logistics", "Capacity_MW": 0, "Details": "Key regional import and fabrication hub for South West marine engineering."},
    {"Name": "Hornsea One (Offshore Wind)", "Lat": 53.8833, "Lon": 1.7833, "Type": "Offshore Wind", "Capacity_MW": 1218, "Details": "One of the world's largest operational offshore wind farms."},
    {"Name": "Dogger Bank Wind Farm", "Lat": 54.8000, "Lon": 2.0000, "Type": "Offshore Wind", "Capacity_MW": 3600, "Details": "Massive multi-phase utility-scale offshore wind development in the North Sea."},
    {"Name": "Barrow Offshore Wind", "Lat": 54.0500, "Lon": -3.2667, "Type": "Offshore Wind", "Capacity_MW": 90, "Details": "Established UK Irish Sea offshore wind asset."},
    {"Name": "Hinkley Point C (Nuclear)", "Lat": 51.2089, "Lon": -3.1292, "Type": "Grid & Baseload", "Capacity_MW": 3200, "Details": "Major low-carbon baseload nuclear construction project in Somerset."},
    {"Name": "Greater Gabbard", "Lat": 52.1750, "Lon": 1.9333, "Type": "Offshore Wind", "Capacity_MW": 504, "Details": "Operational North Sea offshore wind installation."},
    {"Name": "Port of Bristol Marine Terminal", "Lat": 51.4930, "Lon": -2.7100, "Type": "Port & Logistics", "Capacity_MW": 0, "Details": "Handling heavy cargo and supporting local industrial operations."},
]

df = pd.DataFrame(data)

# Sidebar Filters
st.sidebar.header("🔍 GIS Data Filters")
selected_type = st.sidebar.selectbox("Filter Asset Category", ["All Categories", "Offshore Wind", "Port & Logistics", "Grid & Baseload"])
min_capacity = st.sidebar.slider("Minimum Capacity (MW)", 0, 4000, 0, 100)

# Apply filters
filtered_df = df.copy()
if selected_type != "All Categories":
    filtered_df = filtered_df[filtered_df["Type"] == selected_type]
filtered_df = filtered_df[filtered_df["Capacity_MW"] >= min_capacity]

# Top Metrics Bar
col1, col2, col3 = st.columns(3)
col1.metric("Visible Assets on Map", len(filtered_df))
col2.metric("Total Filtered Capacity", f"{filtered_df['Capacity_MW'].sum():,} MW")
col3.metric("Geographic Focus", "United Kingdom & South West")

st.markdown("---")

# Actual Interactive Map Section
st.subheader("📍 Live Interactive UK Map")

# Initialize Folium map centered on the UK with a dark sleek tile theme
m = folium.Map(location=[54.5, -3.5], zoom_start=6, tiles="CartoDB dark_matter")

# Color mapping for pins based on asset type
color_map = {
    "Offshore Wind": "blue",
    "Port & Logistics": "orange",
    "Grid & Baseload": "purple"
}

# Add markers dynamically from filtered data
for idx, row in filtered_df.iterrows():
    color = color_map.get(row["Type"], "red")
    popup_html = f"""
    <div style='font-family: sans-serif; color: #000; width: 200px;'>
        <h4 style='margin:0; color:#0366d6;'>{row['Name']}</h4>
        <p style='margin:5px 0;'><b>Category:</b> {row['Type']}</p>
        <p style='margin:5px 0;'><b>Capacity:</b> {row['Capacity_MW']} MW</p>
        <p style='margin:5px 0; font-size:11px;'>{row['Details']}</p>
    </div>
    """
    folium.Marker(
        location=[row["Lat"], row["Lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=row["Name"],
        icon=folium.Icon(color=color, icon="info-sign", prefix='glyphicon')
    ).add_to(m)

# Render the map inside Streamlit
st_folium(m, width=1200, height=550, use_container_width=True)

st.markdown("---")

# Bottom Section: Asset Table Directory
st.subheader("📋 Infrastructure Asset Directory")
st.dataframe(filtered_df[["Name", "Type", "Capacity_MW", "Details"]], use_container_width=True)
