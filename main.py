from datetime import datetime, timezone

from settings import settings


def run_scheduled_task() -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    secret_value = settings.get_key_vault_secret()
    return f"simple-writer timer ran at {timestamp}; loaded Key Vault secret ({len(secret_value)} chars)"
