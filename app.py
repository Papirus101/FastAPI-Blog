import traceback

from fastapi import FastAPI, Response, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from utils.bot import send_telegram_error

from routes.users import users_router
from routes.posts import posts_router
from routes.comments import comments_router

app = FastAPI(
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json'
        )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        await send_telegram_error(traceback.format_exc())
        return Response("Internal server error", status_code=500)

# app.middleware('http')(catch_exceptions_middleware)

app.include_router(users_router, prefix='/api')
app.include_router(posts_router, prefix='/api', dependencies=[Depends(OAuth2PasswordBearerCookie())])
app.include_router(comments_router, prefix='/api', dependencies=[Depends(OAuth2PasswordBearerCookie())])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Forum API",
        version="1.0.0",
        description="Ну а вот тут, короче, супер длинное и крутое описание документации -_-</br>"
        "В общем базовая АПИ, с возможностью регистрации, авторизации по токену, можно загрузить свою фоточку как аватарку</br>"
        "Есть простенькая система постов с комментариями и категориями, бесконечная вложенность с генерацией дерева на стороне бекенда</br>"
        "Кстати, к постам тоже можно загружать фоточки :)</br>"
        "Проект пишется в надежде, что при устройстве хотя бы кто-то посмотрит на гитхаб и не будет проосить делать тестовое, большинство кейсов тестовых заданий, есть тут!</br></br>"
        "<b>Если ты был тут, нажми <a href='https://github.com/Papirus101'><img width='15px' src='https://cdn-icons-png.flaticon.com/512/25/25231.png'></a>, чтобы посмотреть другие мои репозитории</b></br>"
        "<b>А ещё у меня есть <img width='15px' src='https://web.telegram.org/img/logo_share.png'> Telegram: <a href='https://t.me/Papirus101'>@Papirus101</a></b></br></br>"
        "<b>Используемые технологии:</b></br>"
        "<img src='https://camo.githubusercontent.com/735520e7f3675790ecb0499e803da92370fdcaeee6f1bcdb92650afebc580cb7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d626c75653f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465'> "
        "<img src='https://camo.githubusercontent.com/388eec9485fc4f4cc924e2ff72ae826f1b6f6c2b8aa0ecf82001ebedfe4a352b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f466173744150492d677265656e3f7374796c653d666f722d7468652d6261646765266c6f676f3d66617374617069266c6f676f436f6c6f723d7768697465'></br>"
        "<img src='https://camo.githubusercontent.com/a7d9e65ab699c17b0d89db50d247039dd4764f6d6bd4908140efbaa0ce28d773/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53514c416c6368656d792d7265643f7374796c653d666f722d7468652d6261646765266c6f676f436f6c6f723d7768697465'> "
        "<img src='https://camo.githubusercontent.com/b5c800847b46a87a938a167bcd8374293f627cbd36ef09efd6e9da21f2f42d1c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f506f737467726553514c2d626c75653f7374796c653d666f722d7468652d6261646765266c6f676f3d706f737467726573716c266c6f676f436f6c6f723d7768697465'></br>"
        "<img src='https://camo.githubusercontent.com/ec0d32e85caf4723d5182a75338c89f85a2c3679aed0c46c9ee9fd1c8dc2a316/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6769742d2532334630353033332e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d676974266c6f676f436f6c6f723d7768697465'> "
        "<img src='https://camo.githubusercontent.com/a37b583596f3d06a65e5324fe8d63f8a406e734b402648fffa6569c99b7298fc/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f52656469732d7265643f7374796c653d666f722d7468652d6261646765266c6f676f3d7265646973266c6f676f436f6c6f723d7768697465'> "
        "<img src='https://camo.githubusercontent.com/0c75b890f268add3cf96f9994398f3fe1d6c7d81c4458f789e78eb664de74ae9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f416c656d6269632d77686974653f7374796c653d666f722d7468652d6261646765266c6f676f3d616c656d626963266c6f676f436f6c6f723d7768697465'>",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi