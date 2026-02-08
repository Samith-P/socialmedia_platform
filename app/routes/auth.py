from fastapi import APIRouter,Depends,HTTPException,status
from ..schemas import User
from ..database import get_db
from sqlalchemy.orm import Session 
from ..models import UserORM
from ..utils import verify
from ..outh2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=["Authentication"])

@router.post("/login")
def login(payLoad:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(UserORM).filter(UserORM.email==payLoad.username).first()
    try:
        if(not user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
        if(not verify(payLoad.password,user.password)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")
    except:
        return (Exception,"ERROR OCCURED")
    token=create_access_token({"user_id":user.id})
    return {"access_token":token,"token_type":"Bearer"}