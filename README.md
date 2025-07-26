# Universal Modular AI for Emergency Departments (healthcare_ai_ed_core)

## Overview

This project is an open, country-agnostic, modular AI platform for Emergency Department (ED) triage, flow forecasting, diagnostic ordering, and disposition prediction. It is designed for real-world hospital integration, research, and rapid prototyping.

- **Interoperable:** FHIR, HL7, LOINC, SNOMED, DICOM, OpenEHR adapters
- **Privacy-Ready:** No PHI in code, synthetic data by default
- **Plug-and-Play:** Modules for triage, flow, diagnostics, disposition—extendable for any region or use case
- **Professional Architecture:** CI/CD, Docker, multi-cloud deploy, robust logging, RBAC-ready

## Quick Start

1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. (Optional) Add synthetic FHIR/HL7/DICOM test data in `/data/`

## Documentation

- System design: `/docs/design_overview.md`
- Protocols: `/docs/protocol_coverage.md`
- Literature checklist: `/docs/literature_checklist.md`
- Deployment: `/docs/deployment_guide.md`

## Contributing

PRs welcome! See `/docs/` and `.github/` for guidelines.

---

**Next steps:**  
- Tell me which module or protocol you want full code for next (diagnostic ordering, SNOMED, LOINC, etc.), or if you want more test coverage, user management, RBAC, etc.
- I can also package the above as a ZIP or add starter data for you!

Let’s keep going—just specify what you want to build out next!
