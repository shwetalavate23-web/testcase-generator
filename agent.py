"""LLM agent logic for generating business-scenario-oriented regression test cases."""

from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from config import Settings
from prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class RegressionTestCaseAgent:
    """Agent responsible for generating regression test cases from requirements."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)

    def read_requirements(self, requirement_file: Path) -> str:
        """Read user stories / functional requirements from the configured file."""

        if not requirement_file.exists():
            raise FileNotFoundError(
                f"Requirement file not found: {requirement_file}. "
                "Create requirement.txt and add your user stories."
            )

        contents = requirement_file.read_text(encoding="utf-8").strip()
        if not contents:
            raise ValueError(f"Requirement file is empty: {requirement_file}")

        return contents

    def generate_regression_test_cases(self, requirements: str) -> str:
        """Generate structured business-oriented regression test cases using OpenAI."""

        response = self._client.responses.create(
            model=self._settings.openai_model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT_TEMPLATE.format(requirements=requirements),
                },
            ],
        )
        return response.output_text.strip()

    def run(self) -> str:
        """End-to-end execution for reading requirements and producing output."""

        requirements = self.read_requirements(self._settings.requirement_file)
        return self.generate_regression_test_cases(requirements=requirements)
