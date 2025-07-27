import streamlit as st
import datetime
import pandas as pd
import os
from modules.triage_ai.model import triage_predict, triage_trace
from core.context import context

def triage_ui():
    st.header("AI Triage (Advanced)")
    st.caption("Modern triage scoring using multiple factors, clinical rules, and explainable logic. No PHI.")

    with st.form("triage_form"):
        st.subheader("Patient Info")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=42)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            arrival_mode = st.selectbox("Arrival Mode", ["Walk-in", "Ambulance", "Referral"])
            recent_ed_visits = st.number_input("ED visits (last 30 days)", 0, 10, 0)
        with col2:
            chief_complaint = st.text_input("Chief Complaint", "Shortness of breath")
            allergies = st.text_input("Allergies", "None")
            comorbidities = st.multiselect(
                "Comorbidities", 
                ["Diabetes", "Hypertension", "COPD/Asthma", "Cancer", "None"], 
                default=["None"]
            )

        st.subheader("Vital Signs")
        hr = st.number_input("Heart Rate", min_value=30, max_value=200, value=98)
        temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=43.0,_
