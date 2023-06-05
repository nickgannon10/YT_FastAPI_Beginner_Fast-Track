from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# what data is received from the client
# class PostBase(BaseModel):
#     pass

class Post(BaseModel):
    id: Optional[int] = None    
    title: str
    content: str
    published: Optional[bool] = True
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True

