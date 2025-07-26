import streamlit as st
from modules.triage_ai.model import triage_predict
from core.context import context

def triage_ui():
    st.header("Triage AI (Demo Mode)")
    st.caption("Simulated triage assessment using clinical best practices. No real patient data.")

    with st.form("triage_form"):
        st.subheader("Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Patient Age", min_value=0, max_value=120, value=40)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            arrival_mode = st.selectbox("Arrival Mode", ["Walk-in", "Ambulance", "Referral"])
        with col2:
            chief_complaint = st.text_input("Chief Complaint", value="Chest pain")
            allergies = st.text_input("Known Allergies", value="None")
            comorbidities = st.multiselect(
                "Comorbidities", 
                ["Diabetes", "Hypertension", "COPD/Asthma", "Cancer", "None"], 
                default=["None"]
            )

        st.divider()
        st.subheader("Vital Signs")
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            hr = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=88)
        with col4:
            temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=43.0, value=37.2)
        with col5:
            systolic = st.number_input("Systolic BP", min_value=60, max_value=220, value=120)
            diastolic = st.number_input("Diastolic BP", min_value=30, max_value=140, value=80)
        with col6:
            resp_rate = st.number_input("Respiratory Rate", min_value=5, max_value=40, value=16)
            spo2 = st.number_input("O₂ Saturation (%)", min_value=50, max_value=100, value=98)

        st.divider()
        st.subheader("Assessment Details")
        pain_score = st.slider("Pain Score", 0, 10, 4)
        notes = st.text_area("Nurse/Clinician Notes", "Patient reports chest pain for 1 hour...")

        submitted = st.form_submit_button("Predict Triage Level")

    if submitted:
        # Expand triage_predict to accept more fields for future-proofing
        result = triage_predict(
            age=age, 
            complaint=chief_complaint,
            hr=hr, 
            temp=temp,
            systolic=systolic,
            diastolic=diastolic,
            resp_rate=resp_rate,
            spo2=spo2,
            pain_score=pain_score,
            comorbidities=comorbidities,
            arrival_mode=arrival_mode,
            gender=gender
        )
        st.success(f"**Predicted Triage Level:** {result['level']}")
        st.write(f"**Clinical Reasoning:** {result['reason']}")
        st.metric("Predicted Risk Score", f"{result['risk']*100:.0f}%")
        st.info("Recommended action: " + result.get("recommendation", "See provider soon."))

        st.divider()
        st.subheader("Session Triage History")
        history = context.get("triage_history", [])
        history.append({
            "level": result["level"],
            "chief_complaint": chief_complaint,
            "risk": result["risk"],
            "time": st.session_state.get("time", "now"),
        })
        context.set("triage_history", history[-5:])
        st.table(history[-5:])

        st.caption("This is a synthetic demonstration. No actual patient risk is being assessed.")

