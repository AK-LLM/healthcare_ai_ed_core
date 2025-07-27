# modules/cardiac_risk/model.py

def calculate_risk(age, sex, cholesterol, systolic_bp, smoking, diabetes):
    """
    Example Framingham Risk-like calculation (very simplified for demo).
    """
    risk = 0
    risk += 0.1 * age
    if sex == "Male":
        risk += 2
    risk += 0.02 * cholesterol
    risk += 0.03 * systolic_bp
    risk += 2 if smoking else 0
    risk += 2 if diabetes else 0
    # Return risk score (0-20 demo scale)
    return min(max(round(risk, 2), 0), 20)

