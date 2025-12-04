from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from pydantic import BaseModel

router = APIRouter(prefix="/rewards_store", tags=["Rewards Store"])

# Replace with real xp amount later
user_xp = {"current_xp": 500}

# Replace with stored rewards later
rewards = {
    "icecream": {"cost": 100, "name": "Ice Cream"},
    "movienight": {"cost": 500, "name": "Movie Night"},
}

@router.get("/rewards")
async def get_rewards():
    return rewards

@router.post("/rewards")
async def add_reward(
    id: str = Form(),
    name: str = Form(),
    cost: int = Form(),
    level_unlock: int = Form(),
    image: UploadFile = File(None),
):
    if id in rewards:
        raise HTTPException(status_code=400, detail="Reward ID already exists")
    if image:
        file_bytes = await image.read()
    
    rewards[id] = {
        "id": id,
        "name": name,
        "cost": cost,
        "level_unlock": level_unlock,
        "image": ""
    }
    return {"message": f"Reward '{name}' created successfully!", "reward": rewards[id]}
    
@router.post("/claim/{reward_id}")
async def claim_reward(reward_id: str):
    if reward_id not in rewards:
        raise HTTPException(status_code=404, detail="Reward not found")

    reward = rewards[reward_id]
    
    if user_xp["current_xp"] < reward["cost"]:
        raise HTTPException(status_code=400, detail="Not enough XP")
    
    user_xp["current_xp"] -= reward["cost"]
    
    return {
        "message": f"{reward['name']} claimed!",
        "remaining_xp": user_xp["current_xp"]
    }