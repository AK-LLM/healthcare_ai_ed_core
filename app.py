import streamlit as st
from core.config import config
from core.auth import get_current_user

st.set_page_config(page_title="Universal AI ED Platform", layout="wide")
user = get_current_user()

st.sidebar.title("AI Emergency Dept Platform")
st.sidebar.info(f"Logged in as: **{user.username}** ({user.role})")

module = st.sidebar.selectbox(
    "Select Module",
    ["Triage AI", "Flow Forecasting", "Diagnostic Ordering", "Disposition Prediction"]
)

st.title("Universal Modular AI for Emergency Departments")

if module == "Triage AI":
    from modules.triage_ai.views import triage_ui
    triage_ui()
elif module == "Flow Forecasting":
    st.info("Flow Forecasting module coming soon.")
elif module == "Diagnostic Ordering":
    st.info("Diagnostic Ordering module coming soon.")
elif module == "Disposition Prediction":
    st.info("Disposition Prediction module coming soon.")
else:
    st.warning("Select a module to begin.")
