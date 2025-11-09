# src/main.py

from fastapi import FastAPI
from routes import (
    collabrewards_routes,
    signup_routes,
    login_routes,
    calendar_routes,
    rewards_store_routes,
    chore_routes,
    auth_routes,
    progress_routes,
)

app = FastAPI(title="QuestNest API")

app.include_router(collabrewards_routes.router)
app.include_router(signup_routes.router)
app.include_router(login_routes.router)
app.include_router(calendar_routes.router)
app.include_router(rewards_store_routes.router)
app.include_router(chore_routes.router)
app.include_router(auth_routes.router)
app.include_router(progress_routes.router)

@app.get("/health")
def health():
    return {"ok": True}
