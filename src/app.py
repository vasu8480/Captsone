"""Minimal HTTP service for the starter app pipeline demo."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlparse

from src.calculator import add, divide, multiply, subtract


Operation = Callable[[float, float], float]
OPERATIONS: dict[str, Operation] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


def load_runtime_metadata(environ: dict[str, str] | None = None) -> dict[str, str]:
    runtime_env = environ or os.environ
    return {
        "name": runtime_env.get("APP_NAME", "starter-app"),
        "version": runtime_env.get("APP_VERSION", "dev"),
        "environment": runtime_env.get("APP_ENV", "local"),
        "port": runtime_env.get("PORT", "8000"),
    }


def build_response(
    path: str,
    query: dict[str, list[str]],
    environ: dict[str, str] | None = None,
) -> tuple[HTTPStatus, dict[str, object]]:
    metadata = load_runtime_metadata(environ)

    if path == "/":
        return HTTPStatus.OK, {
            "service": metadata,
            "endpoints": {
                "health": "/health",
                "ready": "/ready",
                "operations": "/operations",
                "calculate": "/calculate?op=add&a=2&b=3",
            },
        }

    if path == "/health":
        return HTTPStatus.OK, {"status": "ok", "service": metadata}

    if path == "/ready":
        return HTTPStatus.OK, {"status": "ready", "service": metadata}

    if path == "/operations":
        return HTTPStatus.OK, {"operations": sorted(OPERATIONS.keys()), "service": metadata}

    if path != "/calculate":
        return HTTPStatus.NOT_FOUND, {"error": "Not found"}

    operation_name = query.get("op", [""])[0]
    operation = OPERATIONS.get(operation_name)
    if operation is None:
        return HTTPStatus.BAD_REQUEST, {"error": f"Unsupported operation: {operation_name}"}

    try:
        a = float(query["a"][0])
        b = float(query["b"][0])
    except KeyError as exc:
        return HTTPStatus.BAD_REQUEST, {"error": f"Missing parameter: {exc.args[0]}"}
    except (TypeError, ValueError):
        return HTTPStatus.BAD_REQUEST, {"error": "Parameters a and b must be numeric"}

    try:
        result = operation(a, b)
    except ValueError as exc:
        return HTTPStatus.BAD_REQUEST, {"error": str(exc)}

    return HTTPStatus.OK, {
        "service": metadata,
        "operation": operation_name,
        "a": a,
        "b": b,
        "result": result,
    }


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        status, payload = build_response(parsed.path, parse_qs(parsed.query))
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def run() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), CalculatorHandler)
    print(f"Serving {load_runtime_metadata()['name']} on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()