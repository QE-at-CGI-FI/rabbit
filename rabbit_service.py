"""Rabbit compute service — internal only, no auth."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Rabbit Compute Service", docs_url=None, redoc_url=None)

_RABBIT_SCRIPT = Path(__file__).parent / "rabbit.py"


class Result(BaseModel):
    result: int


@app.get("/compute/{n}", response_model=Result)
def compute(n: int) -> Result:
    if n < 1 or n > 1473:
        raise HTTPException(status_code=422, detail="n out of range (1–1473).")
    proc = subprocess.run(
        [sys.executable, str(_RABBIT_SCRIPT), str(n)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=proc.stderr.strip())
    return Result(result=int(proc.stdout.strip()))
