#!/bin/bash
set -e
echo "Running Automated LLM Evaluation Test Suite..."
pytest -v --tb=short
echo "All evaluation checks passed!"
