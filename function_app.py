import logging

import azure.functions as func
from settings import settings
# from etl.bronze import run_scheduled_task as run_bronze_task

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def simple_writer(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("simple-writer timer trigger is past due.")
    res = settings.values["AzureStorageConnectionString"]
    logging.info(f"Loaded secret from Key Vault: {res[:4]}...{res[-4:]}")
    logging.info("simple-writer timer trigger function ran")
    # result = run_bronze_task()
    # logging.info(result)
