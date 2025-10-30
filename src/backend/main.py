#FastAPI app
from fastapi import FastAPI
from backend.routes import collabrewards_routes, signup_routes, login_routes, calendar_routes, rewards_store_routes

app = FastAPI()

app.include_router(collabrewards_routes.router)
app.include_router(signup_routes.router)
app.include_router(login_routes.router)
app.include_router(calendar_routes.router)
app.include_router(rewards_store_routes.router)