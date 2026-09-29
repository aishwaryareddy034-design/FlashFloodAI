import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="FlashFlood AI",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1.5rem;
}

.title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    font-size: 17px;
    color: #5f6368;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background: white;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

.metric-title {
    font-size: 14px;
    color: #64748b;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
}

.warning {
    padding: 20px;
    border-radius: 12px;
    background-color: #fff4f4;
    border-left: 6px solid #d32f2f;
}

.safe {
    padding: 20px;
    border-radius: 12px;
    background-color: #f0fff4;
    border-left: 6px solid #2e7d32;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🌧️ FlashFlood AI")

st.sidebar.write(
    "AI-Based Flash Flood Prediction System "
    "for Hilly Regions"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Dashboard",
        "🤖 Flood Prediction",
        "🗺️ Risk Map",
        "🚨 Alerts",
        "📡 Data Sources",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption("SIH Problem Statement: 26192")
st.sidebar.caption("Prototype Version 1.0")

# ---------------------------------------------------------
# PREDICTION FUNCTION
# ---------------------------------------------------------

def calculate_risk(rainfall, river_level, soil_moisture, slope, rain_duration):

    score = 0

    # Rainfall
    if rainfall >= 100:
        score += 35
    elif rainfall >= 70:
        score += 28
    elif rainfall >= 40:
        score += 18
    else:
        score += 8

    # River level
    if river_level >= 5:
        score += 25
    elif river_level >= 4:
        score += 20
    elif river_level >= 3:
        score += 12
    else:
        score += 5

    # Soil moisture
    if soil_moisture >= 85:
        score += 20
    elif soil_moisture >= 70:
        score += 15
    elif soil_moisture >= 50:
        score += 10
    else:
        score += 5

    # Slope
    if slope >= 35:
        score += 15
    elif slope >= 25:
        score += 10
    elif slope >= 15:
        score += 6
    else:
        score += 3

    # Rain duration
    if rain_duration >= 5:
        score += 10
    elif rain_duration >= 3:
        score += 7
    else:
        score += 3

    # Maximum score approximately 105
    probability = min(int(score * 0.95), 99)

    if probability >= 80:
        risk = "CRITICAL"
    elif probability >= 60:
        risk = "HIGH"
    elif probability >= 35:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return probability, risk


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="title">🌧️ FlashFlood AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Based Flash Flood Prediction System for Hilly Regions'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns([1.4, 1])

    with col1:

        st.header("Predict Before Disaster Strikes")

        st.write(
            """
            Flash floods in hilly regions can develop rapidly because of
            intense rainfall, steep slopes, saturated soil and sudden
            increases in river or stream levels.

            **FlashFlood AI** combines multiple environmental parameters
            to estimate the flash-flood risk of a selected region.
            """
        )

        st.info(
            "The current version is a demonstration prototype using "
            "simulated environmental data."
        )

        st.markdown("### Key Features")

        st.write("🌧️ Rainfall monitoring")
        st.write("🌊 River-level monitoring")
        st.write("🌱 Soil-moisture analysis")
        st.write("⛰️ Terrain and slope analysis")
        st.write("🗺️ Flood-risk visualization")
        st.write("🚨 Early-warning alerts")

    with col2:

        st.markdown(
            """
            <div class="card">
            <h3>Multi-Source Data</h3>
            <p>Weather</p>
            <p>Rainfall</p>
            <p>River Level</p>
            <p>Soil Moisture</p>
            <p>Satellite Data</p>
            <p>Terrain / DEM</p>
            <p>Historical Flood Records</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Goal: Provide an early indication of flash-flood risk "
            "to support faster disaster response."
        )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

elif page == "📊 Dashboard":

    st.title("📊 Flood Monitoring Dashboard")

    st.caption("Prototype environmental monitoring interface")

    # Demo values
    rainfall = 82
    river_level = 4.8
    soil_moisture = 76
    slope = 38
    rain_duration = 3

    probability, risk = calculate_risk(
        rainfall,
        river_level,
        soil_moisture,
        slope,
        rain_duration
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Rainfall", f"{rainfall} mm/hr")

    with col2:
        st.metric("River Level", f"{river_level} m")

    with col3:
        st.metric("Soil Moisture", f"{soil_moisture}%")

    with col4:
        st.metric("Slope", f"{slope}°")

    with col5:
        st.metric("Flood Probability", f"{probability}%")

    st.markdown("---")

    if risk == "CRITICAL":
        st.error(f"🔴 CURRENT RISK: {risk}")
    elif risk == "HIGH":
        st.warning(f"🟠 CURRENT RISK: {risk}")
    elif risk == "MODERATE":
        st.warning(f"🟡 CURRENT RISK: {risk}")
    else:
        st.success(f"🟢 CURRENT RISK: {risk}")

    # Graph
    st.subheader("Rainfall Trend")

    hours = list(range(1, 13))

    rainfall_values = [
        15, 18, 22, 28,
        35, 42, 50, 61,
        68, 75, 79, 82
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hours,
            y=rainfall_values,
            mode="lines+markers",
            name="Rainfall"
        )
    )

    fig.update_layout(
        xaxis_title="Time (hours)",
        yaxis_title="Rainfall (mm/hr)",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Current System Status")

    status1, status2, status3 = st.columns(3)

    with status1:
        st.success("Weather Data\n\nONLINE")

    with status2:
        st.success("River Monitoring\n\nONLINE")

    with status3:
        st.success("Prediction Engine\n\nACTIVE")


# ---------------------------------------------------------
# FLOOD PREDICTION
# ---------------------------------------------------------

elif page == "🤖 Flood Prediction":

    st.title("🤖 Flash Flood Prediction")

    st.write(
        "Enter environmental conditions to estimate the flood-risk level."
    )

    col1, col2 = st.columns(2)

    with col1:

        location = st.selectbox(
            "Select Region",
            [
                "Region A - Hilly Catchment",
                "Region B - Mountain Valley",
                "Region C - River Basin",
                "Region D - High Slope Zone"
            ]
        )

        rainfall = st.slider(
            "Rainfall Intensity (mm/hr)",
            0,
            150,
            70
        )

        rain_duration = st.slider(
            "Rainfall Duration (hours)",
            1,
            12,
            3
        )

        river_level = st.slider(
            "River / Stream Level (m)",
            0.0,
            8.0,
            4.0
        )

    with col2:

        soil_moisture = st.slider(
            "Soil Moisture (%)",
            0,
            100,
            70
        )

        slope = st.slider(
            "Terrain Slope (degrees)",
            0,
            60,
            30
        )

        elevation = st.slider(
            "Elevation (m)",
            100,
            4000,
            1200
        )

    st.markdown("---")

    if st.button(
        "🔍 PREDICT FLOOD RISK",
        use_container_width=True
    ):

        probability, risk = calculate_risk(
            rainfall,
            river_level,
            soil_moisture,
            slope,
            rain_duration
        )

        st.subheader("Prediction Result")

        result1, result2 = st.columns(2)

        with result1:

            st.metric(
                "Predicted Flood Probability",
                f"{probability}%"
            )

        with result2:

            if risk == "CRITICAL":
                st.error(f"🔴 {risk} RISK")

            elif risk == "HIGH":
                st.warning(f"🟠 {risk} RISK")

            elif risk == "MODERATE":
                st.warning(f"🟡 {risk} RISK")

            else:
                st.success(f"🟢 {risk} RISK")

        if risk in ["CRITICAL", "HIGH"]:

            st.markdown(
                f"""
                <div class="warning">

                <h3>⚠️ Early Warning Generated</h3>

                High-risk environmental conditions have been detected
                for <b>{location}</b>.

                <br><br>

                <b>Flood Probability:</b> {probability}%<br>
                <b>Rainfall:</b> {rainfall} mm/hr<br>
                <b>River Level:</b> {river_level} m<br>
                <b>Soil Moisture:</b> {soil_moisture}%<br>
                <b>Slope:</b> {slope}°

                <br><br>

                Recommended action: Increase monitoring and prepare
                appropriate emergency-response measures.

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.success(
                "Current conditions indicate a lower flood risk. "
                "Continue monitoring environmental conditions."
            )


# ---------------------------------------------------------
# RISK MAP
# ---------------------------------------------------------

elif page == "🗺️ Risk Map":

    st.title("🗺️ Flash Flood Risk Map")

    st.write(
        "Prototype map showing risk levels across selected hilly locations."
    )

    # Example coordinates for demonstration only
    map_center = [25.5, 91.8]

    flood_map = folium.Map(
        location=map_center,
        zoom_start=7
    )

    locations = [
        {
            "name": "Zone A",
            "lat": 25.57,
            "lon": 91.88,
            "risk": "CRITICAL",
            "probability": 91
        },
        {
            "name": "Zone B",
            "lat": 25.35,
            "lon": 91.65,
            "risk": "HIGH",
            "probability": 74
        },
        {
            "name": "Zone C",
            "lat": 25.70,
            "lon": 92.00,
            "risk": "MODERATE",
            "probability": 48
        },
        {
            "name": "Zone D",
            "lat": 25.20,
            "lon": 91.95,
            "risk": "LOW",
            "probability": 21
        }
    ]

    colors = {
        "CRITICAL": "red",
        "HIGH": "orange",
        "MODERATE": "beige",
        "LOW": "green"
    }

    for location in locations:

        folium.Marker(
            location=[
                location["lat"],
                location["lon"]
            ],
            popup=(
                f"<b>{location['name']}</b><br>"
                f"Risk: {location['risk']}<br>"
                f"Probability: {location['probability']}%"
            ),
            icon=folium.Icon(
                color=colors[location["risk"]],
                icon="warning-sign"
            )
        ).add_to(flood_map)

    st_folium(
        flood_map,
        width=1100,
        height=550
    )

    st.markdown("---")

    st.write("### Risk Legend")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.success("🟢 LOW")

    with c2:
        st.warning("🟡 MODERATE")

    with c3:
        st.warning("🟠 HIGH")

    with c4:
        st.error("🔴 CRITICAL")


# ---------------------------------------------------------
# ALERTS
# ---------------------------------------------------------

elif page == "🚨 Alerts":

    st.title("🚨 Early Warning Alerts")

    st.write(
        "Prototype alert-management interface."
    )

    st.error(
        "🔴 CRITICAL ALERT — Zone A"
    )

    st.write(
        "High flash-flood probability detected."
    )

    st.write("Probability: **91%**")
    st.write("Rainfall: **105 mm/hr**")
    st.write("River Level: **5.4 m**")

    st.markdown("---")

    st.warning(
        "🟠 HIGH ALERT — Zone B"
    )

    st.write(
        "Rapid increase in rainfall and stream level detected."
    )

    st.write("Probability: **74%**")

    st.markdown("---")

    st.subheader("Alert Recipients")

    st.checkbox(
        "Disaster Management Authority",
        value=True
    )

    st.checkbox(
        "Local Administration",
        value=True
    )

    st.checkbox(
        "Rescue Team",
        value=True
    )

    st.checkbox(
        "Community Warning System",
        value=True
    )

    if st.button(
        "📢 Simulate Emergency Notification",
        use_container_width=True
    ):

        st.success(
            "Prototype notification successfully generated."
        )


# ---------------------------------------------------------
# DATA SOURCES
# ---------------------------------------------------------

elif page == "📡 Data Sources":

    st.title("📡 Multi-Source Data")

    st.write(
        "The proposed system combines different environmental "
        "data sources before generating a flood-risk prediction."
    )

    data = pd.DataFrame({
        "Data Source": [
            "Rainfall",
            "Weather",
            "River Level",
            "Soil Moisture",
            "Satellite",
            "Terrain / DEM",
            "Historical Flood Data"
        ],

        "Purpose": [
            "Measure rainfall intensity",
            "Monitor atmospheric conditions",
            "Track water-level changes",
            "Estimate ground saturation",
            "Observe land and water conditions",
            "Analyse elevation and slope",
            "Train and validate prediction models"
        ],

        "Status": [
            "Connected",
            "Connected",
            "Connected",
            "Simulated",
            "Available",
            "Available",
            "Available"
        ]
    })

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Prediction Pipeline")

    st.code("""
Weather Data
     +
Rainfall Data
     +
River-Level Data
     +
Soil-Moisture Data
     +
Satellite Data
     +
Terrain / DEM
     +
Historical Flood Data
          |
          v
   Data Processing
          |
          v
 Feature Extraction
          |
          v
      AI / ML
          |
          v
 Flood Probability
          |
          v
 Risk Classification
          |
          v
 Early Warning Alert
    """)


# ---------------------------------------------------------
# ABOUT
# ---------------------------------------------------------

elif page == "ℹ️ About":

    st.title("ℹ️ About FlashFlood AI")

    st.subheader(
        "SIH Problem Statement 26192"
    )

    st.write(
        """
        FlashFlood AI is a prototype concept for predicting flash-flood
        risk in hilly regions using multiple environmental data sources.

        The system is designed to combine rainfall, river-level,
        soil-moisture, terrain and other relevant information to
        generate a localized flood-risk estimate.
        """
    )

    st.subheader("Proposed Technology")

    tech = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Pandas",
            "Plotly",
            "Folium",
            "Machine Learning",
            "GIS",
            "Satellite Data"
        ],

        "Role": [
            "Application development",
            "Web dashboard",
            "Data processing",
            "Charts and visualization",
            "Interactive maps",
            "Flood-risk prediction",
            "Spatial analysis",
            "Environmental monitoring"
        ]
    })

    st.dataframe(
        tech,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Prototype disclaimer: This application uses demonstration "
        "data and must not be used for real-world emergency decisions."
    )
