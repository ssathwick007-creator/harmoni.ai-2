"""Minimal runnable HTTP service for harmoni.ai-2."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class HarmoniRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with health and root endpoints."""

    server_version = "harmoni-ai/0.1"

    def _write_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802 (http server naming convention)
        if self.path == "/health":
            self._write_json({"status": "ok"})
            return

        if self.path == "/":
            self._write_json(
                {
                    "name": "harmoni.ai-2",
                    "message": "Service is running",
                    "endpoints": ["/", "/health"],
                }
            )
            return

        self._write_json(
            {
                "error": "not_found",
                "message": f"Path {self.path!r} was not found",
            },
            status=HTTPStatus.NOT_FOUND,
        )

    def log_message(self, format: str, *args: object) -> None:
        """Keep test output clean by suppressing default request logs."""


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run the HTTP server."""

    server = ThreadingHTTPServer((host, port), HarmoniRequestHandler)
    print(f"harmoni.ai-2 listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the harmoni.ai-2 service")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
