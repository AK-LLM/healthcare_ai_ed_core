import requests
import os

class APIClient:
    """
    Demo API Client (future FHIR/HL7-ready).
    """
    def __init__(self, base_url=None, token=None):
        self.base_url = base_url or os.environ.get("AI_ED_API_URL", "")
        self.token = token or os.environ.get("AI_ED_API_TOKEN", "")

    def get_fhir_patient(self, patient_id):
        if not self.base_url:
            raise RuntimeError("No API base URL configured.")
        url = f"{self.base_url}/Patient/{patient_id}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    # Add post/put methods, HL7 endpoints, error handling as needed

# Usage (future): api = APIClient(); api.get_fhir_patient("1234")
