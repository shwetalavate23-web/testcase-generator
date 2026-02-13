# Business-Scenario Regression Test Case Generator

This project provides a web application that generates **business-scenario-oriented regression test cases** from functional requirements in `requirement.txt` using OpenAI.

## Project Structure

- `main.py` - Web app entry point
- `webapp.py` - HTTP routes and UI
- `agent.py` - LLM agent logic
- `prompt.py` - Prompt template definitions
- `config.py` - On-demand environment configuration loading
- `requirement.txt` - Input functional requirements/user stories
- `output.md` - Generated regression test suite download target
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
OUTPUT_FILE=output.md
```

## Run

```bash
python main.py
```

Open: `http://localhost:8000`

## Usage

1. Upload a file or paste user stories in the textbox and click **Save User Story** (writes to `requirement.txt`).
2. Click **Generate**.
3. The app runs the LLM agent, writes generated regression test cases to `output.md`, and automatically downloads `output.md`.
