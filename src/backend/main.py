#FastAPI app
from fastapi import FastAPI
from backend.routes import collabrewards_routes, signup_routes, login_routes

app = FastAPI()

app.include_router(collabrewards_routes.router)
app.include_router(signup_routes.router)
app.include_router(login_routes.router)