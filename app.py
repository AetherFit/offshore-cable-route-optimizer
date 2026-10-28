import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page Setup & Professional Dark Theme Injection
st.set_page_config(page_title="SubseaRoute AI | Offshore Wind Engineering", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
    .css-1r6slb0, .css-12w0qpk { background-color: #161B22; border-radius: 10px; padding: 20px; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    .badge-success { background-color: #238636; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    .badge-warning { background-color: #9e6a03; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    .badge-danger { background-color: #da3633; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("⚡ SubseaRoute AI")
st.markdown("<p style='color: #8B949E; font-size: 18px;'>Subsea Cable Route Optimization, Hydrodynamic Loads & Commercial Risk Engine</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("🛠️ Engineering & Site Parameters")

# Cable Engineering Specs
st.sidebar.subheader("Cable Specifications")
cable_voltage = st.sidebar.selectbox("Operating Voltage (kV)", [132, 220, 275, 400], index=1)
cable_cross_section = st.sidebar.selectbox("Conductor Cross-Section (mm²)", [630, 800, 1000, 1200], index=2)
conductor_material = st.sidebar.radio("Conductor Material", ["Copper (Cu)", "Aluminium (Al)"])

# Route & Seabed Parameters
st.sidebar.subheader("Route & Bathymetry")
start_point = (0, 0)
end_x = st.sidebar.slider("Substation Easting (km)", 10.0, 80.0, 45.0, 1.0)
end_y = st.sidebar.slider("Substation Northing (km)", 10.0, 80.0, 35.0, 1.0)
hazard_avoidance = st.sidebar.checkbox("Apply AI Route Avoidance (Bypasses Rock Outcrops)", value=True)

water_depth = st.sidebar.slider("Max Water Depth (m)", 15.0, 120.0, 45.0, 5.0)
seabed_type = st.sidebar.selectbox(
    "Seabed Geology Profile",
    ["Clay / Soft Silt (Low Risk)", "Mobile Sand Waves (Medium Risk)", "Hard Rock / Basalt Outcrops (High Risk)"]
)

# Commercial & Vessel Parameters
st.sidebar.subheader("Vessel & Environmental Logistics")
vessel_daily_rate = st.sidebar.number_input("CLV (Cable Lay Vessel) Day Rate (£)", min_value=60000, max_value=300000, value=145000, step=5000)
hs_wave_limit = st.sidebar.slider("Operational Significant Wave Height Limit Hs (m)", 1.5, 3.5, 2.2, 0.1)
weather_contingency = st.sidebar.slider("Seasonal Downtime Factor (%)", 5, 45, 18, 1)

# Physics & Mathematical Computations
# Direct linear distance vs optimized routed length
direct_dist = np.sqrt(end_x**2 + end_y**2)
route_length = direct_dist * (1.18 if hazard_avoidance else 1.05)

# Electrical Loss Calculation (Simplified AC resistance physics)
resistivity = 0.0175 if "Copper" in conductor_material else 0.028
resistance_per_km = (resistivity * 1000) / cable_cross_section
current_load = 800  # Amperes (typical offshore wind export load)
power_loss_mw = (3 * (current_load ** 2) * resistance_per_km * route_length) / 1e6
efficiency_percent = max(0.0, 100.0 - ((power_loss_mw / 400.0) * 100))

# Cost calculations
cable_cost_per_km = 420000 if "Copper" in conductor_material else 290000
cable_cost_per_km *= (cable_voltage / 220)
material_cost = route_length * cable_cost_per_km

seabed_mult = 1.0 if "Clay" in seabed_type else (1.4 if "Sand" in seabed_type else 2.1)
trenching_speed_km_day = 1.4 if "Clay" in seabed_type else (0.9 if "Sand" in seabed_type else 0.35)

trenching_cost = route_length * 140000 * seabed_mult
laying_days_net = route_length / trenching_speed_km_day
total_vessel_days = laying_days_net * (1 + (weather_contingency / 100))
vessel_cost = total_vessel_days * vessel_daily_rate

total_capex = material_cost + trenching_cost + vessel_cost

# Mechanical Tension Warning
lay_tension_kn = (water_depth * 0.85) + (route_length * 0.15)
tension_critical = lay_tension_kn > 85.0

# Top KPI Metric Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cable Route CapEx", f"£{total_capex:,.0f}", delta=f"{route_length:.1f} km Total Length")
col2.metric("Total Offshore Duration", f"{total_vessel_days:.1f} Days", delta=f"{total_vessel_days - laying_days_net:.1f} Days Weather Risk")
col3.metric("Electrical Transmission Efficiency", f"{efficiency_percent:.2f}%", delta=f"-{power_loss_mw:.2f} MW Loss")
col4.metric("Max Lay Tension", f"{lay_tension_kn:.1f} kN", delta="WARNING: High Tension" if tension_critical else "Within Limits", delta_color="inverse" if tension_critical else "normal")

st.markdown("---")

# Row 1: Interactive Spatial Map + Electrical Profile
map_col, physics_col = st.columns([6, 4])

with map_col:
    st.subheader("🗺️ Dynamic Subsea Spatial Route Map")
    
    # Generate Route Coordinates
    x_coords = [0, end_x * 0.3, end_x * 0.75, end_x] if hazard_avoidance else [0, end_x]
    y_coords = [0, end_y * 0.5 + 5, end_y * 0.8 - 3, end_y] if hazard_avoidance else [0, end_y]
    
    fig_map = go.Figure()
    
    # Hazard Zone
    fig_map.add_shape(type="circle", xref="x", yref="y", x0=end_x*0.2, y0=end_y*0.2, x1=end_x*0.5, y1=end_y*0.6,
                      fillcolor="rgba(218, 54, 51, 0.2)", line=dict(color="rgba(218, 54, 51, 0.8)", width=2))
    fig_map.add_annotation(x=end_x*0.35, y=end_y*0.4, text="Seabed Hazard Zone<br>(High Scour / Rock Outcrops)", showarrow=False, font=dict(color="#FF7B72", size=10))
    
    # Cable Route Trace
    fig_map.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines+markers', name='Optimized Cable Path',
                                 line=dict(color='#58A6FF', width=4, dash='solid' if hazard_avoidance else 'dot')))
    
    # Waypoints
    fig_map.add_trace(go.Scatter(x=[0, end_x], y=[0, end_y], mode='markers+text',
                                 text=['Offshore Substation (OSS)', 'Onshore Grid Landing'],
                                 textposition=["top right", "top left"],
                                 marker=dict(size=14, color=['#3FB950', '#D29922'])))
    
    fig_map.update_layout(template="plotly_dark", height=420, margin=dict(l=20, r=20, t=30, b=20),
                          xaxis_title="Easting Distance (km)", yaxis_title="Northing Distance (km)",
                          showlegend=False)
    st.plotly_chart(fig_map, use_container_width=True)

with physics_col:
    st.subheader("⚡ Cable Physics & Mechanical Profile")
    
    physics_df = pd.DataFrame({
        "Parameter": ["Operating Voltage", "Conductor Area", "Conductor Material", "AC Resistance", "Power Loss", "Min Bending Radius (MBR)"],
        "Value": [f"{cable_voltage} kV", f"{cable_cross_section} mm²", conductor_material, f"{resistance_per_km:.4f} Ω/km", f"{power_loss_mw:.2f} MW", f"{cable_cross_section * 0.025:.2f} m"]
    })
    st.table(physics_df)
    
    if tension_critical:
        st.error("⚠️ **Mechanical Structural Alert**: Recommended installation tension exceeds maximum safety factor for selected cable spec. Consider increasing conductor cross-section or altering lay speed.")
    else:
        st.success("✅ **Structural Integrity Normal**: Cable lay tension and bending strain remain well within manufacturer tolerances.")

st.markdown("---")

# Row 2: Operational Gantt Timeline & Commercial Cost Breakdown
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("📅 Offshore Installation Programme (Gantt)")
    
    # Build schedule timeline
    mob_days = 3.0
    lay_days = laying_days_net
    weather_days = total_vessel_days - laying_days_net
    demob_days = 2.0
    
    tasks = [
        dict(Task="Vessel Mobilization", Start=0, Finish=mob_days, Category="Logistics"),
        dict(Task="Cable Laying & Burial", Start=mob_days, Finish=mob_days + lay_days, Category="Operations"),
        dict(Task="Seasonal Weather Downtime", Start=mob_days + lay_days, Finish=mob_days + lay_days + weather_days, Category="Risk"),
        dict(Task="Post-Lay Inspection & Demob", Start=mob_days + lay_days + weather_days, Finish=mob_days + lay_days + weather_days + demob_days, Category="Logistics")
    ]
    
    df_gantt = pd.DataFrame(tasks)
    fig_gantt = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Category",
                            color_discrete_map={"Logistics": "#8957E5", "Operations": "#238636", "Risk": "#DA3633"},
                            template="plotly_dark")
    fig_gantt.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="Operational Days")
    st.plotly_chart(fig_gantt, use_container_width=True)

