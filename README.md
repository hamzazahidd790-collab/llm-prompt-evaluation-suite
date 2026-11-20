# Automated LLM & Prompt Evaluation Suite

A lightweight, containerized Python framework built to evaluate **LLM / AI Agent (Claude & GPT)** outputs for structured JSON compliance, prompt instruction adherence, keyword coverage, and edge-case handling.

## Features
- **Automated Rubric Scoring:** Validates JSON schema formatting, keyword coverage, and refusal detection.
- **Automated Testing with `pytest`:** Comprehensive unit and edge-case test suites.
- **Containerized Execution:** Reproducible Linux environment via `Docker`.
- **Shell Automation:** One-command test execution via `run_eval.sh`.

## Quick Start (Linux / Docker)

### Run Locally with `pytest`
```bash
pip install -r requirements.txt
chmod +x run_eval.sh
./run_eval.sh
```

### Run inside Docker
```bash
docker build -t llm-eval-suite .
docker run --rm llm-eval-suite
```
