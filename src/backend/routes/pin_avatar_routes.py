from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
import hashlib
from backend.database.firestore import db
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter(tags=["PIN & Avatar"])

# # In-memory user store for demo:
# # users["Emma"] = {"pin_hash": "...", "avatar_id": "images/avatars/dragon.png"}
# users: Dict[str, Dict[str, Optional[str]]] = {}

def hash_pin(pin: str) -> str:
    """Hash the PIN so we do not store it in plain text."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()

class PinCreateRequest(BaseModel):
    username: str
    # 4 digits only
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^[0-9]+$")


class PinVerifyRequest(BaseModel):
    username: str
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^[0-9]+$")


class AvatarRequest(BaseModel):
    username: str
    avatar_id: str

    # Find correct user document from Firestore based on user
def get_user_doc(username: str):
    ref = db.collection("Family Member").document(username)
    doc = ref.get()
    if doc.exists:
        return ref, doc.to_dict()
    
    # Searches by first== name
    matches = db.collection("FAMILY MEMBER").where(filter=FieldFilter("First", "==", username)).limit(1).stream()
    match = next(matches, None)

    if match:
        return db.collection("FAMILY MEMBER").document(match.id), match.to_dict()

    return None, None

@router.post("/pin")
async def create_or_update_pin(body: PinCreateRequest):
    """
    Create or update a PIN for a user.
    """
    # Look up user in Firestore
    user_ref = db.collection("FAMILY MEMBER").document(body.username)
    doc = user_ref.get()

    # If not found, look by first name
    if not doc.exists:
        matches = db.collection("FAMILY MEMBER").where(filter=FieldFilter("First", "==", body.username)).limit(1).stream()
        match = next(matches, None)
        if not match:
            raise HTTPException(status_code=404, detail="User not found.")
        user_ref = db.collection("FAMILY MEMBER").document(match.id)
    
    # Save hashed PIN to database
    pin_hash = hash_pin(body.pin)
    user_ref.update({"PINHash": pin_hash})

    # if body.username not in users:
    #     users[body.username] = {"pin_hash": pin_hash, "avatar_id": None}
    # else:
    #     users[body.username]["pin_hash"] = pin_hash

    return {"message": "PIN set successfully.", "username": body.username}


@router.post("/pin/verify")
async def verify_pin(body: PinVerifyRequest):
    """
    Verify a user's PIN.
    """
    # Look up user in Firestore
    user_ref = db.collection("FAMILY MEMBER").document(body.username)
    doc = user_ref.get()

    # If not found, search by first name
    if not doc.exists:
        matches = db.collection("FAMILY MEMBER").where(filter=FieldFilter("First", "==", body.username)).limit(1).stream()
        match = next(matches, None)
        if not match:
            raise HTTPException(status_code=404, detail="User not found.")
        user_ref = db.collection("FAMILY MEMBER").document(match.id)
        doc = user_ref.get()
    
    # Compare PINS to ensure they match
    data = doc.to_dict()
    stored_hash = data.get("PINHash")

    if stored_hash != hash_pin(body.pin):
        raise HTTPException(status_code=401, detail="Invalid PIN.")
    
    # user = users.get(body.username)
    
    # if not user:
    #     default_pin = "1234"
    #     users[body.username] = {"pin_hash": hash_pin(default_pin), "avatar_id": None}
    #     # Now treat as if the correct PIN was entered
    #     if body.pin == default_pin:
    #         return {
    #             "message": "Fallback with default PIN for now",
    #             "username": body.username,
    #         }
    #     else:
    #         raise HTTPException(status_code=401, detail="Invalid PIN (fallback user).")

    # if not user.get("pin_hash"):
    #     raise HTTPException(status_code=404, detail="User or PIN not found.")

    # if user["pin_hash"] != hash_pin(body.pin):
    #     raise HTTPException(status_code=401, detail="Invalid PIN.")

    return {"message": "PIN verified.", "username": body.username}


@router.post("/avatar")
async def set_avatar(body: AvatarRequest):
    """
    Choose an avatar and associate it with the user.
    """
    # Look up user in Firestore
    user_ref = db.collection("FAMILY MEMBER").document(body.username)
    doc = user_ref.get()

    # If not found, search by first name
    if not doc.exists:
        users = db.collection("FAMILY MEMBER").where(filter=FieldFilter("First", "==", body.username)
                        ).limit(1).stream()
        user_doc = next(users, None)
        
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found.")
        
        user_ref = db.collection("FAMILY MEMBER").document(user_doc.id)
    # Save chosen avatar to that user
    user_ref.update({"AvatarID": body.avatar_id})
    
    # if body.username not in users:
    #     users[body.username] = {"pin_hash": None, "avatar_id": body.avatar_id}
    # else:
    #     users[body.username]["avatar_id"] = body.avatar_id

    return {
        "message": "Avatar set successfully.",
        "username": body.username,
        "avatar_id": body.avatar_id,
    }

# This will list all avatars associated with that family account (profiles)
# Does not show names associated with those profiles yet
@router.get("/avatar/list")
async def list_avatars():
    
    members = db.collection("FAMILY MEMBER").stream()
    avatar_list = []

    for doc in members:
        data = doc.to_dict()
        if "AvatarID" in data and data["AvatarID"]:
            avatar_list.append({
                "username": data.get("MemberID"),
                "avatar_id": data["AvatarID"]
            })

    return avatar_list