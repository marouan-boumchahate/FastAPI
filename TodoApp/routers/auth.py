from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..models import Users
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET_KEY = '754a3b82e89c04fb326e6b5eaaf1c1b5173a1d8db5c696694cac8a699104082e'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ouathe2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class UserRequest(BaseModel):
    #id: int = Field(gt=0)
    email: str = Field(min_length=3)
    username: str = Field(min_length=3, max_length=25)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=5)
    role: str
    phone_number: str = Field(min_length=6, max_length=15, pattern=r"^\d+$")

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="TodoApp/templates")


### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###



def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user: return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False 
    
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(ouathe2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not Validate user.')

        return {'username': username, 'id': user_id, 'role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not Validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      user_model: UserRequest):
    user = Users(
        email = user_model.email,
        username = user_model.username,
        first_name = user_model.first_name,
        last_name = user_model.last_name,
        role = user_model.role,
        hashed_password = bcrypt_context.hash(user_model.password),
        is_active = True,
        phone_number = user_model.phone_number
    )

    db.add(user)
    db.commit()
    
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not Validate user.')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}