from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True


class Author(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

class Post(BaseModel):
    id: Optional[int] = None    
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int] = None

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: int
    is_sale: bool = False
    inventory: int

    class Config:
        orm_mode = True
