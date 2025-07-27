import pandas as pd
import random

complaints = ['Chest pain', 'Abdominal pain', 'Shortness of breath', 'Fever', 'Falls']
triage_levels = ['High Acuity', 'Urgent', 'Routine']
arrival_modes = ['Walk-in', 'Ambulance']

def generate_patients(n=100):
    data = []
    for i in range(n):
        row = {
            "patient_id": f"ED{i+1:03}",
            "age": random.randint(16, 92),
            "gender": random.choice(['Male', 'Female']),
            "chief_complaint": random.choice(complaints),
            "triage_level": random.choice(triage_levels),
            "arrival_mode": random.choice(arrival_modes),
            "ed_visit_count": random.randint(0, 6)
        }
        data.append(row)
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_patients(100)
    df.to_csv("synthetic_patients.csv", index=False)
