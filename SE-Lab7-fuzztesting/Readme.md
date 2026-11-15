# Lab 7 — Fuzz Testing for Input Validation Bugs

**Student:** M Ajjaiah  
**USN:** PES1UG25CS823  
**Section:** G  
**Base application:** Lab 6 — Water Utility Billing

## Files

- `processor.py` — corrected application with strict validation.
- `test_processor.py` — Hypothesis-based property/fuzz tests for all three functions.
- `processor_original.py` — original Lab 6 implementation, retained for pre-fix reproduction.
- `test_original_failures.py` — Hypothesis tests that demonstrate malformed inputs crashing the original implementation.
- `requirements.txt` — test dependencies.
- `Lab7_Report_PES1UG25CS823.pdf` — consolidated report with evidence and complete required source code.
- `screenshots/` — genuine terminal screenshots supplied during execution.

## Functions tested

1. `validate_billing_inputs(accounts, base_fee)`
2. `calculate_water_bill(accounts, base_fee)`
3. `check_meter_tampering(readings_matrix)`

## Setup and execution

Run these commands from this folder:

```powershell
python -m pip install -r requirements.txt
python -m pytest -v test_original_failures.py
python -m pytest -v test_processor.py
python processor.py
```

The original-failure tests are expected to fail because they assert that malformed values raise `ValueError`, while the original implementation instead raises uncaught `AttributeError`/`TypeError` for the reproduced inputs. This is intentional diagnostic evidence.

The user's captured local execution shows 3 original tests failed as expected and 16 corrected Hypothesis tests passed. The screenshots in `screenshots/` are the evidence supplied for those runs.

## Git

From the parent repository, add this folder, commit, and push using the repository's configured remote:

```powershell
git add Lab7_FuzzTesting_PES1UG25CS823
git commit -m "Complete Lab 7 hypothesis fuzz testing"
git push
```
