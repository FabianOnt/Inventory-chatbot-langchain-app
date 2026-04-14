from fastapi import FastAPI
from api.routes.sessions import router as session_router

app = FastAPI(title="FastAPI Session Auth")

# Register router
app.include_router(session_router)


@app.get("/")
def root():
    return {"message": "API is running"}