from fastapi import APIRouter, Form, HTTPException

router = APIRouter(prefix="/signup_page", tags=["Create Account"])

@router.post("/")
# Not sure yet if async is needed in front of 'def'
def create_account(username: str = Form(), email: str = Form(), password: str = Form(), confirm: str = Form()):
    
    if password != confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    # Firestore logic here?
    # Also, may need to store passcodes as a hash to encrypt it for safety?
    
    return {
        "username": username,
        "email": email
    }
