import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(page_title="Global Offshore Wind & Energy GIS Explorer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Global Offshore Wind & Infrastructure GIS Explorer")
st.markdown("<p style='color: #8B949E; font-size: 16px;'>Interactive global spatial mapping of major international offshore wind farms, renewable assets, and port hubs.</p>", unsafe_allow_html=True)
st.markdown("---")

# Global open-source dataset representing major international offshore wind assets and ports
data = [
    # United Kingdom & Europe
    {"Name": "Dogger Bank Wind Farm", "Lat": 54.8000, "Lon": 2.0000, "Region": "Europe", "Type": "Offshore Wind", "Capacity_MW": 3600, "Details": "World's largest utility-scale offshore wind development in the North Sea (UK)."},
    {"Name": "Hornsea Two", "Lat": 53.9300, "Lon": 1.8500, "Region": "Europe", "Type": "Offshore Wind", "Capacity_MW": 1382, "Details": "Massive operational North Sea wind asset off the Yorkshire coast (UK)."},
    {"Name": "Borssele Wind Farm", "Lat": 51.7000, "Lon": 3.0500, "Region": "Europe", "Type": "Offshore Wind", "Capacity_MW": 1500, "Details": "Major Dutch North Sea offshore energy installation (Netherlands)."},
    {"Name": "Walney Extension", "Lat": 54.0500, "Lon": -3.5200, "Region": "Europe", "Type": "Offshore Wind", "Capacity_MW": 659, "Details": "Irish Sea high-capacity offshore wind farm (UK)."},
    {"Name": "Avonmouth / Bristol Port Hub", "Lat": 51.4881, "Lon": -2.6917, "Region": "Europe", "Type": "Port & Logistics", "Capacity_MW": 0, "Details": "Key regional import and fabrication hub for South West marine engineering."},
    {"Name": "Port of Rotterdam", "Lat": 51.9244, "Lon": 4.4777, "Region": "Europe", "Type": "Port & Logistics", "Capacity_MW": 0, "Details": "Europe's largest port handling heavy offshore construction logistics."},
    
    # Asia-Pacific
    {"Name": "Yangjiang Offshore Wind Farm", "Lat": 21.8500, "Lon": 111.9700, "Region": "Asia-Pacific", "Type": "Offshore Wind", "Capacity_MW": 2000, "Details": "Utility-scale multi-gigawatt coastal wind complex in Guangdong (China)."},
    {"Name": "Jiangsu Qidong Project", "Lat": 31.8100, "Lon": 121.6500, "Region": "Asia-Pacific", "Type": "Offshore Wind", "Capacity_MW": 800, "Details": "Major East China Sea offshore energy installation."},
    {"Name": "Formosa 2 Wind Farm", "Lat": 24.6000, "Lon": 120.7500, "Region": "Asia-Pacific", "Type": "Offshore Wind", "Capacity_MW": 376, "Details": "Commercial-scale strait crossing offshore wind farm (Taiwan)."},
    
    # North America
    {"Name": "Coastal Virginia Offshore Wind", "Lat": 36.9000, "Lon": -75.4000, "Region": "Americas", "Type": "Offshore Wind", "Capacity_MW": 2600, "Details": "Major commercial utility-scale wind development off the US East Coast."},
    {"Name": "Block Island Wind Farm", "Lat": 41.2800, "Lon": -71.5200, "Region": "Americas", "Type": "Offshore Wind", "Capacity_MW": 30, "Details": "Pioneering first commercial offshore wind farm in the United States."},
]

df = pd.DataFrame(data)

# Sidebar Filters
st.sidebar.header("🔍 Global GIS Filters")
selected_region = st.sidebar.selectbox("Filter Region", ["All Regions", "Europe", "Asia-Pacific", "Americas"])
selected_type = st.sidebar.selectbox("Filter Asset Category", ["All Categories", "Offshore Wind", "Port & Logistics"])
min_capacity = st.sidebar.slider("Minimum Capacity (MW)", 0, 4000, 0, 100)

# Apply filters
filtered_df = df.copy()
if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_type != "All Categories":
    filtered_df = filtered_df[filtered_df["Type"] == selected_type]
filtered_df = filtered_df[filtered_df["Capacity_MW"] >= min_capacity]

# Top Metrics Bar
col1, col2, col3 = st.columns(3)
col1.metric("Global Assets Mapped", len(filtered_df))
col2.metric("Total Filtered Capacity", f"{filtered_df['Capacity_MW'].sum():,} MW")
col3.metric("Scope", "Global Maritime Infrastructure")

st.markdown("---")

# Global Interactive Map Section
st.subheader("📍 Live Global GIS Map")

# Initialize Folium map centered globally with a standard open-source tile layer
m = folium.Map(location=[25.0, 10.0], zoom_start=2, tiles="OpenStreetMap")

# Color mapping for pins based on asset type
color_map = {
    "Offshore Wind": "blue",
    "Port & Logistics": "orange"
}

# Add markers dynamically from filtered data
for idx, row in filtered_df.iterrows():
    color = color_map.get(row["Type"], "red")
    popup_html = f"""
    <div style='font-family: sans-serif; color: #000; width: 220px;'>
        <h4 style='margin:0; color:#0366d6;'>{row['Name']}</h4>
        <p style='margin:4px 0;'><b>Region:</b> {row['Region']}</p>
        <p style='margin:4px 0;'><b>Category:</b> {row['Type']}</p>
        <p style='margin:4px 0;'><b>Capacity:</b> {row['Capacity_MW']} MW</p>
        <p style='margin:4px 0; font-size:11px;'>{row['Details']}</p>
    </div>
    """
    folium.Marker(
        location=[row["Lat"], row["Lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=row["Name"],
        icon=folium.Icon(color=color, icon="globe", prefix='glyphicon')
    ).add_to(m)

# Render the map inside Streamlit
st_folium(m, width=1200, height=550, use_container_width=True)

st.markdown("---")

# Bottom Section: Global Asset Directory
st.subheader("📋 International Infrastructure Directory")
st.dataframe(filtered_df[["Name", "Region", "Type", "Capacity_MW", "Details"]], use_container_width=True)
