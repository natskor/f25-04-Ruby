# src/routes/auth_routes.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
import jwt
import os

# use absolute import so it works when started as `uvicorn src.main:app`
from src.backend.firestore import db

# ---------------- Config ----------------
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = "HS256"
ACCESS_TOKEN_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------- Models ----------------
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    firstName: str
    lastName: str
    role: str = Field(pattern="^(parent|child)$")
    familyID: Optional[str] = None

class PublicUser(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    role: str
    familyID: Optional[str] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------------- Helpers ----------------
def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)

def create_access_token(sub: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_MINUTES)).timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> PublicUser:
    email = decode_token(token)
    doc = db.collection("users").document(email).get()
    if not doc.exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    u = doc.to_dict()
    return PublicUser(
        email=email,
        firstName=u["firstName"],
        lastName=u["lastName"],
        role=u["role"],
        familyID=u.get("familyID"),
    )

# ---------------- Routes ----------------
@router.post("/register", response_model=PublicUser, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn):
    users = db.collection("users")
    if users.document(data.email).get().exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    users.document(data.email).set({
        "email": data.email,
        "firstName": data.firstName,
        "lastName": data.lastName,
        "role": data.role,
        "familyID": data.familyID,
        "passwordHash": hash_password(data.password),
        "createdAt": datetime.utcnow().isoformat(),
    })
    return PublicUser(
        email=data.email,
        firstName=data.firstName,
        lastName=data.lastName,
        role=data.role,
        familyID=data.familyID,
    )

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password

    doc = db.collection("users").document(email).get()
    if not doc.exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user = doc.to_dict()
    if not verify_password(password, user["passwordHash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(sub=email)
    return TokenOut(access_token=token)

@router.get("/me", response_model=PublicUser)
async def me(current: PublicUser = Depends(get_current_user)):
    return current
