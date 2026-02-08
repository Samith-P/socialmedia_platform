from .config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


engine =create_engine(settings.database_url)

Base.metadata.create_all(bind=engine)

session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=session()
    try:
        yield db 
    finally:
        db.close()