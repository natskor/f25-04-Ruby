from fastapi import APIRouter

router = APIRouter(prefix="/collabrewards", tags=["Collaborative Family Rewards"])

@router.get("/progress")
def get_collab_progress():
    return {
        "goal_xp": 20000,
        "current_xp": 8000,
        "contributors": ["Kaleb","Alice", "Mom", "Dad"]
    }
    
@router.post("/update")
def update_collab_progress(member_id: str = "test_user", xp_earned: int = 0):
    new_total = 1000 + xp_earned
    return {
        "message": f"{member_id} earned {xp_earned} XP!",
        "new_total": new_total
    }