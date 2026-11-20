# Lab 6 — Code and Branch Coverage Analysis

**SRN:** PES2UG24AM169  
**Assigned repository:** L6_L7_13_pet_walking_service (Lab 6)

Two independent test suites are included as required: `CodeCoverageTest_PES2UG24AM169_application.py` and `BranchCoverageTest_PES2UG24AM169_application.py`. The tests cover route confirmation, all session types, invalid session types, pet counts, aggression alerts, medication, weekend transport fees, incident audit status, zero/completed statuses, GPS empty/online/lost-signal cases, and input validation.

## Run line/code coverage
```bash
python -m coverage erase
python -m coverage run --source=pet_walking_service -m pytest -q CodeCoverageTest_PES2UG24AM169_application.py
python -m coverage report -m
```

## Run branch coverage
```bash
python -m coverage erase
python -m coverage run --branch --source=pet_walking_service -m pytest -q BranchCoverageTest_PES2UG24AM169_application.py
python -m coverage report -m
```

Commit the code-coverage suite first and the branch-coverage suite second when pushing to the assigned GitHub repository.
