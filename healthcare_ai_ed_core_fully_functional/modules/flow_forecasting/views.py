
import streamlit as st
from modules.flow_forecasting.model import predict_bed_need
def flow_forecasting_ui():
    st.header("Flow/Bed Forecasting (Demo Mode)")
    num_patients = st.number_input("Number of current patients", min_value=1, value=10)
    triage_levels = st.multiselect("Triage levels", ["High Acuity", "Urgent", "Routine"], default=["Routine"])
    patients = [{"id": i, "triage": t} for i, t in enumerate(triage_levels * num_patients)]
    if st.button("Forecast Bed Needs"):
        result = predict_bed_need(patients, triage_levels)
        st.success(f"Predicted beds needed: **{result['beds_needed']}**")
        st.json(result)
