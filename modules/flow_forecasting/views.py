import streamlit as st
import pandas as pd
import numpy as np
from core.context import context

def simulate_flow_forecast(days, beds, walkins, ambulance, surge, covid):
    forecast = []
    np.random.seed(42)
    for i in range(days):
        date = pd.Timestamp.now() + pd.Timedelta(days=i)
        baseline = walkins * 24 + ambulance + np.random.randint(-8, 8)
        if covid:
            baseline = int(baseline * surge)
        census = np.clip(np.random.normal(baseline, 10), beds * 0.5, beds * 1.5)
        wait_time = np.clip(np.random.normal(45 + census/beds*15, 10), 20, 240)
        forecast.append({
            "Date": date.date(),
            "Predicted_ED_Census": int(census),
            "Bed_Availability": beds - int(census) if beds > census else 0,
            "Mean_Wait_Time_Min": int(wait_time),
            "ED_Occupancy_%": int(census/beds*100)
        })
    return pd.DataFrame(forecast)

def flow_forecasting_ui():
    st.header("ED Flow Forecasting (Enterprise Demo)")
    st.caption("Forecasts patient volumes, waits, and capacity stress. All logic is auditable and exportable.")

    beds = st.number_input("ED Bed Count", 5, 100, 25)
    walkin_rate = st.slider("Walk-in Rate (patients/hr)", 1, 18, 7)
    ambulance = st.slider("Ambulance Arrivals (per day)", 0, 40, 8)
    covid_surge = st.checkbox("Pandemic Surge Mode", value=False)
    surge_factor = st.slider("Surge Multiplier", 1.0, 2.5, 1.3) if covid_surge else 1.0
    forecast_days = st.slider("Forecast Horizon (days)", 1, 14, 7)

    if st.button("Run Flow Forecast"):
        forecast = simulate_flow_forecast(forecast_days, beds, walkin_rate, ambulance, surge_factor, covid_surge)
        st.subheader("Predicted ED Flow")
        st.line_chart(forecast.set_index("Date")[["Predicted_ED_Census", "Bed_Availability"]])
        st.dataframe(forecast)
        st.metric("Max Predicted Occupancy (%)", int(forecast["ED_Occupancy_%"].max()))
        if (forecast["ED_Occupancy_%"] > 100).any():
            st.warning("Overcapacity risk detected in forecast window.")

        st.download_button(
            "Download Forecast Data (CSV)",
            forecast.to_csv(index=False).encode("utf-8"),
            "ed_flow_forecast.csv"
        )
        context.set("flow_forecast", forecast)
