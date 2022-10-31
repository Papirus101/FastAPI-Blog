from pydantic import BaseModel, EmailStr


class UserBaseScheme(BaseModel):
    email: EmailStr
    login: str
    avatar: str | None

    class Config:
        orm_mode = True
        
class UserShortSheme(BaseModel):
    login: str
    avatar: str
    
    class Config:
        orm_mode = True

class UserRegisterScheme(UserBaseScheme):
    password: str


class UserLoginScheme(BaseModel):
    login: str
    password: str

class UserUpdateSheme(BaseModel):
    login: str | None
    email: EmailStr | None
    password: str | None


class TokenScheme(BaseModel):
    Authorization: str
