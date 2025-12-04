from fastapi import APIRouter, Form, HTTPException
from backend.database import family_unit
from backend.database.firestore import db
import hashlib

router = APIRouter(prefix="/signup_page", tags=["Create Account"])

# Function to hash password
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/")
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
        family_unit.add_username(email, username)
        family_unit.add_password(email, pw_hash)
        
        # Error if making the account doesn't work for whatever reason
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating account: {e}")
    
    return {
        "message": "Account created successfully!",
        "username": username,
        "email": email
    }
