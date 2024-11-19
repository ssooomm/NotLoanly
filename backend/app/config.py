# class Config:
#     SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your-secret-key"

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1220@localhost:3306/notLoanly"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "a_very_secret_key_that_should_not_be_shared"

