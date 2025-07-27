import streamlit as st
import pandas as pd
from core.context import context

def analytics_dashboard():
    st.header("Session Analytics Dashboard")
    triage_hist = context.get("triage_history", [])
    flow_forecast = context.get("flow_forecast", pd.DataFrame())
    disposition_hist = context.get("disposition_history", [])
    st.subheader("Triage History")
    if triage_hist:
        st.dataframe(pd.DataFrame(triage_hist))
    st.subheader("Disposition Prediction History")
    if disposition_hist:
        st.dataframe(pd.DataFrame(disposition_hist))
    st.subheader("ED Flow Forecast")
    if isinstance(flow_forecast, pd.DataFrame) and not flow_forecast.empty:
        st.line_chart(flow_forecast.set_index("Date")[["Predicted_ED_Census", "Bed_Availability"]])
        st.dataframe(flow_forecast)
    st.caption("Session analytics reflect the last N actions this session.")
