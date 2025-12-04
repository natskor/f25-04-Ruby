from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/xp/{member_id}")
def get_xp(member_id: str):
    return {
        "member_id": member_id,
        "goal_xp": 5000,
        "current_xp": 1500,
    }
    
@router.post("/xp/{member_id}/update")
def update_xp(member_id: str, xp_earned: int = 0):
    new_total = 1000 + xp_earned
    return {
        "member_id": member_id,
        "message": f"{member_id} earned {xp_earned} XP!",
        "new_total": new_total
    }

@router.get("/level/{member_id}")
def get_level(member_id: str):
    return {
        "member_id": member_id,
        "level": 10,
    }

@router.post("/level/{member_id}/update")
def update_level(member_id: str, current_level: int = 10):
    new_level = current_level + 1
    return {
        "member_id": member_id,
        "message": f"{member_id} leveled up!",
        "new_level": new_level
    }

