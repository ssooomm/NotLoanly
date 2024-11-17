#routers.py
#RESTful API의 엔드포인트를 정의


from flask import Blueprint, request, jsonify
from .services import chat_with_gpt
from app.models import User  # User 모델 가져오기
from .services import get_montyly_expense
from . import db
from .models import User, Categories


main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/api/hello", methods=["GET"])
def say_hello():
    return jsonify({"message": "Hello, Flask!"})

#대출하는거
#user테이블의 loan_amount, interest_rate를 업데이트 해주는 엔드포인트
@main_routes.route("/api/loan/apply", methods=["POST"])
def apply_loan():
    try:
        # 요청 데이터 가져오기
        data = request.json
        user_id = data.get("user_id")
        loan_amount = data.get("loan_amount")
        interest_rate = data.get("interest_rate")

        # 필수 값 체크
        if not user_id or loan_amount is None or interest_rate is None:
            return jsonify({
                "status": "error",
                "message": "user_id, loan_amount, and interest_rate are required."
            }), 400

        # 데이터베이스에서 사용자 찾기
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({
                "status": "error",
                "message": f"User with id {user_id} not found."
            }), 404

        # 사용자 데이터 업데이트
        user.loan_amount = loan_amount
        user.interest_rate = interest_rate
        db.session.commit()  # 변경 사항 저장

        return jsonify({
            "status": "success",
            "message": "Loan details updated successfully.",
            "updated_user": user.to_dict()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500
#카테고리 보여주는 GET 요청
@main_routes.route("/api/categories", methods=["GET"])
def get_categories():
    try:
        # Categories 테이블에서 모든 데이터 조회
        categories = Categories.query.all()

        # 각 카테고리를 딕셔너리로 변환
        categories_list = [{"category_id": cat.category_id, "category_name": cat.category_name} for cat in categories]

        return jsonify({
            "status": "success",
            "categories": categories_list
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@main_routes.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)

# 2-1. 소비 분석 데이터 조회
@main_routes.route('/api/repayment/analysis', methods=['GET'])
def repayment_analysis():
    user_id = request.args.get('userId', type=int)
    data = get_montyly_expense(user_id, 10)  # 10월 데이터 조회
    return jsonify(data)