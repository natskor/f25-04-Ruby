from fastapi import APIRouter, Form
from backend.database.firestore import db as DB
from backend.database.collab_reward import (create_collab_reward, update_collab_reward,)

router = APIRouter(prefix="/collabrewards", tags=["Collaborative Family Rewards"])
    
@router.post("/create")
async def create_collab_reward(
    email: str = Form(),
    title: str = Form(),
    description: str = Form(),
    goal_xp: int = Form(),
):
    
    ref = (
        DB.collection("FAMILY UNIT")
        .document(email)
        .collection("COLLAB REWARD")
        .document("active")
        )
    
    reward_data = {
        "Title": title,
        "Description": description,
        "XP Goal": goal_xp,
        "Current XP": 0,
    }

    ref.set(reward_data)
    
    return {"message": "Collaborative family reward created!", "reward": reward_data}
    
@router.get("/progress")
async def get_collab_progress(email: str):
    
    ref = (
        DB.collection("FAMILY UNIT")
        .document(email)
        .collection("COLLAB REWARD")
        .document("active")
    )

    doc = ref.get()
    if not doc.exists:
        return {
            "Title": "No active family reward",
            "Description": None,
            "XP Goal": 1,
            "Current XP": 0,
        }

    return doc.to_dict()
    
@router.post("/update")
async def update_collab_progress(email: str = Form(),
                                 member_id: str = Form(),
                                 xp_earned: int = Form()):
    
    ref = (
        DB.collection("FAMILY UNIT")
        .document(email)
        .collection("COLLAB REWARD")
        .document("active")
    )
    
    doc = ref.get()
    data = doc.to_dict()
    new_total = data.get("Current XP", 0) + xp_earned
    ref.update({"Current XP": new_total})
        
    unlocked = new_total >= data.get("XP Goal", 1)
    return {
        "message": f"{member_id} earned {xp_earned} XP!",
        "new_total": new_total,
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
