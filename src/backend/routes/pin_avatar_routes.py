from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
import hashlib

router = APIRouter(tags=["PIN & Avatar"])

# In-memory user store for demo:
# users["Emma"] = {"pin_hash": "...", "avatar_id": "images/avatars/dragon.png"}
users: Dict[str, Dict[str, Optional[str]]] = {}


def hash_pin(pin: str) -> str:
    """Hash the PIN so we do not store it in plain text."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


class PinCreateRequest(BaseModel):
    username: str
    # 4–6 digits only
    pin: str = Field(..., min_length=4, max_length=6, pattern=r"^[0-9]+$")


class PinVerifyRequest(BaseModel):
    username: str
    pin: str = Field(..., min_length=4, max_length=6, pattern=r"^[0-9]+$")


class AvatarRequest(BaseModel):
    username: str
    avatar_id: str


@router.post("/pin")
def create_or_update_pin(body: PinCreateRequest):
    """
    Create or update a PIN for a user.
    """
    pin_hash = hash_pin(body.pin)

    if body.username not in users:
        users[body.username] = {"pin_hash": pin_hash, "avatar_id": None}
    else:
        users[body.username]["pin_hash"] = pin_hash

    return {"message": "PIN set successfully.", "username": body.username}


@router.post("/pin/verify")
def verify_pin(body: PinVerifyRequest):
    """
    Verify a user's PIN.
    """
    user = users.get(body.username)

    if not user or not user.get("pin_hash"):
        raise HTTPException(status_code=404, detail="User or PIN not found.")

    if user["pin_hash"] != hash_pin(body.pin):
        raise HTTPException(status_code=401, detail="Invalid PIN.")

    return {"message": "PIN verified.", "username": body.username}


@router.post("/avatar")
def set_avatar(body: AvatarRequest):
    """
    Choose an avatar and associate it with the user.
    """
    if body.username not in users:
        users[body.username] = {"pin_hash": None, "avatar_id": body.avatar_id}
    else:
        users[body.username]["avatar_id"] = body.avatar_id

    return {
        "message": "Avatar set successfully.",
        "username": body.username,
        "avatar_id": body.avatar_id,
    }
