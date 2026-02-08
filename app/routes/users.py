from fastapi import HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..utils import encryptpass
from ..models import UserORM
from ..schemas import User,UserCreate
from ..database import get_db
from ..utils import verify
router=APIRouter(prefix="/users",tags=["Users"])
@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserORM).all()


@router.post("/", response_model=UserCreate)
def create_user(payload: User, db: Session = Depends(get_db)):
    hashed = encryptpass(payload.password)
    user = UserORM(email=payload.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}",response_model=UserCreate)
def get_userby_ID(id:int,db:Session=Depends(get_db)):
    user=db.query(UserORM).filter(UserORM.id==id).first()
    if(not user):
        raise HTTPException(status_code=404, detail="User not found")
    
    return user