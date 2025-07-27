import streamlit as st
from core.auth import get_current_user
from analytics.analytics_dashboard import analytics_dashboard

st.set_page_config(page_title="Enterprise AI ED Platform", layout="wide")
user = get_current_user()

st.sidebar.title("AI Emergency Dept Platform")
st.sidebar.info(f"Logged in as: **{user.username}** ({user.role})")

module = st.sidebar.selectbox(
    "Select Module",
    [
        "Triage AI",
        "Flow Forecasting",
        "Diagnostic Ordering",
        "Disposition Prediction",
        "Analytics Dashboard",
        "Data Ingestion"
    ]
)

st.title("Enterprise Modular AI for Emergency Departments")

if module == "Triage AI":
    from modules.triage_ai.views import triage_ui
    triage_ui()
elif module == "Flow Forecasting":
    from modules.flow_forecasting.views import flow_forecasting_ui
    flow_forecasting_ui()
elif module == "Diagnostic Ordering":
    from modules.diagnostic_ordering.views import diagnostic_ordering_ui
    diagnostic_ordering_ui()
elif module == "Disposition Prediction":
    from modules.disposition_prediction.views import disposition_prediction_ui
    disposition_prediction_ui()
elif module == "Analytics Dashboard":
    analytics_dashboard()
elif module == "Data Ingestion":
    from modules.data_ingestion.data_ingestion import data_ingestion_ui
    data_ingestion_ui()
else:
    st.warning("Select a module to begin.")
