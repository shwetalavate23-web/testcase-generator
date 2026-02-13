"""Entry point for the business-scenario regression test case generator."""

from __future__ import annotations

from agent import RegressionTestCaseAgent
from config import load_settings


def main() -> None:
    settings = load_settings()
    agent = RegressionTestCaseAgent(settings=settings)

    output = agent.run()
    settings.output_file.write_text(output + "\n", encoding="utf-8")

    print(f"Regression test cases generated successfully: {settings.output_file}")


if __name__ == "__main__":
    main()
