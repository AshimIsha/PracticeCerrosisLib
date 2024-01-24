from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError
from jose import jwt
from passlib.context import CryptContext
#from schemes import user_shemes
from database.connection import get_connection, commit
from database.user_database import User, Check
import bcrypt

SECRET_KEY = 'some_key'
ALGO = 'HS256'
ACCESS_TIME = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hash(password: str):
    return context.hash(password)


def create_token(data:dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user_by_username(username, session=get_connection()):
    return session.query(User).filter_by(username=username).first()

def get_check_by_user(id, session=get_connection()):
    return session.query(Check).filter_by(user_id=id).first()


def authenticate_user(username, password, session=get_connection()):
    user = session.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt


def get_current_user(token):
    if token is None:
        token = Depends(oauth2_scheme)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGO]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return username


def create_user(username, password, wallet, age, session=get_connection()):
    new_user = User(username=username, hashed_password=hash_password(password), wallet=wallet, age=age)
    session.add(new_user)
    commit(session)
    new_check = create_check(id=new_user.id, cost=15)
    session.add(new_check)
    commit(session)
    return new_user

def create_check(id, cost):
    new_bill = Check(user_id=id, cost=cost)
    return new_bill

def update_check(id, new_cost, session=get_connection()):
    try:
        check = session.query(Check).get(id)
        if check:
            check.money = new_cost
            commit(session)
            return 1
    except:
        return 0
