from flask import Blueprint, jsonify, request

bp = Blueprint("api", __name__)

@bp.route("/api/users", methods=["GET"])
def get_users():
    # 예제 데이터
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)

@bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    return jsonify({"message": f"User {data['name']} created!"})
