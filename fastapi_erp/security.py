# fastapi_erp/security.py

from functools import lru_cache

import jwt
from fastapi import HTTPException

from fastapi_erp.config import get_jwt_public_key_location


ISSUER = "https://example.com/issuer"


@lru_cache
def get_public_key() -> str:
    location = get_jwt_public_key_location()

    print(f"JWT public key: {location}")

    with open(location, "r", encoding="utf-8") as file:
        return file.read()


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            get_public_key(),
            algorithms=["RS256"],
            issuer=ISSUER,
        )

    except jwt.ExpiredSignatureError as exc:
        print("JWT ERROR: ExpiredSignatureError:", exc)
        raise HTTPException(401, "Token expired")

    except jwt.InvalidIssuerError as exc:
        print("JWT ERROR: InvalidIssuerError:", exc)
        raise HTTPException(401, "Invalid issuer")

    except jwt.InvalidSignatureError as exc:
        print("JWT ERROR: InvalidSignatureError:", exc)
        raise HTTPException(401, "Invalid signature")

    except jwt.InvalidTokenError as exc:
        print(
            "JWT ERROR:",
            type(exc).__name__,
            str(exc)
        )
        raise HTTPException(
            401,
            f"Invalid token: {type(exc).__name__}"
        )