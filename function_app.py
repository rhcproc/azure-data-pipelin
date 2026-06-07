import logging

import azure.functions as func

# from etl.bronze import run_scheduled_task as run_bronze_task

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def simple_writer(timer: func.TimerRequest) -> None:
    try:
        logging.info("[APP] Function started")

        if timer.past_due:
            logging.warning("[APP] Timer is past due")

        from settings import settings

        res = settings.values["AzureStorageConnectionString"]

        logging.info(f"[APP] Loaded secret: {res[:4]}...{res[-4:]}")
        logging.info("[APP] Function finished")

    except Exception:
        logging.exception("[APP] Function failed")
        raise