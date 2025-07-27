import streamlit as st
from core.context import context

ORDER_RULES = {
    "Chest pain": {
        "labs": ["Troponin", "CBC", "D-dimer", "Electrolytes"],
        "imaging": ["ECG", "Chest X-ray"],
        "urgent": True,
        "cost_estimate": 350
    },
    "Abdominal pain": {
        "labs": ["CBC", "Lipase", "Liver function"],
        "imaging": ["Abdominal Ultrasound"],
        "urgent": False,
        "cost_estimate": 200
    },
    "Fever": {
        "labs": ["CBC", "Blood cultures", "Urinalysis"],
        "imaging": ["Chest X-ray"],
        "urgent": False,
        "cost_estimate": 180
    },
    "Trauma": {
        "labs": ["CBC", "Type & Screen"],
        "imaging": ["Trauma Series", "FAST US"],
        "urgent": True,
        "cost_estimate": 700
    }
}

def diagnostic_ordering_ui():
    st.header("Diagnostic Ordering AI (Enterprise Demo)")
    st.caption("Clinical decision support with evidence rules, urgency, and cost estimation.")

    patient_age = st.number_input("Age", 0, 120, 47)
    complaint = st.selectbox("Chief Complaint", list(ORDER_RULES.keys()) + ["Other"])
    comorbidities = st.multiselect("Comorbidities", [
        "Cardiac", "Diabetes", "COPD", "Pregnant", "Immunosuppressed", "None"
    ], default=["None"])
    red_flags = st.multiselect("Red Flags", ["Hypotension", "Sepsis", "Altered Mental Status", "None"], default=["None"])

    if st.button("Get Diagnostic Orders"):
        if complaint in ORDER_RULES:
            orders = ORDER_RULES[complaint]
        else:
            orders = {"labs": ["CBC", "Basic Metabolic Panel"], "imaging": [], "urgent": False, "cost_estimate": 120}

        if "Sepsis" in red_flags:
            orders["labs"].append("Lactate")
            orders["urgent"] = True
            orders["cost_estimate"] += 40
        if "Pregnant" in comorbidities and complaint in ["Abdominal pain", "Trauma"]:
            orders["imaging"].append("Pelvic US")
            orders["cost_estimate"] += 50

        st.success(f"Orders generated for: {complaint}")
        st.write(f"**Labs:** {', '.join(set(orders['labs'])) or 'None'}")
        st.write(f"**Imaging:** {', '.join(set(orders['imaging'])) or 'None'}")
        st.metric("Estimated Total Cost (USD)", f"${orders['cost_estimate']}")
        st.metric("Urgency", "STAT" if orders["urgent"] else "Routine")

        st.write("**Reasoning Trace:**")
        st.markdown(
            "- Orders chosen based on complaint and risk\n"
            f"- {'STAT' if orders['urgent'] else 'Routine'} based on clinical flags\n"
            "- Cost estimates demo (real costs from hospital billing)"
        )

        context.set("diagnostic_ordering", orders)
