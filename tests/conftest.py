"""Shared fixtures: starts a dedicated test server on port 8001."""
import subprocess
import time
from pathlib import Path

import pytest
import requests

PROJECT_ROOT = Path(__file__).parent.parent
BASE_URL = "http://localhost:8001"


@pytest.fixture(scope="session", autouse=True)
def server():
    """Start a fresh uvicorn process on port 8001 for the test session."""
    proc = subprocess.Popen(
        [str(PROJECT_ROOT / ".venv/bin/uvicorn"), "main:app", "--port", "8001"],
        cwd=PROJECT_ROOT,
    )
    for _ in range(30):
        try:
            requests.get(f"{BASE_URL}/rabbit/1", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.3)
    else:
        proc.terminate()
        raise RuntimeError("Test server did not start in time.")

    yield

    proc.terminate()
    proc.wait()
