from passlib.context import CryptContext
from datetime import datetime,timedelta
from .config import SECRET_KEY, ALGORITHM
import jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas import TokenData
from utils import get_user_by_userName

pwd_context  = CryptContext(schemes=['bcrypt'])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/token/")

def get_hash_password(password):
    hashed_password=pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict, expires_delta:timedelta):
    to_encode = data.copy()
    
    if expires_delta:
        expire =  datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt


async def current_user(token:Annotated[str,Depends(oauth_scheme)],
                        db:Session=Depends(get_db)): #  db_dependency = Annotated[Session,Depends(get_db)]

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        # time = payload.get("exp")# login username
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise HTTPException(
            status_code=440,
            detail="Your session is expired"
        )
       
    user_in_db = get_user_by_userName(db,token_data.username)

    if user_in_db is None:
        raise HTTPException(status_code=400,
                            detail="Invalid Username")
    return user_in_db