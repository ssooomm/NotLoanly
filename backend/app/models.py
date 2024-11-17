from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # to_dict 메서드는 클래스 내부에 정확히 들여쓰기되어 있어야 합니다.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
