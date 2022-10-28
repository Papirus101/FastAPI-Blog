from __future__ import annotations
import json
from datetime import datetime
from typing import List
from pydantic import BaseModel
from models.user_model import UserBaseScheme
    
class CreateCategorySheme(BaseModel):
    name: str
    parrent_category: int
    

class CategoryShortViewSheme(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

    
class CategoryViewSheme(CategoryShortViewSheme):
    children_categories: List[CategoryViewSheme] | None
        
        
class ListCategoriesScheme(BaseModel):
    categories: List[CategoryViewSheme]
        
        
class CreatePostScheme(BaseModel):
    title: str
    body: str
    category_id: int
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    
class ImagesPostSheme(BaseModel):
    photo: str
    
    class Config:
        orm_mode = True
    
    
class ViewPostScheme(BaseModel):
    id: int
    title: str
    category: CategoryShortViewSheme
    body: str
    author: UserBaseScheme
    likes: int
    created_at: datetime
    images: List[ImagesPostSheme]
    
    class Config:
        orm_mode = True
    
    
class ShortPostSheme(BaseModel):
    id: int
    title: str
    category: CategoryShortViewSheme
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