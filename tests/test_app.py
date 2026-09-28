import pytest

from src.app import build_response


def test_healthcheck_response():
    status, payload = build_response("/health", {}, {"APP_VERSION": "1.2.3", "APP_ENV": "test"})

    assert status.value == 200
    assert payload == {
        "status": "ok",
        "service": {
            "name": "starter-app",
            "version": "1.2.3",
            "environment": "test",
            "port": "8000",
        },
    }


def test_root_response_lists_endpoints():
    status, payload = build_response("/", {}, {"APP_NAME": "capstone-calculator"})

    assert status.value == 200
    assert payload["service"]["name"] == "capstone-calculator"
    assert payload["endpoints"]["calculate"].startswith("/calculate")


def test_operations_response():
    status, payload = build_response("/operations", {})

    assert status.value == 200
    assert payload["operations"] == ["add", "divide", "multiply", "subtract"]


def test_calculate_response():
    status, payload = build_response("/calculate", {"op": ["multiply"], "a": ["4"], "b": ["3"]})

    assert status.value == 200
    assert payload["service"]["version"] == "dev"
    assert payload["result"] == 12


def test_calculate_missing_argument():
    status, payload = build_response("/calculate", {"op": ["add"], "a": ["2"]})

    assert status.value == 400
    assert payload == {"error": "Missing parameter: b"}


def test_calculate_divide_by_zero():
    status, payload = build_response("/calculate", {"op": ["divide"], "a": ["10"], "b": ["0"]})

    assert status.value == 400
    assert payload == {"error": "Cannot divide by zero"}


def test_unknown_route():
    status, payload = build_response("/missing", {})

    assert status.value == 404
    assert payload == {"error": "Not found"}