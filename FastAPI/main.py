from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
import models

app = FastAPI()

origin = [
 # Kubernetes Vue Service
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET','POST'],
    allow_headers=["*"],
)


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/{session_user}")
async def HorizonServers(
    request: Request,
    session_user: str,
    db: Session = Depends(get_db)
):
   context = db.query(models.Horizon).filter(models.Horizon.UserName == session_user).all() #Get User From Oauth and MSAL from Frontend vue.js.
    return (context)
   

#Search for a specific User
@app.get("/horizon/{user_name}")
async def HorizonServers(
    request: Request,
    user_name: str,
    db: Session = Depends(get_db)
):
   context = db.query(models.Horizon).filter(models.Horizon.UserName == user_name).all()
   return (context)
