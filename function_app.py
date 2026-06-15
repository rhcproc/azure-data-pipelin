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


@app.event_grid_trigger(arg_name="event")
def process_bronze(event: func.EventGridEvent):
    logging.warning("🔥 EVENT GRID TRIGGER FIRED")

    data = event.get_json()
    logging.warning(f"Event type: {event.event_type}")
    logging.warning(f"Subject: {event.subject}")
    logging.warning(f"Data: {data}")

    blob_url = data.get("url")
    logging.warning(f"Blob URL: {blob_url}")
