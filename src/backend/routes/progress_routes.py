from fastapi import APIRouter, Form
from backend.database.family_unit import (add_current_xp, get_experience_info, increment_level)
from backend.database.firestore import db as DB
router = APIRouter(prefix="/progress", tags=["Individual Progress"])


@router.get("/xp/{member_id}")
async def get_xp(member_id: str, email: str):
    docs = get_experience_info(email, member_id)

    if not docs:
        return {
            "member_id": member_id,
            "current_xp": 0,
            "goal_xp": 1000,
        }

    data = docs[0]
    current_xp = data.get("Current XP", 0)
    needed_xp = data.get("Needed XP", 1000)
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
            "goal_xp": 1000,
        }

    data = docs[0]
    current_xp = data.get("Current XP", 0)
    needed_xp = data.get("Needed XP", 1000)
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
            "level": 1,
            "next_level": 2,
        }

    data = docs[0]
    current_level = data.get("Current Level", 1)
    next_level = data.get("Next Level", 2)

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
            "level": 1,
            "next_level": 2,
        }

    data = docs[0]
    prev_goal = data.get("Current XP", 0) + data.get("Needed XP", 0)
    increment_level(email, member_id, prev_goal)

    docs = get_experience_info(email, member_id)
    data = docs[0]

    current_level = data.get("Current Level", 1)
    next_level = data.get("Next Level", 2)

    return {
        "member_id": member_id,
        "message": f"{member_id} leveled up!",
        "level": current_level,
        "next_level": next_level,
    }

@router.get("/rankings")
async def get_rankings(email: str):
    family_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE")
    profiles = family_ref.stream()

    rankings = []

    for p in profiles:
        pdata = p.to_dict()
        user = pdata.get("User")
        avatar = pdata.get("Avatar", "")
        
        prog = get_experience_info(email, user)
        xp = 0
        level = 1
        if prog:
            xp = prog[0].get("Current XP", 0)
            level = prog[0].get("Current Level", 1)

        rankings.append({
            "user": user,
            "avatar": avatar,
            "xp": xp,
            "level": level
        })

    # sorted by xp amount
    for i in range(len(rankings)):
        for j in range(i + 1, len(rankings)):
            if rankings[j]["xp"] > rankings[i]["xp"]:
                # swap positions
                rankings[i], rankings[j] = rankings[j], rankings[i]

    return rankings