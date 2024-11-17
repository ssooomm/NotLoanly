class Config:
    # MySQL 연결 정보
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:1234@localhost/notLoanly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy 이벤트 시스템 비활성화
    SECRET_KEY = "your-secret-key"
