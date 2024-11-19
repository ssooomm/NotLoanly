# class Config:
#     SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your-secret-key"

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1220@localhost:3306/notLoanly"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
    JSON_AS_ASCII = False  # 한글 깨짐 방지 설정
