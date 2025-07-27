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
        temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=43.0, value=37.5)
        bp_sys = st.number_input("BP Systolic", 60, 240, 126)
        bp_dia = st.number_input("BP Diastolic", 30, 140, 78)
        resp_rate = st.number_input("Respiratory Rate", 8, 50, 18)
        spo2 = st.number_input("O₂ Sat (%)", 50, 100, 98)
        pain_score = st.slider("Pain Score", 0, 10, 4)

        red_flags = st.multiselect("Red Flags", [
            "Altered mental status", "Sepsis", "Severe pain", "Resp distress", "None"
        ], default=["None"])

        submitted = st.form_submit_button("Predict Triage")

    if submitted:
        result = triage_predict(
            age=age, gender=gender, arrival_mode=arrival_mode, 
            chief_complaint=chief_complaint, hr=hr, temp=temp, bp_sys=bp_sys, bp_dia=bp_dia,
            resp_rate=resp_rate, spo2=spo2, pain_score=pain_score, comorbidities=comorbidities, red_flags=red_flags,
            recent_ed_visits=recent_ed_visits
        )
        trace = triage_trace(result)

        st.success(f"**Predicted Triage Level:** {result['level']} (Risk: {result['risk']}%)")
        st.progress(result['risk'] / 100, text=f"Predicted acuity: {result['level']}")

        st.write("**AI Reasoning / Explanation:**")
        for t in trace:
            st.markdown(f"- {t}")

        st.info(result.get("recommendation", "Assess immediately."))

        history = context.get("triage_history", [])
        history.append({
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "level": result["level"], "chief_complaint": chief_complaint, "risk": result["risk"]
        })
        context.set("triage_history", history[-10:])
        st.subheader("Triage History (This Session)")
        st.dataframe(pd.DataFrame(history[-10:]))

        st.download_button(
            "Download Session Triage Log (CSV)",
            pd.DataFrame(history).to_csv(index=False).encode("utf-8"),
            "triage_log.csv"
        )

        st.caption("Enterprise-grade demo: reasoning, trends, and export included.")

    # --- New: Retrain Model Button ---
    st.divider()
    st.subheader("Triage Model Maintenance")
    def retrain_triage_model(clean_data_path='data/clean_data.csv'):
        try:
            if not os.path.exists(clean_data_path):
                st.warning("No cleaned training data found. Please use Data Ingestion to fetch and clean data first.")
                return
            df = pd.read_csv(clean_data_path)
            # TODO: Plug in real ML pipeline here.
            st.success("Model retrained with trusted data. (Pipeline stub)")
        except Exception as e:
            st.error(f"Retraining failed: {e}")

    if st.button("Retrain Triage Model (Demo)"):
        retrain_triage_model()
