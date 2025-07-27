import streamlit as st
import pandas as pd
import datetime
from core.context import context

def disposition_prediction_ui():
    st.header("Disposition Prediction (Advanced Demo)")
    st.caption("Predicts likely ED disposition using a weighted ruleset and demo ML logic. All patient data here is synthetic.")

    st.subheader("Patient Summary")
    col1, col2 = st.columns(2)
    with col1:
        patient_id = st.text_input("MRN / Patient ID", value=f"ED{datetime.datetime.now().strftime('%m%d%H%M')}")
        age = st.number_input("Age", min_value=0, max_value=120, value=78)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        arrival = st.selectbox("Arrival Mode", ["Ambulance", "Walk-in", "Referral"])
    with col2:
        chief_complaint = st.text_input("Chief Complaint", value="Shortness of breath")
        triage_acuity = st.selectbox("Triage Acuity", ["Resuscitation", "Emergent", "Urgent", "Less Urgent", "Non-Urgent"])
        comorbidities = st.multiselect("Comorbidities", [
            "CHF", "Diabetes", "COPD", "CKD", "Cancer", "None"], default=["COPD"])
        support = st.selectbox("Home Support", ["Lives alone", "Family support", "Care home", "No fixed address"])

    st.divider()
    st.subheader("Clinical & Social Risk Factors")
    col3, col4, col5 = st.columns(3)
    with col3:
        vital_instability = st.checkbox("Vital Instability (e.g., SBP <90, SpO2 <92%)", value=True)
        abnormal_labs = st.checkbox("Abnormal Labs/Imaging", value=True)
        psychiatric = st.checkbox("Active Psych Issue", value=False)
    with col4:
        pain_score = st.slider("Pain Score", 0, 10, 5)
        admission_risk = st.slider("Clinician Admission Estimate (%)", 0, 100, 80)
        language_barrier = st.checkbox("Language/Cultural Barrier", value=False)
    with col5:
        recent_ed_visits = st.number_input("ED Visits in Last 30 Days", 0, 10, 1)
        safety_concerns = st.checkbox("Safety/Abuse/Neglect Flag", value=False)

    if st.button("Predict Disposition"):
        trace = []
        risk = 0

        if triage_acuity in ["Resuscitation", "Emergent"]:
            risk += 30
            trace.append("High acuity (+30)")
        if vital_instability:
            risk += 20
            trace.append("Unstable vitals (+20)")
        if abnormal_labs:
            risk += 10
            trace.append("Abnormal labs/imaging (+10)")
        if "None" not in comorbidities and len(comorbidities) > 0:
            risk += 5
            trace.append("Chronic comorbidities (+5)")
        if support in ["Lives alone", "No fixed address"]:
            risk += 10
            trace.append("Poor home support (+10)")
        if psychiatric:
            risk += 10
            trace.append("Active psych issue (+10)")
        if language_barrier:
            risk += 5
            trace.append("Language barrier (+5)")
        if recent_ed_visits > 2:
            risk += 5
            trace.append("Frequent ED use (+5)")
        if safety_concerns:
            risk += 15
            trace.append("Safety/abuse flag (+15)")
        if admission_risk > 70:
            risk += 10
            trace.append("Clinician override/estimate (+10)")

        risk = min(100, risk)
        confidence = min(100, 70 + abs(admission_risk - 70)//2)

        if risk >= 60:
            disposition = "Admit to Hospital"
        elif risk >= 40:
            disposition = "Observation/Short Stay Unit"
        else:
            disposition = "Safe for Discharge"

        st.success(f"**Recommended Disposition:** {disposition}")
        st.metric("Predicted Admission Risk (%)", risk)
        st.progress(confidence / 100, text="Prediction Confidence")

        st.write("**AI Reasoning / Trace:**")
        for line in trace:
            st.markdown(f"- {line}")

        triage_history = context.get("disposition_history", [])
        triage_history.append({
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": patient_id,
            "disposition": disposition,
            "risk": risk,
            "confidence": confidence,
            "chief_complaint": chief_complaint,
        })
        context.set("disposition_history", triage_history[-10:])
        st.divider()
        st.subheader("Session Disposition History")
        st.dataframe(pd.DataFrame(triage_history[-10:]))

        csv = pd.DataFrame(triage_history).to_csv(index=False).encode('utf-8')
        st.download_button("Download Disposition Log (CSV)", csv, "disposition_log.csv", "text/csv")

        st.caption("This is a synthetic advanced demo. All logic is explainable, and ready for real model integration.")
