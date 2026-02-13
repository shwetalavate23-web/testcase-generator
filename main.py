"""Entry point for the business-scenario regression test case generator."""

from __future__ import annotations

from webapp import run_web_app


def main() -> None:
    run_web_app(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
