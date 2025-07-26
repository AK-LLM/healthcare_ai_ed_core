from core.protocols.fhir_adapter import FHIRAdapter

def test_extract_demographics():
    fhir = FHIRAdapter(base_path="data/")
    sample = {
        "name": [{"text": "John Doe"}],
        "gender": "male",
        "birthDate": "1980-01-01"
    }
    result = fhir.extract_demographics(sample)
    assert result["name"] == "John Doe"
    assert result["gender"] == "male"
    assert result["birthdate"] == "1980-01-01"
