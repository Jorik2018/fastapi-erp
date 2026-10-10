import os

from fastapi_erp.vault import get_vault_secret

VAULT_GLOBAL_PATH = "secret/data/global"

def _get_vault_secret(path: str) -> dict:
    if os.getenv("MOCK_VAULT", "false").lower() == "true":
        from fastapi_erp.mocks.vault import get_vault_secret as get_vault_secret_mock
        return get_vault_secret_mock(path)
    return get_vault_secret(path)

def get_database_url() -> str:
    database_url = _get_vault_secret(VAULT_GLOBAL_PATH).get("MYSQL_URL")#DATABASE_URL
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured in Vault"
        )
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )
    if database_url.startswith("mysql://"):
        database_url = database_url.replace(
            "mysql://",
            "mysql+pymysql://",
            1,
        )
    return database_url


def get_jwt_public_key_location() -> str:
    location = _get_vault_secret(VAULT_GLOBAL_PATH).get("JWT_PUBLIC_KEY_LOCATION")
    if not location:
        raise RuntimeError(
            "JWT_PUBLIC_KEY_LOCATION is not configured in Vault"
        )
    return location