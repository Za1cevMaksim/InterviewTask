from sqlalchemy.orm import Session
import models, schemas
import time
from models import User


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_message(db: Session, message: schemas.MessageBase, user_id: int):
    db_message = models.Message(content=message.content, user_id=user_id, channel_id=message.channel_id, timestamp=int(time.time()))
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, channel_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.channel_id == channel_id).offset(skip).limit(limit).all()

def create_channel(db: Session, channel: schemas.ChannelBase):
    db_channel = models.Channel(name=channel.name)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def get_channels(db: Session):
    return db.query(models.Channel).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()