import json
from decimal import Decimal
from flask import make_response

def json_response(data, status=200):
    """JSON 응답을 UTF-8로 처리, Decimal 지원"""
    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)  # 또는 str(obj)
        raise TypeError

    response = make_response(json.dumps(data, ensure_ascii=False, default=decimal_default))
    response.status_code = status
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
