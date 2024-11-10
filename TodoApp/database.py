from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%40marouan%2FNARJIS%2F08%40@localhost/TodoApplicationDatabase'


#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) --> Second argument only for sqlite3

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()









