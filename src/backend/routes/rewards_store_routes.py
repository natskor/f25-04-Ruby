from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/rewards_store", tags=["Rewards Store"])

# Replace with real xp amount later
user_xp = {"current_xp": 500}

# Replace with stored rewards later
rewards = {
    "icecream": {"cost": 100, "name": "Ice Cream"},
    "movienight": {"cost": 500, "name": "Movie Night"},
}

class Reward(BaseModel):
    id: str
    name: str
    cost: int
    level_unlock: int

# This will require changing code in rewards_store.py to have a scrollable empty list that we add rewards to
@router.get("/rewards")
def get_rewards():
    return rewards

@router.post("/rewards")
def add_reward(reward: Reward):
    if reward.id in rewards:
        raise HTTPException(status_code=400, detail="Reward ID already exists")
    
    rewards[reward.id] = reward.dict()
    return {"message": f"Reward '{reward.name}' created successfully!", "reward": reward.dict()}
    
@router.post("/claim/{reward_id}")
def claim_reward(reward_id: str):
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