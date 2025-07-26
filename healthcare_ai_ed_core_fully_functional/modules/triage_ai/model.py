
def triage_predict(age, complaint, hr, temp):
    if hr > 120 or temp > 39:
        return {"level": "High Acuity", "risk": 0.9, "reason": "Abnormal vitals"}
    if "chest pain" in complaint.lower():
        return {"level": "Urgent", "risk": 0.8, "reason": "Chest pain"}
    return {"level": "Routine", "risk": 0.3, "reason": "No red flags"}
