from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://todoapp_q80j_user:94omzdh4w0Pp8W9Ym3OmliLFJ4wexGVu@dpg-csrm7a0gph6c73b8v9eg-a.frankfurt-postgres.render.com/todoapp_q80j'


#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) --> Second argument only for sqlite3

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()









