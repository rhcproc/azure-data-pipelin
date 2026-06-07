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

The app also reads a secret from Azure Key Vault. Set these app settings locally
in `local.settings.json` and in the deployed Function App configuration:

```json
"KEY_VAULT_URL": "https://<your-vault-name>.vault.azure.net/",
"KEY_VAULT_SECRET_NAME": "<your-secret-name>"
```

For local development, sign in with the Azure CLI or another
`DefaultAzureCredential` source:

```bash
az login
```

In Azure, enable a system-assigned managed identity on the Function App and
grant it permission to read secrets from the Key Vault.

If port `7071` is already in use, start with another port:

```bash
func start --python --port 7073
```

The timer schedule is defined in `function_app.py`:

```python
schedule="0 */30 * * * *"
```

That NCRONTAB expression means “run at second `0`, every 30 minutes.”

The function entry point is `function_app.py`; the business logic lives in
`main.py`.
