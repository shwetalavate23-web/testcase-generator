# Changelog

## Unreleased

- Add web application entrypoint in `main.py` using `run_web_app()`.
- Ensure `localhost:8000` UI can load before API key is configured.
- Remove deprecated/removed `cgi` dependency from multipart parsing.
- Enforce generated output filename to always be `output.md`.
- Preserve modular architecture (`config.py`, `prompt.py`, `agent.py`, `webapp.py`).
