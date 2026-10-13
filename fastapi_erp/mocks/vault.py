# fastapi_erp/mocks/vault.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
def get_vault_secret(_path: str) -> dict:
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "JWT_PUBLIC_KEY_LOCATION": os.getenv("JWT_PUBLIC_KEY_LOCATION"),
        "MYSQL_URL": os.getenv("MYSQL_URL")
    }