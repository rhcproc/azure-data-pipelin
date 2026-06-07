import logging

import azure.functions as func

# from main import run_scheduled_task
from etl.bronze import run_scheduled_task as run_bronze_task

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */2 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def simple_writer(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("simple-writer timer trigger is past due.")
    logging.info("simple-writer timer trigger function ran at %s", timer.schedule_status.last)
    result = run_bronze_task()
    logging.info(result)


# Function 2
# @app.blob_trigger(
#     arg_name="inputblob",
#     path="bronze/crypto/{name}",
#     connection="AzureWebJobsStorage"
# )
# def bronze_to_silver(inputblob):
#     ...
#     save_to_silver(...)


if __name__ == "__main__":
    bronze_result = run_bronze_task()
    logging.info(bronze_result)
    # print(bronze_result)
