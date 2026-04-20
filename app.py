from fastapi import FastAPI

from api.routes.sessions import router as session_router
from api.routes.queries import router as queries_router
from api.routes.operations import router as operations_router


app = FastAPI(title="FastAPI Session Auth")

app.include_router(session_router)
app.include_router(queries_router)
app.include_router(operations_router)


@app.get("/")
def root():
    return {"message": "API is running"}