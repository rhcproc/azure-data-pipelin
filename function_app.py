import logging

import azure.functions as func

from main import run_scheduled_task

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

    result = run_scheduled_task()
    logging.info(result)
