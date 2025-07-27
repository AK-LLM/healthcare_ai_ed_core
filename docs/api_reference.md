# API Reference

## Core Protocol Adapters

- `parse_fhir_resource(resource: dict) -> dict`
- `parse_hl7_message(msg: str) -> dict`
- `get_loinc_code(term: str) -> str`
- `get_snomed_code(term: str) -> str`
- `parse_dicom_file(dcm) -> dict`
- `parse_openehr(data: dict) -> dict`
- `send_mllp_message(msg: str) -> dict`
- `call_soap_service(request: dict) -> dict`

## Modules

- `triage_predict(...)` - Returns triage level, risk, and recommendation
- `simulate_flow_forecast(...)` - Simulates ED patient census, occupancy, wait times
- `diagnostic_ordering_ui()` - Decision support for lab/radiology
- `disposition_prediction_ui()` - Predicts ED disposition (admit/discharge/etc.)

## Analytics

- Session metrics and export functions in `analytics_dashboard.py`

