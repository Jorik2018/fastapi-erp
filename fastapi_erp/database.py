import os
import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_erp.config import get_database_url


Base = declarative_base()

__engine = None

__sessionmaker = None

def close(db: Session):
    try:
        db.flush()
        db.commit()
    except Exception as commit_exc:
        db.rollback()
        raise commit_exc
    finally:
        db.close()


class DBMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, some_attribute: str):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)

            if hasattr(request.state, "db") and request.state.db:
                request.state.db.commit()

            return response

        except HTTPException:
            if hasattr(request.state, "db") and request.state.db:
                request.state.db.rollback()
            raise

        except Exception:
            if hasattr(request.state, "db") and request.state.db:
                request.state.db.rollback()

            traceback.print_exc()

            return JSONResponse(
                status_code=500,
                content={"message": "Server error"}
            )

        finally:
            if hasattr(request.state, "db") and request.state.db:
                request.state.db.close()

def set_fields_from_dict(obj, data: dict):
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)


def get_sessionmaker():
    global __engine
    global __sessionmaker

    if __sessionmaker is None:
        print("Initializing database")

        database_url = get_database_url()

        __engine = create_engine(database_url)

        if os.getenv("MOCK_VAULT", "false").lower() == "true":
            Base.metadata.create_all(bind=__engine)

        __sessionmaker = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=__engine
        )

    return __sessionmaker


def persist(self: Session, item):
    self.add(item)
    self.flush()
    self.refresh(item)
    return item


def merge_custom(self: Session, item):
    merged_item = self.original_merge(item)
    self.flush()
    self.refresh(merged_item)
    return merged_item


def get_db(request: Request):
    SessionLocal = get_sessionmaker()

    db: Session = SessionLocal()

    db.persist = persist.__get__(db, Session)
    db.original_merge = db.merge
    db.merge = merge_custom.__get__(db, Session)

    request.state.db = db

    print("create db")

    try:
        yield db

    finally:
        print("close get_db")