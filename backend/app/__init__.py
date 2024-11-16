#__init__.py
# Flask 앱과 확장 기능 초기화를 작성

from flask import Flask  # Flask 클래스 가져오기
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy 가져오기
from flask_cors import CORS  # CORS 설정용 플러그인

db = SQLAlchemy()  # 데이터베이스 객체 생성

def create_app():
    app = Flask(__name__)  # Flask 앱 객체 생성

    # 앱 설정 (config.py의 내용을 사용)
    app.config.from_object("app.config.Config")

    # 확장 기능 초기화
    db.init_app(app)  # SQLAlchemy 데이터베이스 초기화
    CORS(app)  # 다른 도메인(예: Vue.js 프론트엔드)에서의 요청 허용

    # 블루프린트(라우트 모음) 등록
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
