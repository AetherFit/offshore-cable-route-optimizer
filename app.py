import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="UK Infrastructure & Energy GIS Explorer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ UK Infrastructure & Renewable Energy GIS Explorer")
st.markdown("<p style='color: #8B949E; font-size: 16px;'>Interactive spatial mapping and filtering of UK renewable assets, ports, and regional infrastructure.</p>", unsafe_allow_html=True)
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

# Interactive Spatial Coordinate Map (Bulletproof on Cloud)
st.subheader("📍 Live UK Spatial Map")

# Fallback sizing if capacity is 0
size_val = filtered_df["Capacity_MW"].apply(lambda x: 18 if x == 0 else max(10, x / 150))

fig = px.scatter(
    filtered_df,
    x="Lon",
    y="Lat",
    color="Type",
    hover_name="Name",
    size=size_val,
    size_max=22,
    template="plotly_dark",
    hover_data=["Capacity_MW", "Details"],
    labels={"Lon": "Longitude (East / West)", "Lat": "Latitude (North / South)"}
)

fig.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=30, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=True, zeroline=False, gridcolor="#30363D"),
    yaxis=dict(showgrid=True, zeroline=False, gridcolor="#30363D")
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Bottom Section: Asset Table Directory
st.subheader("📋 Infrastructure Asset Directory")
st.dataframe(filtered_df[["Name", "Type", "Capacity_MW", "Details"]], use_container_width=True)
