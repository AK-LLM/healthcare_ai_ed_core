import streamlit as st
from core.context import context

def diagnostic_ordering_ui():
    st.header("Diagnostic Ordering AI (Demo Mode)")
    st.caption("Decision support for ordering labs and imaging based on patient scenario.")

    st.subheader("Patient Snapshot")
    complaint = st.selectbox("Chief Complaint", [
        "Chest pain", "Shortness of breath", "Abdominal pain", "Headache", "Fever", "Trauma", "Other"
    ])
    age = st.number_input("Age", min_value=0, max_value=120, value=50)
    risk_factors = st.multiselect("Risk Factors", [
        "Diabetes", "Hypertension", "Heart Disease", "Recent Surgery", "On anticoagulants", "None"
    ])
    symptom_duration = st.slider("Symptom Duration (hours)", 0, 48, 2)
    red_flags = st.checkbox("Red Flags (e.g., syncope, hypotension, etc.)", value=False)
    pregnancy = st.checkbox("Pregnant (if applicable)", value=False)

    if st.button("Get Diagnostic Suggestions"):
        labs = []
        imaging = []
        explanation = []
        # Very basic demo rules:
        if complaint == "Chest pain":
            labs += ["Troponin", "CBC", "Electrolytes", "D-dimer" if "On anticoagulants" in risk_factors else ""]
            imaging += ["ECG", "Chest X-ray"]
            if red_flags:
                imaging += ["CT Angiogram"]
            explanation.append("Standard ACS workup with risk stratification.")
        elif complaint == "Abdominal pain":
            labs += ["CBC", "Liver function", "Lipase"]
            imaging += ["Abdominal Ultrasound"]
            if age > 50 or red_flags:
                imaging += ["Abdominal CT"]
            explanation.append("Older age/red flag triggers advanced imaging.")
        elif complaint == "Headache":
            labs += ["CBC", "Electrolytes"]
            if red_flags or age > 60:
                imaging += ["Head CT"]
            explanation.append("CT indicated for red flag or older patient.")
        elif complaint == "Fever":
            labs += ["CBC", "Blood cultures", "Urinalysis"]
            if risk_factors:
                imaging += ["Chest X-ray"]
            explanation.append("Sepsis or pneumonia workup as indicated.")
        elif complaint == "Trauma":
            labs += ["CBC", "Blood type"]
            imaging += ["Trauma series X-ray", "FAST ultrasound"]
            if red_flags:
                imaging += ["Whole-body CT"]
            explanation.append("Red flag or instability triggers whole-body CT.")
        else:
            labs += ["CBC", "Basic Metabolic Panel"]
            explanation.append("Basic evaluation for undifferentiated complaints.")

        labs = [lab for lab in labs if lab]  # Remove blanks
        imaging = list(set(imaging))  # Remove duplicates

        st.success("Suggested Diagnostic Orders:")
        st.write("**Labs:**", ", ".join(labs) if labs else "None")
        st.write("**Imaging:**", ", ".join(imaging) if imaging else "None")
        st.write("**Explanation:**", " ".join(explanation))
        context.set("diagnostic_ordering", {"labs": labs, "imaging": imaging, "explanation": explanation})

        st.caption("Demo AI logic. Not for clinical use.")
