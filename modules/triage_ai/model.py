def triage_predict(**kwargs):
    risk = 0
    trace = []
    if kwargs.get("arrival_mode") == "Ambulance":
        risk += 10
        trace.append("Ambulance arrival (+10)")
    if kwargs.get("hr", 0) > 120:
        risk += 20
        trace.append("Tachycardia (+20)")
    if kwargs.get("spo2", 100) < 92:
        risk += 20
        trace.append("Low O2 Sat (+20)")
    if "Sepsis" in kwargs.get("red_flags", []):
        risk += 25
        trace.append("Red flag: Sepsis (+25)")
    if "COPD/Asthma" in kwargs.get("comorbidities", []):
        risk += 8
        trace.append("Respiratory comorbidity (+8)")
    risk = min(risk, 99)
    level = "High Acuity" if risk > 50 else "Urgent" if risk > 25 else "Routine"
    return {
        "level": level, "risk": risk,
        "recommendation": "Assess in resus immediately." if risk > 50 else "Assign to monitored bed.",
        "trace": trace
    }

def triage_trace(result):
    if "trace" in result:
        return result["trace"]
    return ["No details available."]
