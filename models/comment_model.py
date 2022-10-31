from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from models.user_model import UserBaseScheme, UserShortSheme

class BaseCommentScheme(BaseModel):
    comment_id: int
    body: str
    likes: List[UserShortSheme]
    created_at: datetime
    owner: UserBaseScheme
    replies: List[BaseCommentScheme] | None
    
    
class NewCommentScheme(BaseModel):
    body: str
    post_id: int
    parrent_comment_id: None | int = Field(gt=0, default=None)        
    
    
class ListCommentsScheme(BaseModel):
    comments: List[BaseCommentScheme]
    
    
class CommentUpdateScheme(BaseModel):
    comment_id: int
    body: str