# AstraLog-HPC
### **Standard Track Template | A.Y. 2025-2026**

Welcome to the **AstraLog-HPC** Standard Track project. This repository provides a mock environment for the telemetry analysis software used in the *"Software Engineering for HPC"* course.

> [!IMPORTANT]
> Your objective is **not to implement the analysis logic**, but to engineer the **DevOps infrastructure** required to test, containerize, and execute this software on the **CINECA Galileo 100 cluster**.

---

## Repository Structure

```text
.
├── src/                         # Engine and main entry point
│   └── astralog_mock.py
├── tests/                       # Pytest test suite
│   └── test_astralog.py
├── input/
│   └── rules.json               # Sample mission rules
│   └── telemetry_cleaned.csv    # Sample telemetry data
└── requirements.txt             # Python dependencies (pytest only)
```

---

## Local Usage

### Installation
Install the required testing framework:
```bash
pip install -r requirements.txt
```

### Running the Mock Engine
The engine simulates the analysis process. Run it via the command line:
```bash
python3 -m src.astralog_mock \
  --rules input/rules.json \
  --input input/telemetry_cleaned.csv \
  --output ./results
```

### Running Unit Tests
Validate the environment and the mock engine using `pytest`:
```bash
python3 -m pytest -v
```

---

## DevOps Assignment (Your Tasks)

Your final grade depends on the successful implementation of the following components:

### 1. CI/CD Pipeline
Create a GitHub Actions workflow in `.github/workflows/main.yml`. The pipeline must:
- [ ] **Trigger:** Run automatically on every `push`.
- [ ] **Setup:** Install all necessary dependencies.
- [ ] **Test:** Execute the test suite using `pytest`.

### 2. Containerization
Write a `Singularity.def` file to:
- [ ] Package the application and all required libraries.
- [ ] Ensure full **reproducibility** of the computing environment.

### 3. HPC Execution
Create a `job.sh` script to:
- [ ] Submit jobs via the **SLURM** scheduler.
- [ ] Execute the containerized application.
- [ ] Target the **Galileo 100 cluster** with correct configurations.

### 4. Automation
Extend your CI/CD pipeline to:
- [ ] **Deploy** the container to the cluster environment.
- [ ] **Automate** job submission on the HPC cluster directly from GitHub Actions.

---

## Rules

### Oral Examination
During the oral exam, you must be prepared to:
*   **Explain** every part of your pipeline and infrastructure.
*   **Modify** configurations live if requested by the instructor.

### Documentation
Your final submission **must include** in the `README.md`:
1. The names of all team members.
2. The selected track (standard in your case).
3. The role of each team member in the project, the detailed activities performed, and the effort spent in hours. 
4.  A detailed section explaining your DevOps design choices. Present also the difficulties you have faced. For those you have overcome, explain how you did it; for the others, describe the attempts you made. 
5.  A description of how AI tools were utilized in the process, if any.

---

## Expected Outcomes
By completing this project, you will master:
*   **CI/CD workflows** tailored for High-Performance Computing.
*   Scientific containerization using **Singularity**.
*   Workload management with **SLURM**.
*   End-to-end **DevOps automation** in a scientific context.

---

## Notes
*   This is a **mock environment**: no real telemetry analysis implementation is required.
*   The focus is entirely on **infrastructure, portability, and automation**.
*   Ensure your solution is **clean, reproducible, and well-documented**.
