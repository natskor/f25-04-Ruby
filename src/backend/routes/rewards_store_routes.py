from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from backend.database.firestore import db

router = APIRouter(prefix="/families", tags=["Rewards Store"])


# ---------- XP helpers (NOW IN FIRESTORE) ----------

def family_doc(family_id: str):
    """
    Convenience helper to get the Firestore document for a family.
    """
    return db.collection("families").document(family_id)


def get_family_xp(family_id: str) -> int:
    """
    Read the family's XP from Firestore.
    Uses the 'current_xp' field on the family document.
    Defaults to 0 if the document or field is missing.
    """
    doc_ref = family_doc(family_id)
    doc = doc_ref.get()

    if not doc.exists:
        return 0

    data = doc.to_dict() or {}
    try:
        return int(data.get("current_xp", 0))
    except (TypeError, ValueError):
        return 0


def set_family_xp(family_id: str, new_xp: int) -> None:
    """
    Write the family's XP to Firestore.
    Stores it in the 'current_xp' field on the family document.
    """
    safe_xp = max(0, int(new_xp))
    doc_ref = family_doc(family_id)
    # merge=True so we don't overwrite other family fields
    doc_ref.set({"current_xp": safe_xp}, merge=True)


class Reward(BaseModel):
    id: str
    name: str
    cost: int
    level_unlock: int
    image_url: str | None = None   # ✅ fixed typo + optional image
    is_family_rewards: bool = True


# ---------- Firestore helpers for rewards ----------

def rewards_collection(family_id: str):
    return (
        db.collection("families")
        .document(family_id)
        .collection("rewards")
    )


def get_family_rewards(family_id: str) -> list[dict]:
    """Return all rewards for a family as a list of dicts."""
    snaps = rewards_collection(family_id).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in snaps]


def reward_exists(family_id: str, reward_id: str) -> bool:
    doc = rewards_collection(family_id).document(reward_id).get()
    return doc.exists


def get_reward(family_id: str, reward_id: str) -> dict | None:
    doc = rewards_collection(family_id).document(reward_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}


# ---------- Routes ----------

# NOTE: leading "/" here is important! prefix="/families" + "/{family_id}/rewards"
#       gives "/families/{family_id}/rewards"
@router.get("/{family_id}/rewards")
async def get_rewards(family_id: str):
    rewards = get_family_rewards(family_id)
    current_xp = get_family_xp(family_id)
    # Frontend can render a scrollable list from rewards
    return {
        "rewards": rewards,
        "current_xp": current_xp,
    }


@router.post("/{family_id}/rewards")
async def add_reward(family_id: str, reward: Reward):
    if reward_exists(family_id, reward.id):
        raise HTTPException(status_code=400, detail="Reward ID already exists")

    reward_data = reward.dict()  # if on Pydantic v2, use reward.model_dump()
    # use reward.id as document ID so we can look it up easily later
    rewards_collection(family_id).document(reward.id).set(reward_data)

    return {
        "message": f"Reward '{reward.name}' created successfully!",
        "reward": reward_data,
    }


@router.post("/{family_id}/claim/{reward_id}")
async def claim_reward(family_id: str, reward_id: str):
    reward = get_reward(family_id, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")

    current_xp = get_family_xp(family_id)

    if current_xp < reward["cost"]:
        raise HTTPException(status_code=400, detail="Not enough XP")

    new_xp = current_xp - reward["cost"]
    set_family_xp(family_id, new_xp)

    return {
        "message": f"{reward['name']} claimed!",
        "remaining_xp": new_xp,
    }
