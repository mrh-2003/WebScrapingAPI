from typing import Union
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import timedelta

from models.user import User
from models.user_in_db import UserInDB
from models.user_register import UserRegister
from db.fake_users import fake_users_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_credentials_exception():
    return HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    user_data = db.get(username)
    if user_data:
        return UserInDB(**user_data)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise get_credentials_exception()
    return user

def create_access_token(data: dict, time_expire: Union[datetime, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + time_expire
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode,key= SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
            raise get_credentials_exception()
        user = get_user(fake_users_db, username)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_active_user(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already in use")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}

def login_user(form_data: UserRegister):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": user.username}, time_expire=access_token_expires)