from fastapi import APIRouter, Form
from backend.database.family_unit import (add_current_xp, get_experience_info, increment_level)

router = APIRouter(prefix="/progress", tags=["Individual Progress"])


@router.get("/xp/{member_id}")
async def get_xp(member_id: str, email: str):
    docs = get_experience_info(email, member_id)

    if not docs:
        return {
            "member_id": member_id,
            "current_xp": 0,
            "goal_xp": 100,
        }

    data = docs[0]
    current_xp = data.get("Current XP", 0)
    needed_xp = data.get("Needed XP", 100)
    goal_xp = current_xp + needed_xp

    return {
        "member_id": member_id,
        "current_xp": current_xp,
        "goal_xp": goal_xp
    }


@router.post("/xp/{member_id}/update")
async def update_xp(member_id: str, email: str = Form(), xp_earned: int = Form()):
    add_current_xp(email, member_id, xp_earned)
    docs = get_experience_info(email, member_id)

    if not docs:
        return {
            "member_id": member_id,
            "current_xp": 0,
            "goal_xp": 100,
        }

    data = docs[0]
    current_xp = data.get("Current XP", 0)
    needed_xp = data.get("Needed XP", 100)
    goal_xp = current_xp + needed_xp

    return {
        "member_id": member_id,
        "message": f"{member_id} earned {xp_earned} XP!",
        "current_xp": current_xp,
        "goal_xp": goal_xp
    }


@router.get("/level/{member_id}")
async def get_level(member_id: str, email: str):
    docs = get_experience_info(email, member_id)

    if not docs:
        return {
            "member_id": member_id,
            "level": 0,
            "next_level": 1,
        }

    data = docs[0]
    current_level = data.get("Current Level", 0)
    next_level = data.get("Next Level", 1)

    return {
        "member_id": member_id,
        "level": current_level,
        "next_level": next_level,
    }


@router.post("/level/{member_id}/update")
async def update_level(member_id: str, email: str = Form(),
):
    docs = get_experience_info(email, member_id)

    if not docs:
        return {
            "member_id": member_id,
            "level": 0,
            "next_level": 1,
        }

    data = docs[0]
    prev_goal = data.get("Current XP", 0) + data.get("Needed XP", 0)
    increment_level(email, member_id, prev_goal)

    docs = get_experience_info(email, member_id)
    data = docs[0]

    current_level = data.get("Current Level", 0)
    next_level = data.get("Next Level", 1)

    return {
        "member_id": member_id,
        "message": f"{member_id} leveled up!",
        "level": current_level,
        "next_level": next_level,
    }
