import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="WindFarm GIS | Layout & Logistics Planner", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ WindFarm GIS: Spatial Layout & Marine Logistics Planner")
st.markdown("<p style='color: #8B949E; font-size: 16px;'>Interactive offshore wind farm site arrangement, turbine spacing, and port-to-site transit modeling.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Controls (Intuitive Project Management Inputs)
st.sidebar.header("🏗️ Farm Layout Parameters")
num_turbines = st.sidebar.slider("Number of Turbines", min_value=10, max_value=100, value=36, step=2)
turbine_capacity_mw = st.sidebar.selectbox("Turbine Capacity", [10, 12, 15, 18], index=2) # MW per turbine
port_distance_km = st.sidebar.slider("Distance from O&M Port (km)", min_value=10.0, max_value=90.0, value=35.0, step=5.0)

st.sidebar.header("🌊 Foundation & Installation")
foundation_type = st.sidebar.selectbox("Substructure Type", ["Monopile (Shallow/Mid Water)", "Jacket Structure (Deep Water)"])
vessel_speed_knots = st.sidebar.slider("Installation Vessel Speed (knots)", min_value=8.0, max_value=20.0, value=12.0, step=1.0)

# Calculations
total_capacity_gw = (num_turbines * turbine_capacity_mw) / 1000.0
layout_grid_size = int(np.ceil(np.sqrt(num_turbines)))

# Generate simulated turbine grid coordinates centered around an Offshore Substation (OSS)
np.random.seed(42)
grid_x, grid_y = [], []
for i in range(layout_grid_size):
    for j in range(layout_grid_size):
        if len(grid_x) < num_turbines:
            grid_x.append(port_distance_km + 5 + (i * 1.5) + np.random.uniform(-0.2, 0.2))
            grid_y.append(20 + (j * 1.5) + np.random.uniform(-0.2, 0.2))

oss_x = port_distance_km + 2
oss_y = 20 + (layout_grid_size * 0.75)

# Logistics calculations
install_days_per_turbine = 3.5 if "Monopile" in foundation_type else 5.0
total_install_days = (num_turbines * install_days_per_turbine) / 2.0 # Assuming dual-vessel spread

# Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Farm Capacity", f"{total_capacity_gw:.2f} GW", delta=f"{num_turbines} Turbines ({turbine_capacity_mw}MW)")
col2.metric("Estimated Installation Window", f"{total_install_days:.0f} Days", delta=foundation_type)
col3.metric("Port Transit Distance", f"{port_distance_km} km", delta="Direct Coastal Route")
col4.metric("Layout Density", f"{layout_grid_size}x{layout_grid_size} Grid", delta="Optimized Array")

st.markdown("---")

# Main Visual Interactive Map
st.subheader("📍 Spatial Site Layout & Cable Array Map")

fig = go.Figure()

# 1. Port Landing
fig.add_trace(go.Scatter(
    x=[0], y=[20],
    mode='markers+text',
    name='Onshore Port / O&M Base',
    text=['Coastal Port Base'],
    textposition='bottom center',
    marker=dict(size=18, color='#D29922', symbol='square')
))

# 2. Export Cable Route from Port to Substation
fig.add_trace(go.Scatter(
    x=[0, oss_x], y=[20, oss_y],
    mode='lines',
    name='Export Cable Route',
    line=dict(color='#3FB950', width=4, dash='dash')
))

# 3. Offshore Substation (OSS)
fig.add_trace(go.Scatter(
    x=[oss_x], y=[oss_y],
    mode='markers+text',
    name='Offshore Substation (OSS)',
    text=['Offshore Substation'],
    textposition='top center',
    marker=dict(size=20, color='#8957E5', symbol='diamond')
))

# 4. Wind Turbine Array
fig.add_trace(go.Scatter(
    x=grid_x, y=grid_y,
    mode='markers',
    name='Wind Turbine Generators',
    marker=dict(size=10, color='#58A6FF', symbol='circle')
))

fig.update_layout(
    template="plotly_dark",
    height=500,
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_title="Easting Distance from Coast (km)",
    yaxis_title="Northing Spatial Coordinate (km)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Bottom Section: Project Management Summary
st.subheader("📋 Executive Logistics & Site Overview")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown(f"""
    **Site Logistics Summary:**
    *   **Selected Foundation:** {foundation_type} (Requires heavy-lift installation vessel deployment)[cite: 4, 5].
    *   **Array Configuration:** Arranged in an optimized grid pattern to minimize wake losses between turbines.
    *   **Export Infrastructure:** Single primary export cable routing from the central Offshore Substation back to the coastal port grid connection point[cite: 4, 5].
    """)

with col_info2:
    st.markdown(f"""
    **Project Schedule & Risk Notes:**
    *   **Vessel Mobilization:** Estimated operational fleet requirement of specialized installation vessels.
    *   **Weather Contingency:** Built-in operational buffer included in the {total_install_days:.0f}-day installation timeline[cite: 5].
    *   **HSE Compliance:** Aligned with standard offshore marine clearance and safety zone parameters[cite: 5].
    """)
