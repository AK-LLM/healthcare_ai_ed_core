from modules.triage_ai.model import triage_predict

def test_triage_high_acuity():
    out = triage_predict(50, "flu", 150, 38)
    assert out["level"] == "High Acuity"

def test_triage_chest_pain():
    out = triage_predict(65, "chest pain", 80, 37)
    assert out["level"] == "Urgent"

def test_triage_routine():
    out = triage_predict(30, "cough", 85, 37)
    assert out["level"] == "Routine"
