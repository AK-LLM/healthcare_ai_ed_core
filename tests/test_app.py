import pytest

def test_import_app():
    """Ensure the main app script and key modules import with no errors."""
    try:
        import app
        import core.auth
        import core.context
        import core.config
        import core.protocols.fhir_adapter
        import modules.triage_ai.views
        import modules.triage_ai.model
        import modules.flow_forecasting.views
        import modules.diagnostic_ordering.views
        import modules.disposition_prediction.views
        import analytics.analytics_dashboard
    except Exception as e:
        pytest.fail(f"Module import failed: {e}")

def test_basic_user():
    from core.auth import get_current_user
    user = get_current_user()
    assert hasattr(user, "username")
    assert hasattr(user, "role")

def test_triage_predict():
    from modules.triage_ai.model import triage_predict
    result = triage_predict(arrival_mode="Ambulance", hr=130, spo2=90, red_flags=["Sepsis"], comorbidities=["COPD/Asthma"])
    assert isinstance(result, dict)
    assert "level" in result and "risk" in result
    assert result["risk"] > 0

def test_protocol_adapters():
    from core.protocols.fhir_adapter import parse_fhir_resource
    from core.protocols.hl7_adapter import parse_hl7_message
    from core.protocols.loinc_adapter import get_loinc_code
    from core.protocols.snomed_adapter import get_snomed_code
    assert parse_fhir_resource({"resourceType": "Patient"})["parsed"]
    assert parse_hl7_message("ADT|")["parsed"]
    assert "LOINC" in get_loinc_code("glucose")
    assert "SNOMED" in get_snomed_code("diabetes")
