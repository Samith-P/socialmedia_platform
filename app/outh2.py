from .config import settings
from jose import JWTError, jwt
from datetime import datetime,timedelta
from .schemas import TokenData
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from .models import UserORM
from sqlalchemy.orm import Session
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expiration_mins
def create_access_token(data):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

def verify(token,credentials_exception):
    try:
        payLoad=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id=payLoad.get("user_id")
        if(not id):
            raise credentials_exception
        token_data=TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not verify credentials")
    token=verify(token,credentials_exception)
    user=db.query(UserORM).filter(UserORM.id==token.id).first()
    return user.id
