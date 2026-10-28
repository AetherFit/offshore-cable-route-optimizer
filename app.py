import streamlit as st
import pandas as pd
import numpy as np

# App Title & Configuration
st.set_page_config(page_title="SubseaRoute AI | Offshore Cable Routing & Risk Simulator", layout="wide")

st.title("⚡ SubseaRoute AI")
st.markdown("### Offshore Wind Subsea Cable Routing, Cost, & Risk Optimization Utility")
st.markdown("---")

# Sidebar Controls for Engineering & Project Parameters
st.sidebar.header("Marine & Engineering Inputs")

route_length = st.sidebar.slider("Cable Route Length (km)", min_value=5.0, max_value=100.0, value=25.0, step=1.0)
water_depth = st.sidebar.slider("Average Water Depth (m)", min_value=10.0, max_value=80.0, value=35.0, step=5.0)

seabed_type = st.sidebar.selectbox(
    "Seabed Geology Profile",
    ["Clay / Soft Silt (Low Risk)", "Mobile Sand Waves (Medium Risk)", "Hard Rock / Outcrops (High Risk)"]
)

vessel_daily_rate = st.sidebar.number_input("Vessel Daily Charter Rate (£)", min_value=50000, max_value=250000, value=120000, step=5000)
weather_risk = st.sidebar.slider("Weather Downtime Contingency (%)", min_value=5, max_value=40, value=15, step=1)

# Assign multipliers based on seabed selection
if "Clay" in seabed_type:
    seabed_multiplier = 1.0
    trench_speed_km_day = 1.2
    risk_score_base = 20
elif "Sand" in seabed_type:
    seabed_multiplier = 1.35
    trench_speed_km_day = 0.8
    risk_score_base = 50
else:  # Hard Rock
    seabed_multiplier = 1.85
    trench_speed_km_day = 0.4
    risk_score_base = 80

# Calculation Logic
base_cable_cost_per_km = 350000  # £350k per km of subsea high-voltage cable
material_cost = route_length * base_cable_cost_per_km

# Installation & Vessel calculations
base_trenching_cost_per_km = 120000
trenching_cost = route_length * base_trenching_cost_per_km * seabed_multiplier

# Vessel days calculation factoring speed and weather contingency
effective_laying_speed = trench_speed_km_day * (1 - (weather_risk / 100))
vessel_days = route_length / effective_laying_speed
vessel_charter_cost = vessel_days * vessel_daily_rate

# Total CapEx
total_capex = material_cost + trenching_cost + vessel_charter_cost

# Overall Risk Score (0-100)
total_risk_score = min(int(risk_score_base + (weather_risk * 0.5) + (water_depth * 0.1)), 100)

# --- Main Dashboard Display ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Estimated CapEx", f"£{total_capex:,.0f}")
col2.metric("Estimated Vessel Days", f"{vessel_days:.1f} Days")
col3.metric("Composite Risk Score", f"{total_risk_score} / 100")
col4.metric("Cable Material Cost", f"£{material_cost:,.0f}")

st.markdown("---")

# Visual Breakdown Charts
st.subheader("📊 Capital Expenditure (CapEx) & Schedule Breakdown")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Cost Distribution (£)")
    cost_data = pd.DataFrame({
        "Cost Category": ["Cable Materials", "Trenching & Burial", "Vessel Charter"],
        "Amount (£)": [material_cost, trenching_cost, vessel_charter_cost]
    })
    st.bar_chart(cost_data.set_index("Cost Category"))

with chart_col2:
    st.markdown("#### Operational Risk Factors")
    risk_factors = pd.DataFrame({
        "Parameter": ["Seabed Geology", "Weather Downtime", "Water Depth Constraints"],
        "Risk Impact (%)": [risk_score_base, weather_risk * 2, int(water_depth)]
    })
    st.bar_chart(risk_factors.set_index("Parameter"))

st.markdown("---")

# Executive Summary & Bill of Quantities Generation
st.subheader("📑 Executive Project Management Summary & BoQ")

if st.button("Generate Formal Engineering Report"):
    st.success("Report generated successfully!")
    
    report_text = f"""
    ### SubseaRoute AI - Executive Engineering Report
    - **Route Length:** {route_length} km
    - **Seabed Classification:** {seabed_type}
    - **Water Depth:** {water_depth} m
    - **Total Project CapEx:** £{total_capex:,.2f}
    - **Required Vessel Time:** {vessel_days:.1f} operational days
    - **HSE & Environmental Risk Rating:** {'HIGH' if total_risk_score > 60 else 'MODERATE' if total_risk_score > 35 else 'LOW'} ({total_risk_score}/100)
    """
    st.markdown(report_text)