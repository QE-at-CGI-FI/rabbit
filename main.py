"""Rabbit API."""
from __future__ import annotations

import os
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(
    title="Rabbit API",
    version="1.0.0",
    description="What does the rabbit return?",
)


_API_KEY = os.environ.get("API_SECRET", "aaa")
_RABBIT_SERVICE_URL = os.environ.get("RABBIT_SERVICE_URL", "http://localhost:8080")
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: str = Security(_api_key_header)) -> None:
    if key != _API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


class RabbitResult(BaseModel):
    input: int
    result: int


_RABBIT_SCRIPT = Path(__file__).parent / "rabbit.py"


@app.get("/rabbit-ui", response_class=HTMLResponse, include_in_schema=False)
def rabbit_ui() -> HTMLResponse:
    """Interactive UI for exploring the rabbit endpoint."""
    rabbit_code = _RABBIT_SCRIPT.read_text()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Rabbit Explorer</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f0f1a;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem;
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 0.5rem;
      background: linear-gradient(135deg, #a78bfa, #60a5fa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .subtitle {{
      color: #94a3b8;
      text-align: center;
      margin-bottom: 2.5rem;
      font-size: 0.95rem;
    }}
    .layout {{
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 2rem;
      width: 100%;
      max-width: 1100px;
      align-items: start;
    }}
    .card {{
      background: #1e1e2e;
      border: 1px solid #2d2d44;
      border-radius: 16px;
      padding: 2rem;
    }}
    .card h2 {{
      font-size: 1rem;
      font-weight: 600;
      color: #a78bfa;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 1.5rem;
    }}
    .field-group {{
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}
    label {{
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.5rem;
    }}
    input[type="number"] {{
      width: 100%;
      padding: 0.75rem 1rem;
      background: #0f0f1a;
      border: 1px solid #3d3d5c;
      border-radius: 8px;
      color: #e2e8f0;
      font-size: 1.1rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    input[type="number"]:focus {{ border-color: #a78bfa; }}
    .output-box {{
      width: 100%;
      padding: 0.75rem 1rem;
      background: #0f0f1a;
      border: 1px solid #3d3d5c;
      border-radius: 8px;
      font-size: 1.4rem;
      font-weight: 700;
      font-family: 'Courier New', monospace;
      color: #60a5fa;
      min-height: 3rem;
      display: flex;
      align-items: center;
    }}
    .output-box.empty {{ color: #3d3d5c; font-size: 0.95rem; font-weight: 400; }}
    .output-box.error {{ color: #f87171; font-size: 0.9rem; font-weight: 400; }}
    button {{
      width: 100%;
      padding: 0.85rem;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      border: none;
      border-radius: 8px;
      color: white;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.2s, transform 0.1s;
    }}
    button:hover {{ opacity: 0.9; }}
    button:active {{ transform: scale(0.98); }}
    button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    .code-card {{
      background: #1e1e2e;
      border: 1px solid #2d2d44;
      border-radius: 16px;
      overflow: hidden;
    }}
    .code-card-header {{
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #2d2d44;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .code-card-header h2 {{
      font-size: 1rem;
      font-weight: 600;
      color: #a78bfa;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .dot-red {{ background: #f87171; }}
    .dot-yellow {{ background: #fbbf24; }}
    .dot-green {{ background: #34d399; }}
    pre {{
      padding: 1.5rem;
      overflow-x: auto;
      font-family: 'Courier New', 'Consolas', monospace;
      font-size: 0.82rem;
      line-height: 1.7;
      color: #c4b5fd;
      background: #13131f;
      margin: 0;
    }}
    @media (max-width: 768px) {{
      .layout {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <h1>What does the rabbit return?</h1>
  <p class="subtitle">Enter a positive integer and discover what emerges from the burrow.</p>

  <div class="layout">
    <div class="card">
      <h2>Experiment</h2>
      <div class="field-group">
        <div>
          <label for="n-input">Input</label>
          <input type="number" id="n-input" min="1" max="1473" placeholder="Enter a positive integer" />
        </div>
        <button id="run-btn" onclick="runRabbit()">Ask the rabbit</button>
        <div>
          <label>Output</label>
          <div class="output-box empty" id="output">—</div>
        </div>
      </div>
    </div>

    <div class="code-card">
      <div class="code-card-header">
        <div class="dot dot-red"></div>
        <div class="dot dot-yellow"></div>
        <div class="dot dot-green"></div>
        <h2 style="margin-left:0.5rem;">rabbit.py</h2>
      </div>
      <pre id="code-display">{rabbit_code}</pre>
    </div>
  </div>

  <script>
    async function runRabbit() {{
      const btn = document.getElementById('run-btn');
      const out = document.getElementById('output');
      const n = parseInt(document.getElementById('n-input').value, 10);
      if (!n || n < 1) {{
        out.textContent = 'Please enter a positive integer.';
        out.className = 'output-box error';
        return;
      }}

      btn.disabled = true;
      btn.textContent = 'Running…';
      out.textContent = '…';
      out.className = 'output-box empty';

      try {{
        const res = await fetch(`/rabbit/${{n}}`, {{
          headers: {{ 'X-API-Key': 'aaa' }},
        }});
        const data = await res.json();
        if (!res.ok) {{
          out.textContent = data.detail || 'Error ' + res.status;
          out.className = 'output-box error';
        }} else {{
          out.textContent = data.result;
          out.className = 'output-box';
        }}
      }} catch (e) {{
        out.textContent = 'Network error: ' + e.message;
        out.className = 'output-box error';
      }} finally {{
        btn.disabled = false;
        btn.textContent = 'Ask the rabbit';
      }}
    }}

    document.getElementById('n-input').addEventListener('keydown', e => {{
      if (e.key === 'Enter') runRabbit();
    }});
  </script>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get(
    "/rabbit/{n}",
    response_model=RabbitResult,
    summary="I take a number and return a number but what am I?",
    tags=["rabbit"],
)
def rabbit(n: int, _: None = Security(require_api_key)) -> RabbitResult:
    """Do what rabbit.py does."""
    if n < 1:
        raise HTTPException(status_code=422, detail="n must be a positive integer.")
    if n > 1473:
        raise HTTPException(status_code=422, detail="n is too large; maximum supported value is 1473.")
    try:
        resp = requests.get(f"{_RABBIT_SERVICE_URL}/compute/{n}", timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RabbitResult(input=n, result=resp.json()["result"])
