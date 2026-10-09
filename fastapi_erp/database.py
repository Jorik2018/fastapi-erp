import os
import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware

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
    
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except HTTPException as http_exc:
            response = http_exc
        except Exception as exc:
            traceback.print_exc()
            response = JSONResponse(status_code=500, content={"message": "Server error"})
        if hasattr(request.state, "db") and request.state.db:
            close(request.state.db)
        return response

def set_fields_from_dict(obj, data: dict):
    for key, value in data.items():
        if hasattr(obj, key):
            print(key)
            setattr(obj, key, value)

load_dotenv()

__DB_URL = os.getenv("DATABASE_URL")

__engine = create_engine(__DB_URL)

__sessionmaker:sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=__engine)

Base = declarative_base()

Base.metadata.create_all(bind=__engine)

def persist(self: Session, item):
    self.add(item)
    self.flush()
    self.refresh(item)
    return item

def merge_custom(self: Session, item):
    merged_item = self.original_merge(item)
    self.flush()
    self.refresh(merged_item)
    return item

def get_db(request: Request):
    db: Session = __sessionmaker()#Session(__engine)
    db.persist = persist.__get__(db, Session)
    db.original_merge = db.merge
    db.merge = merge_custom.__get__(db, Session)
    db.begin()
    request.state.db = db
    print('create db')
    try:
        yield db
    finally:
        db.close()
        #close(db)
        print('close get_db')