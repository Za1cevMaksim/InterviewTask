from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from db.database import get_db

router = APIRouter()

@router.post("/")
def create_channel(channel: schemas.ChannelBase, db: Session = Depends(get_db)):
    db_channel = crud.create_channel(db=db, channel=channel)
    return db_channel

@router.get("/")
def list_channels(db: Session = Depends(get_db)):
    return crud.get_channels(db=db)
