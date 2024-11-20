from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("DB_USER")  # "root"
passwd = os.getenv("DB_PASSWD")  # "1234"
host = os.getenv("DB_HOST")  # "127.0.0.1"
port = os.getenv("DB_PORT")  # "3306"
db = os.getenv("DB_NAME")  # "mydb"

# MySQL 연결 URL 생성
DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

# 엔진 생성 (connection_args는 필요에 따라 조정)
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DB 세션 의존성
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