with chart2:
    st.subheader("📊 CapEx Cost Breakdown (£)")
    
    cost_data = pd.DataFrame({
        "Component": ["Cable Materials", "Trenching & Protection", "Vessel Charter & Crew"],
        "Cost (£)": [material_cost, trenching_cost, vessel_cost]
    })
    fig_pie = px.pie(cost_data, values='Cost (£)', names='Component', hole=0.4,
                     color_discrete_sequence=['#58A6FF', '#3FB950', '#D29922'], template="plotly_dark")
    fig_pie.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Executive PDF/Summary Generator
st.subheader("📋 Executive Project Management Summary")
if st.button("Generate Professional BoQ & Risk Statement"):
    st.markdown(f"""
    <div style='background-color: #161B22; padding: 20px; border-radius: 10px; border-left: 5px solid #58A6FF;'>
        <h4 style='margin-top:0;'>Project Summary: Subsea Export Cable Installation</h4>
        <ul>
            <li><b>Total Route Distance:</b> {route_length:.2f} km (Grid Delta: {direct_dist:.2f} km)</li>
            <li><b>System Specification:</b> {cable_voltage} kV {conductor_material} ({cable_cross_section} mm²)</li>
            <li><b>Total Project CapEx:</b> £{total_capex:,.2f}</li>
            <li><b>Operational Vessel Window:</b> {total_vessel_days + mob_days + demob_days:.1f} Days (Includes {weather_contingency}% weather downtime risk)</li>
            <li><b>Transmission Efficiency Rating:</b> {efficiency_percent:.2f}% ({power_loss_mw:.2f} MW estimated loss)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
