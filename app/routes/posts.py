from fastapi import HTTPException, Depends,status,APIRouter
from sqlalchemy.orm import Session
from ..models import PostORM,UserORM
from ..schemas import Post,PostCreate,Postget
from ..database import get_db
from ..outh2 import get_current_user
from typing import List
router=APIRouter(prefix="/posts",tags=['Posts'])
@router.get("/", response_model=list[Postget])
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostORM).all()


@router.post("/", response_model=Post)
def create_post(payload: PostCreate, db: Session = Depends(get_db),user_id=Depends(get_current_user)):
    post = PostORM(user_id=user_id,**payload.model_dump())
    print(user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/me/posts",response_model=List[Postget])
def get_curr_posts(db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
    ans=db.query(PostORM).filter(PostORM.user_id==user_id).all()
    return ans

@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostORM).filter(PostORM.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post
@router.get("/user/{uname}",response_model=List[Postget])
def get_post(uname: str,db:Session=Depends(get_db)):
    user=db.query(UserORM).filter(UserORM.email==uname)
    if(not user):
        raise HTTPException(status_code=404, detail="User not found")
    posts=db.query(PostORM).join(PostORM.owner).filter(UserORM.email==uname).all()
    return posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int, db: Session = Depends(get_db),user_id=Depends(get_current_user)):
    post = db.query(PostORM).filter(PostORM.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    db.delete(post)
    db.commit()


@router.put("/{id}", response_model=Post)
def update_post(id: int, payload: PostCreate, db: Session = Depends(get_db)):
    post = db.query(PostORM).filter(PostORM.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    for k, v in payload.model_dump().items():
        setattr(post, k, v)
    db.commit()
    db.refresh(post)
    return post
