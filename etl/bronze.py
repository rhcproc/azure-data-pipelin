import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient

from settings import settings


def run_scheduled_task() -> str:
    # Azure Storage Connection String
    CONNECTION_STRING = settings.values["AzureStorageConnectionString"]

    # Create clients
    service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING
    )

    # bronze container
    container_client = service_client.get_container_client("bronze")

    # Example data
    data = {
        "symbol": "BTCUSDT",
        "price": 105001,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Path in Blob Storage
    blob_path = (
        f"crypto/{data['symbol']}.json"
    )

    # Create blob client
    blob_client = container_client.get_blob_client(blob_path)

    # Upload
    blob_client.upload_blob(
        json.dumps(data),
        overwrite=True
    )

    return f"simple-writer timer ran at {datetime.utcnow().isoformat()}; wrote data to {blob_path}"


if __name__ == "__main__":
    result = run_scheduled_task()
    print(result)
