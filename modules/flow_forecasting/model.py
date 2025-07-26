def predict_bed_need(current_patients, triage_levels):
    """
    Simple demo logic: returns beds needed in next 2h based on current patients and triage acuity.
    Replace/extend with ML or analytics later.
    """
    high_acuity = sum(1 for lvl in triage_levels if lvl == "High Acuity")
    beds_needed = int(0.5 * len(current_patients) + high_acuity)
    return {"beds_needed": beds_needed, "high_acuity_patients": high_acuity}
