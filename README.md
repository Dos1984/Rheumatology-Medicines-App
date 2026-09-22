# Rheumatology Medicines Safety & Education — Prototype v0.1

Clinician-facing prototype for csDMARD/bDMARD prescribing support and patient education.

## Included exemplar records
- Methotrexate (csDMARD)
- Adalimumab (bDMARD)

## Clinical governance
This prototype is not a prescribing system. Production deployment should use version-controlled, clinically reviewed data with item-level provenance. Brand/formulation-specific current SmPC information should be authoritative for licensed dosing, contraindications, warnings, adverse-effect frequencies and product instructions.

No patient-identifiable data are required or stored in this prototype.

## Evidence basis
- BSR 2025 csDMARD guideline
- BSR biologic DMARD safety guidance
- EULAR infection screening/prophylaxis guidance
- Current Irish/EU SmPC as intended product-level source of truth
- HSE/MMP/PCRS as intended Irish reimbursement/availability layer

Before clinical use, all drug records require formal pharmacy/rheumatology review and current SmPC verification.


## SmPC verification lifecycle

Clinical content is product-level and versioned. Irish medicines.ie SmPCs are preferred; EMA/UK product information may be used as an explicitly labelled fallback where an Irish SmPC is unavailable. A scheduled weekly audit checks tracked source revisions. A detected source change does **not** automatically overwrite prescribing data: affected clinical sections must be re-extracted and reviewed before the verified record is released. The app should display source jurisdiction, SmPC revision and last clinical verification date.
