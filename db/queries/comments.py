from db.models.comments import Comment, CommentsUsersLikes

from sqlalchemy import select, update, delete, desc
from sqlalchemy.exc import NoResultFound

from exceptions.db_exc import NotFoundException, NotOwnerException


async def create_comment(db_session, user_id: int, **kwargs):
    new_comment = Comment(author_id=user_id, **kwargs)
    db_session.add(new_comment)
    await db_session.commit()
    
    
async def get_replies(db_session, comment: list):
    replies = await db_session.execute(comment[0].replies)
    replies_list = []
    for reply in replies:
        replies_list.append(
            {
                'comment_id': reply[0].id,
                'body': reply[0].body,
                'likes': reply[0].likes,
                'owner': {
                    'login': comment[0].author.login,
                    'avatar': comment[0].author.avatar,
                    'email': comment[0].author.email
                    },
                'replies':await get_replies(db_session, reply),
                'created_at': comment[0].created_at
            }
        )
    return replies_list if replies_list else None
    
    
async def get_comments(db_session, post_id: int):
    sql = select(Comment).where(
        Comment.post_id == post_id,
        Comment.parrent_comment_id == None
        ).order_by(desc(Comment.created_at))
    data = await db_session.execute(sql)
    comments = data.unique()
    comments_list = []
    for comment in comments:
        comments_list.append(
            {
                'comment_id': comment[0].id,
                'body': comment[0].body,
                'likes': comment[0].likes,
                'owner': {
                    'login': comment[0].author.login,
                    'avatar': comment[0].author.avatar,
                    'email': comment[0].author.email
                },
                'replies': await get_replies(db_session, comment),
                'created_at': comment[0].created_at
            }
        )
    return comments_list if comments_list else None


async def get_comment_owner(db_session, comment_id: int):
    sql = select(Comment.author_id).where(Comment.id == comment_id)
    data = await db_session.execute(sql)
    try:
        comment_owner = data.one()
    except NoResultFound:
        raise NotFoundException('Comment was not found')
    return comment_owner


async def update_comment_by_id(db_session, comment_id: int, user_id: int, **kwargs):
    comment_owner = await get_comment_owner(db_session, comment_id)
    if comment_owner.author_id != user_id:
        raise NotOwnerException('comment')
    sql = update(Comment).values(**kwargs).where(Comment.id == comment_id)
    await db_session.execute(sql)
    await db_session.commit()
    
    
async def delete_comment(db_session, comment_id: int, user_id: int):
    comment_owner = await get_comment_owner(db_session, comment_id)
    if comment_owner.author_id != user_id:
        raise NotOwnerException('comment')
    sql = delete(Comment).where(Comment.id == comment_id)
    await db_session.execute(sql)
    await db_session.commit()
    
    
async def like_comment_by_id(db_session, comment_id: int, user_id: int):
    new_like = CommentsUsersLikes(comment_id=comment_id, user_id=user_id)
    db_session.add(new_like)
    await db_session.commit()