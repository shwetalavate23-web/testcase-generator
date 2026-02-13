"""Web app for managing requirements and generating regression test cases."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote_plus, unquote_plus, urlparse
import cgi

from agent import RegressionTestCaseAgent
from config import load_settings


class RegressionWebHandler(BaseHTTPRequestHandler):
    """HTTP handler for requirement management and test case generation."""

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found")
            return

        try:
            settings = load_settings(require_api_key=False)
            requirement_text = ""
            if settings.requirement_file.exists():
                requirement_text = settings.requirement_file.read_text(encoding="utf-8")

            query = parse_qs(parsed.query)
            message = query.get("message", [""])[0]
            body = self._render_index(requirement_text=requirement_text, message=unquote_plus(message))
            self._send_html(body)
        except Exception as exc:  # pragma: no cover - defensive top-level request handling
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/save-requirement":
            self._save_requirement()
            return
        if parsed.path == "/generate":
            self._generate_output()
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Route not found")

    def _save_requirement(self) -> None:
        settings = load_settings(require_api_key=False)
        content_type = self.headers.get("Content-Type", "")

        content = ""
        if content_type.startswith("multipart/form-data"):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type},
            )

            uploaded = form["requirement_file"] if "requirement_file" in form else None
            text_value = form.getvalue("requirement_text", "")

            if uploaded is not None and getattr(uploaded, "filename", ""):
                content = uploaded.file.read().decode("utf-8").strip()
            elif isinstance(text_value, str):
                content = text_value.strip()
        else:
            length = int(self.headers.get("Content-Length", "0"))
            payload = self.rfile.read(length).decode("utf-8")
            data = parse_qs(payload)
            content = data.get("requirement_text", [""])[0].strip()

        if not content:
            self._redirect("/?message=" + quote_plus("Please upload a file or enter requirement text."))
            return

        settings.requirement_file.write_text(content + "\n", encoding="utf-8")
        self._redirect("/?message=" + quote_plus(f"Saved requirements to {settings.requirement_file}."))

    def _generate_output(self) -> None:
        try:
            settings = load_settings(require_api_key=True)
            agent = RegressionTestCaseAgent(settings=settings)

            output = agent.run()
            output_path = settings.output_file
            output_path.write_text(output + "\n", encoding="utf-8")

            payload = output_path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="{output_path.name}"')
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:
            self._redirect("/?message=" + quote_plus(f"Generation failed: {exc}"))

    def _send_html(self, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    @staticmethod
    def _render_index(requirement_text: str, message: str) -> str:
        safe_text = (
            requirement_text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        safe_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Regression Test Case Generator</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 900px; }}
      h1 {{ margin-bottom: 0.5rem; }}
      form {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }}
      textarea {{ width: 100%; min-height: 220px; }}
      button {{ padding: 0.6rem 1rem; cursor: pointer; }}
      .msg {{ color: #0b6; margin: 0.7rem 0; white-space: pre-wrap; }}
    </style>
  </head>
  <body>
    <h1>Business Regression Test Case Generator</h1>
    <p>Upload a user-story file or paste the user story text, then generate regression test cases.</p>
    {f'<p class="msg">{safe_message}</p>' if safe_message else ''}

    <form method=\"post\" action=\"/save-requirement\" enctype=\"multipart/form-data\">
      <h2>Step 1: Upload or Enter User Story</h2>
      <p><input type=\"file\" name=\"requirement_file\" accept=\".txt,.md,.text\" /></p>
      <p>OR</p>
      <textarea name=\"requirement_text\" placeholder=\"Paste user story / functional requirements here...\">{safe_text}</textarea>
      <p><button type=\"submit\">Save User Story</button></p>
    </form>

    <form method=\"post\" action=\"/generate\">
      <h2>Step 2: Generate Regression Test Cases</h2>
      <button type=\"submit\">Generate</button>
    </form>
  </body>
</html>"""


def run_web_app(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run the HTTP web application."""

    server = ThreadingHTTPServer((host, port), RegressionWebHandler)
    print(f"Web app running at http://{host}:{port}")
    server.serve_forever()
