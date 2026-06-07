import json
from datetime import datetime
from azure.storage.filedatalake import DataLakeServiceClient

from settings import settings


def run_scheduled_task() -> str:
    # Azure Storage Connection String
    CONNECTION_STRING = settings.values["AzureStorageConnectionString"]

    # Create clients
    service_client = DataLakeServiceClient.from_connection_string(
        CONNECTION_STRING
    )

    # bronze container
    file_system_client = service_client.get_file_system_client(
        file_system="bronze"
    )

    # Example data
    data = {
        "symbol": "BTCUSDT",
        "price": 105001,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Path in Data Lake
    file_path = (
        f"crypto/{data['symbol']}.json"
    )

    # Create file
    file_client = file_system_client.get_file_client(file_path)

    # Upload
    file_client.upload_data(
        json.dumps(data),
        overwrite=True
    )

    return f"simple-writer timer ran at {datetime.utcnow().isoformat()}; wrote data to {file_path}"


if __name__ == "__main__":
    result = run_scheduled_task()
    print(result)