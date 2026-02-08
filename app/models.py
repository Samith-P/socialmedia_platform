from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base



class PostORM(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=True)
    published=Column(Boolean,default=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="Cascade"),nullable=False)
    owner=relationship("UserORM")

class UserORM(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'))