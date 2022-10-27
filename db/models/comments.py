from db.base import Base
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref


class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(VARCHAR(150), nullable=False)
    author_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    parrent_comment_id = Column(ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    likes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    replies = relationship('Comment', backref=backref('parent', remote_side=[id]), lazy='dynamic')
    author = relationship('User', backref=backref('comments'), lazy='joined')
    