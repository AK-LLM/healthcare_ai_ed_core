import streamlit as st
from core.context import context

def disposition_prediction_ui():
    st.header("Disposition Prediction (Demo Mode)")
    st.caption("Predicts ED disposition based on patient risk, social, and clinical scenario.")

    st.subheader("Disposition Factors")
    age = st.number_input("Patient Age", min_value=0, max_value=120, value=70)
    acuity = st.selectbox("Triage Acuity", ["Resuscitation", "Emergent", "Urgent", "Less Urgent", "Non-Urgent"])
    comorbidities = st.multiselect("Comorbidities", [
        "Diabetes", "Heart Failure", "COPD", "Cancer", "Immunosuppressed", "None"
    ])
    social_factors = st.multiselect("Social Factors", [
        "Lives alone", "No fixed address", "No support at home", "Elderly caregiver", "None"
    ])
    vital_instability = st.checkbox("Vital Instability", value=False)
    abnormal_labs = st.checkbox("Abnormal Labs/Imaging", value=False)
    admission_risk_score = st.slider("Admission Risk (clinician estimate)", 0, 100, 25)

    if st.button("Predict Disposition"):
        # Basic rule-based demo logic (replace with AI model as needed)
        admit = False
        obs = False
        explanation = []
        if acuity in ["Resuscitation", "Emergent"] or vital_instability:
            admit = True
            explanation.append("High acuity or unstable vitals.")
        if "No support at home" in social_factors or admission_risk_score > 65:
            admit = True
            explanation.append("No safe discharge or high admission risk.")
        if acuity in ["Urgent", "Less Urgent"] and not admit:
            obs = True
            explanation.append("Could benefit from observation.")
        if not admit and not obs:
            explanation.append("Safe for discharge with follow-up.")

        result = "Admit to hospital" if admit else "Observation" if obs else "Discharge"
        st.success(f"**Recommended Disposition:** {result}")
        st.write("**Rationale:**", " ".join(explanation))
        context.set("disposition_prediction", {"result": result, "explanation": explanation})

        st.caption("This is a demonstration of disposition support. Not real patient advice.")
