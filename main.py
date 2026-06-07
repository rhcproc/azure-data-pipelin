from __future__ import annotations

from datetime import datetime, timezone

import requests

url = ""

requests.post(url, data={
    "name": "name1",
    "score": 195
})


def run_scheduled_task() -> str:
    """Run the work that should happen on each timer tick."""
    timestamp = datetime.now(timezone.utc).isoformat()
    return f"Hourly scheduled task ran at {timestamp}"
