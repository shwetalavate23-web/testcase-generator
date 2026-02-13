# Business-Scenario Regression Test Case Generator

This project generates **business-scenario-oriented regression test cases** from functional requirements in `requirement.txt` using OpenAI.

## Project Structure

- `main.py` - Entry point
- `agent.py` - LLM agent logic
- `prompt.py` - Prompt template definitions
- `config.py` - On-demand environment configuration loading
- `requirement.txt` - Input functional requirements/user stories
- `.env` - Runtime configuration and secrets (do not commit real secrets)

## Setup

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OLLAMA_HOST=http://localhost:11434
REQUIREMENT_FILE=requirement.txt
OUTPUT_FILE=regression_test_cases.md
```

4. Populate `requirement.txt` with functional requirements.

## Run

```bash
python main.py
```

The generated regression suite is saved to the file configured by `OUTPUT_FILE`.
