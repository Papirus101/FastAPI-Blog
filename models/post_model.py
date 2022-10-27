from datetime import date, datetime
from typing import List
from pydantic import BaseModel
from models.user_model import UserBaseScheme

class CreatePostScheme(BaseModel):
    title: str
    body: str
    
class ViewPostScheme(BaseModel):
    title: str
    body: str
    author: UserBaseScheme
    likes: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
    
class ShortPostSheme(BaseModel):
    title: str
    author: UserBaseScheme
    likes: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
    
class ListPostsSheme(BaseModel):
    posts: List[ShortPostSheme]
    
    
class EditPostScheme(BaseModel):
    post_id: int
    title: str = None
    body: str = None