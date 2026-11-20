import json
import re
from typing import Dict, List, Any


class LLMEvaluator:
    """
    Evaluates LLM / AI Agent responses (Claude / GPT) against structured prompt
    engineering rubrics, format compliance, and hallucination guardrails.
    """

    def __init__(self, required_keywords: List[str] = None):
        self.required_keywords = required_keywords or []

    def check_json_validity(self, response_text: str) -> bool:
        """Checks whether the model output is valid JSON."""
        try:
            json.loads(response_text)
            return True
        except (ValueError, TypeError):
            return False

    def check_keyword_coverage(self, response_text: str) -> float:
        """Returns fraction (0.0 to 1.0) of required keywords present in output."""
        if not self.required_keywords:
            return 1.0
        text_lower = response_text.lower()
        matched = sum(1 for kw in self.required_keywords if kw.lower() in text_lower)
        return round(matched / len(self.required_keywords), 2)

    def evaluate_response(self, prompt: str, response_text: str, expect_json: bool = False) -> Dict[str, Any]:
        """Runs full evaluation pipeline on a single prompt-response pair."""
        if not response_text or not response_text.strip():
            return {
                "passed": False,
                "score": 0.0,
                "errors": ["Empty response from model"]
            }

        errors = []
        json_ok = True
        if expect_json:
            json_ok = self.check_json_validity(response_text)
            if not json_ok:
                errors.append("Expected valid JSON output, but parsing failed.")

        kw_score = self.check_keyword_coverage(response_text)
        if kw_score < 0.8:
            errors.append(f"Low keyword coverage: {kw_score * 100:.0f}%")

        # Penalize refusal / uncertainty phrases in deterministic tasks
        refusal_patterns = [r"as an ai language model", r"i cannot fulfill this request"]
        for pat in refusal_patterns:
            if re.search(pat, response_text.lower()):
                errors.append("Unexpected model refusal detected.")

        passed = len(errors) == 0
        final_score = round((1.0 if json_ok else 0.0) * 0.5 + kw_score * 0.5, 2) if expect_json else kw_score

        return {
            "passed": passed,
            "score": final_score,
            "errors": errors
        }
