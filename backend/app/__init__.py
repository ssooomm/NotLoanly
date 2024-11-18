#__init__.py
# Flask 앱과 확장 기능 초기화를 작성
#Flask 객체 생성: Flask(__name__)은 현재 파일 이름을 기준으로 Flask 애플리케이션 객체를 만듭니다.
#설정 적용: app.config.from_object를 통해 설정 파일의 값을 불러옵니다.
#데이터베이스 초기화: db.init_app(app)으로 데이터베이스 연결 설정을 완료합니다.
#블루프린트 등록: register_blueprint를 통해 라우트를 앱에 추가합니다.
from flask import Flask  # Flask 클래스 가져오기
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy 가져오기
from flask_cors import CORS  # CORS 설정용 플러그인
from flask_socketio import SocketIO

db = SQLAlchemy()  # 데이터베이스 객체 생성
socketio = SocketIO(cors_allowed_origins="*")  # WebSocket 초기화

def create_app():
    app = Flask(__name__)  # Flask 앱 객체 생성
    #__name__은 현재 Python 모듈의 이름
    # 앱 설정 (config.py의 내용을 사용)
    app.config.from_object("app.config.Config")

    # 확장 기능 초기화
    db.init_app(app)  # SQLAlchemy 데이터베이스 초기화
    CORS(app)  # 다른 도메인(예: Vue.js 프론트엔드)에서의 요청 허용
    socketio.init_app(app) # WebSocket 초기화

    # 블루프린트(라우트 모음) 등록
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app

