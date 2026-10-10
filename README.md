https://medium.com/@caetanoog/start-your-first-fastapi-server-with-poetry-in-10-minutes-fef90e9604d9
https://medium.com/@konstantine.dvalishvil/transactional-methods-fastapi-sqlalchemy-6f33370b95dd
https://stackoverflow.com/questions/72243379/fastapi-dependency-inside-middleware
https://www.encode.io/databases/database_queries/
https://stackoverflow.com/questions/63853813/how-to-create-routes-with-fastapi-within-a-class
https://pythonnest.github.io/PyNest/blank/
https://stackoverflow.com/questions/61153498/what-is-the-good-way-to-provide-an-authentication-in-fastapi
https://medium.com/@seymaaozlerr/building-an-authentication-system-with-fastapi-redis-and-mysql-cc8b005b9c30

brew install openssl

poetry install
poetry add psycopg2-binary
poetry add asyncpg
poetry remove databases
poetry add sqlalchemy
poetry run uvicorn fastapi_erp:app --reload

Api Doc
http://localhost:8000/docs#/Book

https://github.com/tiangolo/full-stack-fastapi-postgresql
https://medium.com/@shubhkarmanrathore/mastering-crud-operations-with-sqlalchemy-a-comprehensive-guide-a05cf70e5dea
https://dev.to/uponthesky/python-post-reviewhow-to-implement-a-transactional-decorator-in-fastapi-sqlalchemy-ein
https://stackoverflow.com/questions/65699977/fastapi-sqlalchemy-how-to-manage-transaction-session-and-multiple-commits



# async def verify_key(x_key: Annotated[str, Header(1)]):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# app = FastAPI(dependencies=[Depends(verify_key)])
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response

# #@app.middleware("http")
# async def custom_middleware(request: Request, call_next):
#     try:
#         response = await call_next(request)
#     except HTTPException as http_exc:
#         response = http_exc
#     except Exception as exc:
#         traceback.print_exc()
#         response = JSONResponse(status_code=500, content={"message": "Server error"})
#     if hasattr(request.state, "db") and request.state.db:
#         db: Session = request.state.db
#         try:
#             db.commit()
#         except Exception as commit_exc:
#             db.rollback()
#             raise commit_exc
#         finally:
#             db.close()
#     return response



MOCK_VAULT=true poetry run uvicorn fastapi_erp:app --reload