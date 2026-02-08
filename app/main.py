from fastapi import FastAPI
from .routes import posts, users, auth
from .database import engine, Base
from . import models  

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "welcome to my api"}
