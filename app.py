import streamlit as st

# Defensive imports for modular code
try:
    from core.config import config
except Exception as e:
    st.error(f"Config import error: {e}")
    config = None

try:
    from core.auth import get_current_user
except Exception as e:
    st.error(f"Auth import error: {e}")
    def get_current_user():
        class Dummy:
            username = "unknown"
            role = "tester"
        return Dummy()

# App layout and navigation
st.set_page_config(page_title="Universal AI ED Platform", layout="wide")
user = get_current_user()

st.sidebar.title("AI Emergency Dept Platform")
st.sidebar.info(f"Logged in as: **{user.username}** ({user.role})")

module = st.sidebar.selectbox(
    "Select Module",
    ["Triage AI", "Flow Forecasting", "Diagnostic Ordering", "Disposition Prediction"]
)

st.title("Universal Modular AI for Emergency Departments")

# Try importing each module's UI only if needed, so a broken module won't crash the whole app
if module == "Triage AI":
    try:
        from modules.triage_ai.views import triage_ui
        triage_ui()
    except Exception as e:
        st.error(f"Triage module failed to load: {e}")

elif module == "Flow Forecasting":
    try:
        from modules.flow_forecasting.views import flow_forecasting_ui
        flow_forecasting_ui()
    except Exception as e:
        st.error(f"Flow Forecasting module failed to load: {e}")

elif module == "Diagnostic Ordering":
    try:
        from modules.diagnostic_ordering.views import diagnostic_ordering_ui
        diagnostic_ordering_ui()
    except Exception as e:
        st.info("Diagnostic Ordering module coming soon.")
        st.error(f"Diagnostic Ordering module failed to load: {e}")

elif module == "Disposition Prediction":
    try:
        from modules.disposition_prediction.views import disposition_prediction_ui
        disposition_prediction_ui()
    except Exception as e:
        st.info("Disposition Prediction module coming soon.")
        st.error(f"Disposition Prediction module failed to load: {e}")

else:
    st.warning("Select a module to begin.")
