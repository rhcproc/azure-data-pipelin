import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from azure.storage.filedatalake import DataLakeServiceClient

from settings import settings


BRONZE_FILE_SYSTEM = "bronze"
SILVER_FILE_SYSTEM = "silver"
CRYPTO_SYMBOL = "BTCUSDT"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _to_decimal(value: Any) -> str:
    try:
        return str(Decimal(str(value)))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid price value: {value!r}") from exc


def _bronze_path(blob_name: str) -> str:
    return blob_name.removeprefix(f"{BRONZE_FILE_SYSTEM}/")


def _load_bronze_data(
    service_client: DataLakeServiceClient,
    source_path: str,
    raw_data: bytes | str | None,
) -> dict[str, Any]:
    if raw_data is not None:
        return json.loads(raw_data)

    bronze_client = service_client.get_file_system_client(
        file_system=BRONZE_FILE_SYSTEM
    )
    bronze_file = bronze_client.get_file_client(source_path)
    return json.loads(bronze_file.download_file().readall())


def run_scheduled_task(
    source_name: str | None = None,
    raw_data: bytes | str | None = None,
) -> str:
    connection_string = settings.values["AzureStorageConnectionString"]
    service_client = DataLakeServiceClient.from_connection_string(
        connection_string
    )

    silver_client = service_client.get_file_system_client(
        file_system=SILVER_FILE_SYSTEM
    )

    source_path = _bronze_path(source_name or f"crypto/{CRYPTO_SYMBOL}.json")
    bronze_data = _load_bronze_data(service_client, source_path, raw_data)

    symbol = str(bronze_data["symbol"]).upper()
    silver_data = {
        "symbol": symbol,
        "price": _to_decimal(bronze_data["price"]),
        "source_timestamp": bronze_data["timestamp"],
        "processed_timestamp": _utc_now(),
        "source_layer": BRONZE_FILE_SYSTEM,
    }

    target_path = source_path
    silver_file = silver_client.get_file_client(target_path)
    silver_file.upload_data(
        json.dumps(silver_data),
        overwrite=True,
    )

    return (
        f"simple-writer silver task ran at {_utc_now()}; "
        f"wrote data to {SILVER_FILE_SYSTEM}/{target_path}"
    )


if __name__ == "__main__":
    result = run_scheduled_task()
    print(result)
