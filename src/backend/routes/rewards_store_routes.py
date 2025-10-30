from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/rewards_store", tags=["Rewards Store"])

# Replace with real xp amount later
user_xp = {"current_xp": 500}

# Replace with stored rewards later
rewards = {
    "icecream": {"cost": 100, "name": "Ice Cream"},
    "movienight": {"cost": 500, "name": "Movie Night"},
}

# This will require changing code in rewards_store.py to have a scrollable empty list that we add rewards to
@router.get("/rewards")
def get_rewards():
    return rewards
    
    
@router.post("/claim/{reward_id}")
def claim_reward(reward_id: str):
    reward = rewards[reward_id]
    
    if user_xp["current_xp"] < reward["cost"]:
        raise HTTPException(status_code=400, detail="Not enough XP")
    
    user_xp["current_xp"] -= reward["cost"]
    
    return {
        "message": f"{reward['name']} claimed!",
        "remaining_xp": user_xp["current_xp"]
    }