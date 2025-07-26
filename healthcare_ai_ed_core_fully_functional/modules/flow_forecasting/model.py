
def predict_bed_need(current_patients, triage_levels):
    high_acuity = sum(1 for lvl in triage_levels if lvl == "High Acuity")
    beds_needed = int(0.5 * len(current_patients) + high_acuity)
    return {"beds_needed": beds_needed, "high_acuity_patients": high_acuity}
