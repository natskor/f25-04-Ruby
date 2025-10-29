#FastAPI app
from fastapi import FastAPI
from backend.routes import collabrewards_route

app = FastAPI()

app.include_router(collabrewards_route.router)