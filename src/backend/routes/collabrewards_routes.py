from fastapi import APIRouter, Form
from pydantic import BaseModel
from backend.database.firestore import db as DB
from backend.database.collab_reward import (create_collab_reward, update_collab_reward,)

router = APIRouter(prefix="/collabrewards", tags=["Collaborative Family Rewards"])

# class CollabReward(BaseModel):
#     title: str
#     description: str | None = None
#     goal_xp: int

collab_reward = None
    
@router.post("/create")
async def create_collab_reward(
    title: str = Form(),
    description: str = Form(),
    goal_xp: int = Form(),
):
    global collab_reward
    collab_reward = {
        "Title": title,
        "Description": description,
        "XP Goal": goal_xp,
        "Current XP": 0,
    }
    return {"message": "Collaborative family reward created!", "reward": collab_reward}
    
@router.get("/progress")
async def get_collab_progress():
    if not collab_reward:
        return {
            "Title": None,
            "Description": None,
            "Current XP": 0,
            "XP Goal": 1,
        }
        
    return collab_reward
    
@router.post("/update")
async def update_collab_progress(member_id: str = Form(), xp_earned: int = Form()):
    global collab_reward
    collab_reward["Current XP"] += xp_earned
        
    unlocked = collab_reward["Current XP"] >= collab_reward["XP Goal"]
    return {
        "message": f"{member_id} earned {xp_earned} XP!",
        "new_total": collab_reward["Current XP"],
        "unlocked": unlocked,
    }
    
@router.get("/familysize")
async def get_family_size(email: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    profiles = list(family_ref.collection("PROFILE").stream())
    count = len(profiles)
    return {"family_size": max(1, count)}

# Helper function for chore integration(added by JS)       
async def award_points(username: str, points: int):
    """Helper function for chore integration."""
    print(f"Awarded {points} points to {username} for completing a chore.")
