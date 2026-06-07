from __future__ import annotations

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class KeyVaultValues:
    def __init__(self, app_settings: AppSettings) -> None:
        self._app_settings = app_settings

    def __getitem__(self, secret_name: str) -> str:
        return self._app_settings.get_key_vault_secret(secret_name)

    def get(self, secret_name: str, default: str | None = None) -> str | None:
        try:
            return self[secret_name]
        except Exception:
            return default


class AppSettings:
    def __init__(
        self,
        key_vault_url: str | None = None,
        default_secret_name: str | None = None,
    ) -> None:
        self._key_vault_url = key_vault_url
        self._default_secret_name = default_secret_name
        self._secret_client: SecretClient | None = None
        self._values = KeyVaultValues(self)

    @property
    def key_vault_url(self) -> str:
        if not self._key_vault_url:
            raise RuntimeError("Missing required setting: key_vault_url")
        return self._key_vault_url

    @property
    def values(self) -> KeyVaultValues:
        return self._values

    @property
    def secret_client(self) -> SecretClient:
        if self._secret_client is None:
            credential = DefaultAzureCredential()
            self._secret_client = SecretClient(
                vault_url=self.key_vault_url,
                credential=credential,
            )
        return self._secret_client

    def get_key_vault_secret(self, secret_name: str | None = None) -> str:
        name = secret_name or self._default_secret_name
        if not name:
            raise RuntimeError("Missing required setting: secret_name")
        return self.secret_client.get_secret(name).value


settings = AppSettings(
    key_vault_url="https://trigger-base-kv.vault.azure.net/",
)


if __name__ == "__main__":
    key_vault_settings = AppSettings(
        key_vault_url="https://trigger-base-kv.vault.azure.net/",
    )
    print(key_vault_settings.values["AzureStorageConnectionString"])
