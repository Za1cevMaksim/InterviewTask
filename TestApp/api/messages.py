from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
import crud, schemas
from auth import get_current_user
from fastapi import HTTPException
from db.database import get_db


router = APIRouter()

@router.post("/")
def send_message(message: schemas.MessageBase,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_message = crud.create_message(db=db, message=message, user_id=current_user.id)
    return db_message

@router.get("/{channel_id}")
def get_messages(channel_id: int, db: Session = Depends(get_db)):
    return crud.get_messages(db=db, channel_id=channel_id)