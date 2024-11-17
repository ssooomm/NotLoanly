from app import create_app,db

app = create_app()

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
