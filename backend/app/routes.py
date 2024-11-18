#routers.py
#RESTful API의 엔드포인트를 정의


from flask import Blueprint, request, jsonify
from .services import chat_with_gpt
from app.models import User  # User 모델 가져오기
from .services import get_montyly_expense
from .services import get_dashboard_summary
from .services import get_repayment_status
from .services import get_consumption_percentage, get_consumption_analysis
from . import db
from .models import User, Categories
from . import socketio
from .models import Transactions, Notification
from .utils import json_response



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
            "message": "대출신청이 완료되었습니다.",
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
        categories = Categories.query.all()
        categories_list = [{"category_id": cat.category_id, "category_name": cat.category_name} for cat in categories]

        return json_response({
            "status": "success",
            "categories": categories_list
        })
    except Exception as e:
        return json_response({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, status=500)



@main_routes.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return json_response(user_list)

# 2-1. 소비 분석 데이터 조회
@main_routes.route('/api/repayment/analysis', methods=['GET'])
def repayment_analysis():
    user_id = request.args.get('userId', type=int)
    data = get_montyly_expense(user_id, 10)  # 10월 데이터 조회
    return json_response(data)

# 3-1. 상환 요약 조회 
@main_routes.route('/api/dashboard/summary', methods=['GET'])
def dashboard_summary():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        summary = get_dashboard_summary(user_id)
        return json_response({"status": "success", "summary": summary}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#3-2. 상환 현황 조회
@main_routes.route('/api/dashboard/repayment-status', methods=['GET'])
def repayment_status():
    try:
        # 예: 사용자 ID를 요청 헤더 또는 인증 토큰에서 가져옴 (여기서는 1로 가정)
        user_id = request.args.get('user_id', type=int, default=1)
        data = get_repayment_status(user_id)
        return jsonify(data), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3-3. 상환 플랜 비율 조회
@main_routes.route('/api/dashboard/consumption-percentage', methods=['GET'])
def consumption_percentage():
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"status": "error", "message": "User ID is required"}), 400

    response = get_consumption_percentage(user_id)
    return json_response(response), response.get("status", 200)


# 3-4. 소비 분석 조회
@main_routes.route('/api/dashboard/consumption-analysis', methods=['GET'])
def consumption_analysis():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"status": "error", "message": "User ID is required"}), 400

    response = get_consumption_analysis(user_id)
    return jsonify(response), 200


# 4. 거래내역 추가
@main_routes.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.json

    # 필수 필드 검증
    user_id = data.get('user_id')
    category_id = data.get('category_id')
    transaction_date = data.get('transaction_date')
    amount = data.get('amount')
    description = data.get('description')
    payment_method = data.get('payment_method')

    if not user_id or not category_id or not transaction_date or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # 새로운 거래 추가
        transaction = Transactions(
            user_id=user_id,
            category_id=category_id,
            transaction_date=transaction_date,
            amount=amount,
            description=description,
            payment_method=payment_method
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully",
            "transaction_id": transaction.transaction_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# API: 사용자 알림 가져오기
@main_routes.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.sent_at.desc()).all()
    return json_response([{
        "notification_id": n.notification_id,
        "message": n.message,
        "sent_at": n.sent_at.strftime("%Y-%m-%d %H:%M:%S")
    } for n in notifications])

