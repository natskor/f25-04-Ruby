from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import hashlib
from backend.database.firestore import db
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter(tags=["PIN & Avatar"])

def hash_pin(pin: str) -> str:
    """Hash the PIN so we do not store it in plain text."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()

class PinCreateRequest(BaseModel):
    email: str
    profile: str
    # 4 digits only
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^[0-9]+$")


class PinVerifyRequest(BaseModel):
    email: str
    profile: str
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^[0-9]+$")


class AvatarRequest(BaseModel):
    email: str
    profile: str
    avatar: str

@router.post("/pin")
async def create_or_update_pin(body: PinCreateRequest):
    """
    Create or update a PIN for a user.
    """
    # Look up user in Firestore
    profile_ref = (db.collection("FAMILY UNIT").document(body.email).collection("PROFILE").document(body.profile))
    doc = profile_ref.get()

    # If not found
    if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")
    
    # Save hashed PIN to database
    profile_ref.update({"PIN": hash_pin(body.pin)})

    return {"message": "PIN set successfully.", "profile": body.profile}


@router.post("/pin/verify")
async def verify_pin(body: PinVerifyRequest):
    """
    Verify a user's PIN.
    """
    # Look up user in Firestore
    profile_ref = (db.collection("FAMILY UNIT").document(body.email).collection("PROFILE").document(body.profile))
    doc = profile_ref.get()

    # If not found
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Compare PINS to ensure they match
    stored_hash = doc.to_dict().get("PIN")

    if stored_hash != hash_pin(body.pin):
        raise HTTPException(status_code=401, detail="Invalid PIN.")

    return {"message": "PIN verified.", "profile": body.profile}


@router.post("/avatar")
async def set_avatar(body: AvatarRequest):
    """
    Choose an avatar and associate it with the user.
    """
    # Look up user in Firestore
    profile_ref = (db.collection("FAMILY UNIT").document(body.email).collection("PROFILE").document(body.profile))
    doc = profile_ref.get()

    # If not found
    if not doc.exists:
        profile_ref.set({
            "User": body.profile,
            "Avatar": body.avatar,
            "Role": "Caregiver",
            "PIN": "",
        })
    else:   
        # Save chosen avatar to that user
        profile_ref.update({"Avatar": body.avatar})

    return {
        "message": "Avatar set successfully.",
        "profile": body.profile,
        "avatar": body.avatar,
    }

# This will list all avatars associated with that family account (profiles)
# Does not show names associated with those profiles yet
@router.get("/avatar/list/{email}")
async def list_avatars(email: str):
    
    profiles = db.collection("FAMILY UNIT").document(email).collection("PROFILE").stream()
    profiles_list = []

    for doc in profiles:
        data = doc.to_dict()
        profiles_list.append({
            "profile": doc.id,
            "avatar": data.get("Avatar")
        })

    return profiles_list