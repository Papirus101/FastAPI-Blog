from db.base import Base

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=False)
    body = Column(VARCHAR, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    author_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    author = relationship('User', backref=backref('posts'), lazy='joined')
    

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(VARCHAR(150), nullable=False)
    post_id = Column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    author_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    parrent_comment_id = Column(ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    likes = Column(Integer, default=0)
    
    replies = relationship('Comment', backref=backref('replies_comment', remote_side=[id]), lazy='dynamic')