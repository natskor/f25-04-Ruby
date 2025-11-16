from fastapi import APIRouter, Form, HTTPException
from backend.database.firestore import db
import hashlib

router = APIRouter(prefix="/login_page", tags=["Login to Account"])

# Function to hash password
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/")
# Not sure yet if async is needed in front of 'def'
async def login_user(email: str = Form(), password: str = Form()):
    
    # Hash the password
    pw_hash = hash_password(password)
    
    # Look for a user doc in Firestore
    users_ref = db.collection("FAMILY UNIT").document(email).get()    
    # Get matching document if found
 
    # If no account is found error
    if not users_ref.exists:
        raise HTTPException(status_code=404, detail="No account found with that email.")
    
    data = users_ref.to_dict()
    
    # Get stored hashed pw from Firestore
    stored_hashed_pw = data.get("PasswordHash")
    
    # If these don't match, exception
    if pw_hash != stored_hashed_pw:
        raise HTTPException(status_code=401, detail="Invalid password.")
    
    return {"message": "Login Successful!"}
