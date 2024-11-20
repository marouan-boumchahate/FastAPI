from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from starlette import status
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..models import Users
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)


SECRET_KEY = '754a3b82e89c04fb326e6b5eaaf1c1b5173a1d8db5c696694cac8a699104082e'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


ouathe2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



class UserVertification(BaseModel):
    current_password: str
    new_password: str = Field(min_length=5)

@router.get('/allusers', status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency,
                    db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    if user['role'] != 'admin':
        raise HTTPException(status_code=401, detail='This user is not allowed to get other users')
    
    return db.query(Users).filter(Users.id != user.get('id')).all()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency,
                   db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()



@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(form_data: UserVertification,
                          user: user_dependency,
                          db: db_dependency):
    
    # current_password = form_data.current_password
    # new_password = form_data.new_password

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()


    if not bcrypt_context.verify(form_data.current_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Current password is incorrect!!!')
    
    user_model.hashed_password = bcrypt_context.hash(form_data.new_password)

    db.add(user_model)
    db.commit()



@router.put('/update_phone_number/{new_phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_phone_number(user: user_dependency,
                      db: db_dependency,
                      new_phone_number: str):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = new_phone_number

    db.add(user_model)
    db.commit()


