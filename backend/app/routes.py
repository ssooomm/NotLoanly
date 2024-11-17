#routers.py
#RESTful API의 엔드포인트를 정의


from flask import Blueprint, request, jsonify
from .services import chat_with_gpt
from app.models import User  # User 모델 가져오기

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/api/hello", methods=["GET"])
def say_hello():
    return jsonify({"message": "Hello, Flask!"})

@main_routes.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    response = chat_with_gpt(user_input)
    return jsonify({"response": response})

@main_routes.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)