import uuid
import hashlib
import redis
from datetime import timedelta

from fastapi import APIRouter, Response, Request, Depends, HTTPException
from passlib.context import CryptContext
from hashlib import sha256


from api.db.interface import get_connection, run_proc

# -------------------
# Config
# -------------------
SESSION_TTL = 60 * 60 * 2  # 2 hours

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------
# Utils
# -------------------
def generate_session_token() -> str:
    return str(uuid.uuid4())


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------
# Session Management
# -------------------
def create_session(user_id: str) -> str:
    token = generate_session_token()
    token_hash = hash_token(token)

    r.setex(
        name=f"session:{token_hash}",
        time=SESSION_TTL,
        value=user_id
    )

    return token


def get_user_from_session(token: str):
    token_hash = hash_token(token)
    return r.get(f"session:{token_hash}")


def delete_session(token: str):
    token_hash = hash_token(token)
    r.delete(f"session:{token_hash}")


# -------------------
# Dependency
# -------------------
def get_current_user(request: Request):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = get_user_from_session(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return user_id


# -------------------
# Routes
# -------------------
@router.post("/login")
def login(response: Response, username: str, password: str):
    # Replace with real DB validation

    conn = get_connection()
    result = run_proc(
        conn=conn,
        proc="request_session",
        args=(
            username,
        )
    )
    conn.close()

    if len(result[0]) == 0:
        raise HTTPException(status_code=401, detail="Invalid user")

    user = result[0][0]
    print(user)

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")


    print("1")
    token = create_session(user_id=username)

    print("2")
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,   # set False in local dev if needed
        samesite="lax",
        max_age=SESSION_TTL
    )

    print("3")

    return {"message": "Logged in"}


@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("session_token")

    if token:
        delete_session(token)

    response.delete_cookie("session_token")

    return {"message": "Logged out"}


@router.get("/me")
def get_me(user_id: str = Depends(get_current_user)):
    return {"user": user_id}