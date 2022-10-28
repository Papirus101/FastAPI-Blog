from db.base import Base

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=False)
    body = Column(VARCHAR, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    author_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    
    author = relationship('User', backref=backref('posts'), lazy='joined')
    category = relationship('Category', backref=backref('posts'), lazy='joined')
    
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    parrent_category_id = Column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=True, default=None)

    children_categories = relationship('Category', backref=backref('parrent_category', remote_side=[id]), lazy='dynamic')