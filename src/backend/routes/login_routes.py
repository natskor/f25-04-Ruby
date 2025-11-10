from fastapi import APIRouter, Form, HTTPException

router = APIRouter(prefix="/login_page", tags=["Login to Account"])

@router.post("/")
# Not sure yet if async is needed in front of 'def'
async def login_user(email: str = Form(), password: str = Form()):
    
    # Replace with Firestore user input
    user = {
        "email": "email@odu.edu",
        "password": "password"
    }
    
    if email != user["email"] or password != user["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    return {"message": "Login Successful!"}
