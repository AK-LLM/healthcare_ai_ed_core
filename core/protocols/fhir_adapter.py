import json
from core.config import config

class FHIRAdapter:
    """
    Minimal FHIR adapter to parse/format synthetic or real FHIR bundles.
    Add/override methods as needed for HL7, LOINC, etc.
    """

    def __init__(self, base_path=config.DATA_PATH):
        self.base_path = base_path

    def load_patient_from_file(self, filename):
        """
        Load a FHIR Patient resource (JSON format) from data dir.
        """
        path = f"{self.base_path}/synthea_samples/{filename}"
        with open(path, "r") as f:
            return json.load(f)

    def extract_demographics(self, patient_json):
        """
        Extract name, age, gender from FHIR Patient resource.
        """
        name = patient_json.get("name", [{}])[0].get("text", "Unknown")
        gender = patient_json.get("gender", "Unknown")
        birthdate = patient_json.get("birthDate", None)
        # Compute age from birthdate if needed
        return {"name": name, "gender": gender, "birthdate": birthdate}

    # Add more FHIR utility methods as needed for modularity

# Usage: fhir = FHIRAdapter(); patient = fhir.load_patient_from_file("patient1.json")
