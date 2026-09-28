"""Minimal HTTP service for the starter app pipeline demo."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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


def get_ui_html() -> str:
    """Return interactive calculator UI HTML."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2em;
            text-align: center;
        }
        .subtitle {
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #2c3e50;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 0.95em;
        }
        select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        .input-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .input-row input {
            width: 100%;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 10px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f0f7ff;
            border-left: 5px solid #667eea;
            border-radius: 8px;
            display: none;
        }
        .result.show {
            display: block;
        }
        .result-label {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .result-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            font-family: 'Courier New', monospace;
        }
        .error {
            background: #ffe0e0 !important;
            border-left-color: #d73814 !important;
            margin-top: 20px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .error-text {
            color: #d73814;
            font-weight: 600;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 10px;
        }
        .loading.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Calculator</h1>
        <p class="subtitle">Powered by Starter App API</p>
        
        <form id="calcForm" onsubmit="calculate(event)">
            <div class="form-group">
                <label for="operation">Operation</label>
                <select id="operation" required>
                    <option value="">Choose operation...</option>
                    <option value="add">Add (+)</option>
                    <option value="subtract">Subtract (-)</option>
                    <option value="multiply">Multiply (×)</option>
                    <option value="divide">Divide (÷)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Numbers</label>
                <div class="input-row">
                    <input type="number" id="a" placeholder="First number" step="any" required>
                    <input type="number" id="b" placeholder="Second number" step="any" required>
                </div>
            </div>
            
            <button type="submit">Calculate</button>
            <div class="loading" id="loading">Calculating...</div>
        </form>
        
        <div class="result" id="result">
            <div class="result-label">Result</div>
            <div class="result-value" id="resultValue">0</div>
        </div>
        
        <div class="error" id="error">
            <div class="error-text" id="errorText">Error</div>
        </div>
    </div>
    
    <script>
        async function calculate(event) {
            event.preventDefault();
            
            const operation = document.getElementById('operation').value;
            const a = document.getElementById('a').value;
            const b = document.getElementById('b').value;
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            
            loading.classList.add('show');
            result.classList.remove('show');
            error.classList.remove('show');
            
            try {
                const response = await fetch(`/calculate?op=${operation}&a=${a}&b=${b}`);
                const data = await response.json();
                
                loading.classList.remove('show');
                
                if (!response.ok) {
                    error.classList.add('show');
                    document.getElementById('errorText').textContent = data.error || 'Error';
                } else {
                    result.classList.add('show');
                    document.getElementById('resultValue').textContent = data.result;
                }
            } catch (err) {
                loading.classList.remove('show');
                error.classList.add('show');
                document.getElementById('errorText').textContent = 'Connection error';
            }
        }
    </script>
</body>
</html>"""


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
        
        # Serve UI for /ui path
        if parsed.path == "/ui":
            body = get_ui_html().encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        
        # Serve JSON for API paths
        status, payload = build_response(parsed.path, parse_qs(parsed.query))
        body = json.dumps(payload, indent=2).encode("utf-8")

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
