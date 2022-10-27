from fastapi import APIRouter, Body, Depends
from db.queries.comments import create_comment, delete_comment, get_comments, update_comment_by_id
from db.session import get_session
from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from depends.auth.jwt_handler import get_user
from exceptions.db_exc import NotFoundException
from models.comment_model import CommentUpdateScheme, ListCommentsScheme, NewCommentScheme

comments_router = APIRouter(
        prefix='/comments',
        tags=['comments']
        )


@comments_router.post('/new_comment', status_code=201, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def create_new_comment(session = Depends(get_session), user = Depends(get_user), comment: NewCommentScheme = Body()):
        await create_comment(session, user['id'], **dict(comment))
        
        
@comments_router.get('/get_comments_post', response_model=ListCommentsScheme, status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def post_comments(post_id: int, session = Depends(get_session)):
        comments = await get_comments(session, post_id)
        if not comments:
                raise NotFoundException('Comments was not found for this post')
        return {'comments': comments}


@comments_router.patch('/update_comment', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def comment_update(session = Depends(get_session), user = Depends(get_user), post_info: CommentUpdateScheme = Body()):
        comment_id = post_info.pop('comment_id')
        await update_comment_by_id(session, comment_id, user['id'], **dict(post_info))
        
        
@comments_router.delete('/delete_comment', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def delete_comment_post(comment_id: int, session = Depends(get_session), user = Depends(get_user)):
        await delete_comment(session, comment_id, user['id'])