# modules/cardiac_risk/views.py

import streamlit as st
from modules.cardiac_risk.model import calculate_risk

def cardiac_risk_ui():
    st.header("Cardiac Risk Assessment")
    st.caption("Estimate a patient's cardiac risk (Framingham-inspired, not for clinical use).")

    with st.form("cardiac_risk_form"):
        age = st.number_input("Age", min_value=20, max_value=80, value=50)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
        systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=90, max_value=220, value=130)
        smoking = st.checkbox("Current smoker")
        diabetes = st.checkbox("Diabetes")
        submitted = st.form_submit_button("Calculate Risk")
        
        if submitted:
            risk = calculate_risk(age, sex, cholesterol, systolic_bp, smoking, diabetes)
            st.success(f"Estimated Cardiac Risk Score: **{risk} / 20**")

