import streamlit as st
from modules.triage_ai.model import triage_predict
from core.context import context

def triage_ui():
    st.header("Triage AI (Demo Mode)")

    # Sample input (expand with real fields as needed)
    age = st.number_input("Patient Age", min_value=0, max_value=120)
    chief_complaint = st.text_input("Chief Complaint")
    hr = st.number_input("Heart Rate", min_value=20, max_value=220)
    temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=44.0)

    if st.button("Predict Triage Level"):
        result = triage_predict(age, chief_complaint, hr, temp)
        st.success(f"Predicted triage level: **{result['level']}**")
        st.json(result)
        context.set("triage", result)
