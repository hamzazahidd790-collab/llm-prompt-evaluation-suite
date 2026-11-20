import pytest
from evaluator import LLMEvaluator


def test_valid_json_response():
    evaluator = LLMEvaluator(required_keywords=["roomNo", "status"])
    sample_output = '{"roomNo": "104", "status": "allocated"}'
    result = evaluator.evaluate_response(
        prompt="Return room allotment as JSON",
        response_text=sample_output,
        expect_json=True
    )
    assert result["passed"] is True
    assert result["score"] == 1.0
    assert result["errors"] == []


def test_invalid_json_fails():
    evaluator = LLMEvaluator(required_keywords=["roomNo"])
    bad_output = "Room 104 is allocated"
    result = evaluator.evaluate_response(
        prompt="Return room allotment as JSON",
        response_text=bad_output,
        expect_json=True
    )
    assert result["passed"] is False
    assert "Expected valid JSON output, but parsing failed." in result["errors"]


def test_empty_response_handled():
    evaluator = LLMEvaluator()
    result = evaluator.evaluate_response(prompt="Hello", response_text="   ")
    assert result["passed"] is False
    assert result["score"] == 0.0


def test_keyword_coverage_threshold():
    evaluator = LLMEvaluator(required_keywords=["Python", "Docker", "Linux", "pytest"])
    partial_output = "We use Python and Docker for deployment."
    result = evaluator.evaluate_response(prompt="List stack", response_text=partial_output)
    assert result["passed"] is False
    assert result["score"] == 0.5
