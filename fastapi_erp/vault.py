import os
import requests



def get_vault_secret(path: str) -> dict:
    VAULT_ADDR = os.getenv("VAULT_ADDR")
    VAULT_TOKEN = os.getenv("VAULT_TOKEN")
    if not VAULT_ADDR:
        raise RuntimeError("VAULT_ADDR is not configured")

    if not VAULT_TOKEN:
        raise RuntimeError("VAULT_TOKEN is not configured")

    url = f"{VAULT_ADDR}/v1/{path}"

    print(url)

    response = requests.get(
        url,
        headers={
            "X-Vault-Token": VAULT_TOKEN,
        },
        timeout=5,
    )

    response.raise_for_status()

    payload = response.json()

    # Para KV v2
    return payload["data"]["data"]