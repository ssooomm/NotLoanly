from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # 환경 설정 불러오기
    db.init_app(app)                         # 데이터베이스 초기화
    CORS(app)                                # CORS 설정
    with app.app_context():
        from . import routes                 # 라우트 등록
        return app
