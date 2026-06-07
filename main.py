from datetime import datetime, timezone


def run_scheduled_task() -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    return f"simple-writer timer ran at {timestamp}"
