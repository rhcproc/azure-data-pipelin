# simple-writer

Minimal Python Azure Functions app with a timer trigger that runs once per hour.

## Run locally

Install dependencies:

```bash
venv/bin/python -m pip install -r requirements.txt
```

Start the Azure Functions host:

```bash
func start --python
```

Timer triggers use `AzureWebJobsStorage` when schedule monitoring is enabled.
For local development, start Azurite first or replace `AzureWebJobsStorage` in
`local.settings.json` with a real Azure Storage connection string.

If port `7071` is already in use, start with another port:

```bash
func start --python --port 7073
```

The timer schedule is defined in `function_app.py`:

```python
schedule="0 0 * * * *"
```

That NCRONTAB expression means “run at second `0`, minute `0`, every hour.”

The function entry point is `function_app.py`; the business logic lives in
`main.py`.
