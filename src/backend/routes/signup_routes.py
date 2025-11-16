from fastapi import APIRouter, Form, HTTPException
from backend.database import family_unit
from backend.database.firestore import db
import hashlib

router = APIRouter(prefix="/signup_page", tags=["Create Account"])

# Function to hash password
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/")
# Not sure yet if async is needed in front of 'def'
async def create_account(
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
    confirm: str = Form()):
    
    if password != confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    # Check if this email already exists
    existing = db.collection("FAMILY UNIT").document(email).get()
    if existing.exists:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    
    # Secure password
    pw_hash = hash_password(password)
    
    # Try to create new account in Firestore
    try:
        # Create the document and fill fields
        family_unit.create_family(email)
        family_unit.add_password(email, pw_hash)
        family_unit.create_profile(email, username)
        family_unit.add_role(email, username, "Caregiver")
        # Not sure about PIN yet
        # family_member.add_pin(email, "0000")
        
        # Store hashed password in Firestore
        db.collection("FAMILY UNIT").document(email).update({
            "PasswordHash": hash_password(password)
        })
        # Error if making the account doesn't work for whatever reason
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating account: {e}")
    
    return {
        "message": "Account created successfully!",
        "username": username,
        "email": email
    }
