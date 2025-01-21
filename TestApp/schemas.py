from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_moderator: bool

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str
    channel_id: int

class Message(MessageBase):
    id: int
    user_id: int
    timestamp: int

    class Config:
        orm_mode = True

class ChannelBase(BaseModel):
    name: str

class Channel(ChannelBase):
    id: int
    messages: List[Message] = []

    class Config:
        orm_mode = True