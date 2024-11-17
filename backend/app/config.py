# class Config:
#     SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your-secret-key"

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:1234@localhost:3306/notLoanly"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
