#routers.py
#RESTful API의 엔드포인트를 정의
from flask import Blueprint, request, jsonify
from . import db
from .models import User, Categories, UserExpenses, RepaymentPlans, Transactions, Notification
import json
from .services import get_montyly_expense, get_repayment_status, get_dashboard_summary, get_consumption_percentage, get_consumption_analysis
from .services import save_repayment_plan, get_repayment_plans, select_repayment_plan
from .services import create_transaction_service
from . import db
from . import socketio
from .utils import json_response
from .gpt_service import parse_gpt_response, call_chatgpt, generate_prompt_with_loan_details


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
    return jsonify(data)

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
@main_routes.route("/api/repayment/save-plan", methods=["POST"])
def save_plan():
    try:
        data = request.json
        user_id = data.get("userId")
        categories = data.get("categories")
        repayment_period = data.get("repaymentPeriod")

        # 필수 값 확인
        if not user_id or not categories or not repayment_period:
            return json_response({
                "status": "error",
                "message": "userId, categories, and repaymentPeriod are required."
            }, 400)

        # 서비스 호출
        response, status = save_repayment_plan(user_id, categories, repayment_period)
        return json_response(response, status)
    except Exception as e:
        return json_response({"status": "error", "message": str(e)}, 500)

#2-3. 상환 플랜 리스트 조회
@main_routes.route('/api/repayment/plans', methods=['GET'])
def get_repayment_plans():
    try:
        # 사용자 ID를 쿼리 파라미터에서 가져오기
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        # 사용자에 대한 모든 상환 플랜 조회
        plans = db.session.query(RepaymentPlans).filter_by(user_id=user_id).all()

        if not plans:
            return jsonify({"status": "success", "message": "No repayment plans found for this user."}), 200

        # 플랜 데이터 구성
        plans_data = []
        for plan in plans:
            plans_data.append({
                "plan_id": plan.plan_id,
                "plan_name": plan.plan_name,
                "total_amount": plan.total_amount,
                "duration": plan.duration,
                "details": plan.details,  # JSON 문자열로 저장된 경우, 필요시 json.loads()로 변환 가능
                "hashtags": plan.hashtags
            })

        return jsonify({"status": "success", "plans": plans_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

# 2-4. 상환 플랜 선택
@main_routes.route("/api/repayment/select-plan", methods=["POST"])
def select_plan():
    try:
        data = request.json
        user_id = data.get("userId")
        plan_id = data.get("planId")

        try:
            user_id = int(user_id)
            plan_id = int(plan_id)
        except (ValueError, TypeError):
            return json_response({
                "status": "error",
                "message": "userId and planId must be integers."
            }, 400)

        message = select_repayment_plan(user_id, plan_id)
        return json_response({"status": "success", "message": message}, 200)
    except Exception as e:
        return json_response({"status": "error", "message": str(e)}, 500)

@main_routes.route('/api/analyze-and-insert-plans', methods=['POST'])
def analyze_and_insert_plans():
    try:
        # 사용자 입력값 수신
        data = request.json
        user_id = data.get("user_id")
        loan_amount = data.get("loan_amount")
        interest_rate = data.get("interest_rate", 6.0)  # 기본값 6%
        duration = data.get("duration", 6)  # 기본값 6개월
        month = data.get("month", 10)  # 요청 데이터에서 월을 받음, 기본값 10월

        if not user_id or not loan_amount:
            return jsonify({"status": "error", "message": "필수 필드가 누락되었습니다"}), 400

        # 사용자 소비 데이터 가져오기
        user_expenses = UserExpenses.query.filter_by(user_id=user_id, month=month).all()  # 요청한 월의 데이터
        if not user_expenses:
            return jsonify({"status": "error", "message": "사용자의 지출 데이터를 찾을 수 없습니다"}), 404

        expense_data = [
            {
                "category_id": expense.category_id,
                "original_amount": expense.original_amount,
                "is_hard_to_reduce": expense.is_hard_to_reduce
            }
            for expense in user_expenses
        ]

        # ChatGPT로 분석 요청
        prompt = generate_prompt_with_loan_details(expense_data, loan_amount, interest_rate, duration)
        gpt_response = call_chatgpt(prompt)
        plans = parse_gpt_response(gpt_response)

        print(plans)  # 디버깅용 출력

        # RepaymentPlans 테이블에 저장
        try:
            for plan in plans:
                new_plan = RepaymentPlans(
                    user_id=user_id,
                    plan_name=plan['plan_name'],
                    total_amount=plan['total_amount'],
                    duration=plan['duration'],
                    details=json.loads(plan['details']),  # JSON 문자열을 파싱하여 저장
                    hashtags=", ".join(plan['hashtags']),  # hashtags 추가 처리
                    created_at=db.func.current_timestamp()
                )
                db.session.add(new_plan)
            
            db.session.commit()
            print("데이터가 성공적으로 커밋되었습니다.")  # 디버깅 로그 추가

        except Exception as e:
            db.session.rollback()
            print(f"커밋 중 오류 발생: {e}")  # 에러 메시지 출력
            return jsonify({"status": "error", "message": str(e)}), 500

        return jsonify({
            "status": "success",
            "message": "상환 계획이 생성되었습니다",
            "plans": plans
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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


#3-2. ��환 현황 조회
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
    """
    거래내역 생성 API
    """
    data = request.json

    # 필수 필드 검증
    user_id = data.get('user_id')
    category_id = data.get('category_id')
    transaction_date = data.get('transaction_date')
    amount = data.get('amount')
    description = data.get('description')
    payment_method = data.get('payment_method')

    if not user_id or not category_id or not transaction_date or not amount:
        return json_response({"error": "Missing required fields"}), 400

    # 서비스 호출
    result, status_code = create_transaction_service(
        user_id=user_id,
        category_id=category_id,
        transaction_date=transaction_date,
        amount=amount,
        description=description,
        payment_method=payment_method
    )

    return jsonify(result), status_code


# 5-1. API: 사용자 알림 가져오기
@main_routes.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.sent_at.desc()).all()
    notification_list = [{
        "notification_id": n.notification_id,
        "message": n.message,
        "sent_at": n.sent_at.strftime("%Y-%m-%d %H:%M:%S")
    } for n in notifications]

    return jsonify({
        "status": "success",
        "notifications": notification_list
    }), 200

# 5-2. 새 알림 생성
