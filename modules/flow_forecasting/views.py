import streamlit as st
import datetime
from core.context import context

def flow_forecasting_ui():
    st.header("ED Flow Forecasting (Demo Mode)")
    st.caption("Forecasts patient inflow, bed utilization, and bottlenecks. Uses demo/synthetic data.")

    today = datetime.date.today()
    st.write("Select date range to forecast patient flow:")
    start_date = st.date_input("Start Date", today)
    end_date = st.date_input("End Date", today + datetime.timedelta(days=1))

    day_range = (end_date - start_date).days + 1
    if day_range < 1:
        st.warning("End date must be after start date.")
        return

    beds_available = st.number_input("Total ED Beds", min_value=5, max_value=100, value=30)
    staff_on_duty = st.number_input("Staff On Duty (RNs/MDs)", min_value=1, max_value=50, value=8)
    scheduled_admissions = st.number_input("Scheduled Admissions", min_value=0, max_value=40, value=5)
    walkin_rate = st.slider("Walk-in Rate (patients/hr)", 0, 20, 6)
    ambulance_rate = st.slider("Ambulance Arrivals (per day)", 0, 30, 8)
    covid_alert = st.checkbox("Pandemic/Epidemic Surge Scenario?", value=False)

    forecast = []
    for i in range(day_range):
        # Synthetic daily volumes: Walk-in + ambulance + scheduled, plus surge effect
        base = walkin_rate * 24 + ambulance_rate + scheduled_admissions
        surge = base * 1.5 if covid_alert else base
        patients = int(surge if covid_alert else base)
        occupancy = min(100, int(patients / beds_available * 100))
        forecast.append({
            "Date": (start_date + datetime.timedelta(days=i)).isoformat(),
            "Forecast_Patients": patients,
            "ED_Occupancy_%": occupancy,
            "Staff_On_Duty": staff_on_duty,
        })

    if st.button("Run Forecast"):
        st.subheader("Forecast Results")
        st.dataframe(forecast)
        st.metric("Peak ED Occupancy (%)", max(row["ED_Occupancy_%"] for row in forecast))
        if max(row["ED_Occupancy_%"] for row in forecast) > 85:
            st.warning("High risk of ED overcrowding on forecasted days!")
        st.caption("Demo logic—replace with hospital EHR data or actual forecasting models as needed.")

        context.set("flow_forecast", forecast)
