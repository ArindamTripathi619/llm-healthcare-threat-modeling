# Experimental Harness: Secure LLM Orchestrator

This directory contains the code for the **controlled experimental prototype** defined in the research paper.

## ⚠️ Research Disclaimer
This is **NOT** a production healthcare application. It is a measurement instrument designed to:
1.  Simulate specific threat vectors (direct/indirect prompt injection).
2.  Evaluate the effectiveness of proposed defenses (Vector Shield, Guardrails).
3.  Measure latency and cost overheads.

## Directory Structure
- **`orchestrator/`**: The core API gateway and logic hub.
  - **`input_defense/`**: Vector-based intent analysis (probabilistic).
  - **`context/`**: Simulated EHR retrieval (deterministic).
  - **`llm/`**: Isolated proxy for external model calls.
  - **`guardrails/`**: Output validation pipeline.
- **`client/`**: Attacker scripts and benign traffic simulators.
- **`data/`**: Local vector stores and mock EHR JSONs.
- **`logs/`**: WORM-style audit logs and metric CSVs.

## Configuration
All settings are controlled via `config.yaml`. **Do not hardcode thresholds.**

## Setup
```bash
pip install -r requirements.txt
```

## Running the Orchestrator (Future)
```bash
# From project root
uvicorn experiments.orchestrator.main:app --reload
```
