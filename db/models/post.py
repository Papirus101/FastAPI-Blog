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
    