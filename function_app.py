import logging

import azure.functions as func

# from etl.bronze import run_scheduled_task as run_bronze_task

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */2 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def simple_writer(timer: func.TimerRequest) -> None:
    try:
        logging.info("[APP] Function started")

        if timer.past_due:
            logging.warning("[APP] Timer is past due")

        # from settings import settings
        # res = settings.values["AzureStorageConnectionString"]
        # logging.info(f"[APP] Loaded secret: {res[:4]}...{res[-4:]}")
        from etl.bronze import run_scheduled_task as run_bronze_task

        bronze_result = run_bronze_task()
        logging.info(f"[APP] Bronze task result: {bronze_result}")

        logging.info("[APP] Function finished")

    except Exception:
        logging.exception("[APP] Function failed")
        raise


@app.blob_trigger(
    arg_name="blob",
    path="bronze/crypto/{name}",
    connection="AzureStorageConnectionString",
    source="EventGrid",
)
def process_bronze(blob: func.InputStream) -> None:
    # try:
    #     logging.info(f"[APP] Processing bronze blob: {blob.name}")

    #     from etl.silver import run_scheduled_task as run_silver_task

    #     result = run_silver_task(
    #         source_name=blob.name,
    #         raw_data=blob.read(),
    #     )
    #     logging.info(f"[APP] Silver task result: {result}")

    # except Exception:
    #     logging.exception("[APP] Silver task failed")
    #     raise
    logging.info("=== BLOB TRIGGER FIRED ===")
    logging.info(f"Blob name: {blob.name}")
    logging.info(f"Blob size: {blob.length}")
