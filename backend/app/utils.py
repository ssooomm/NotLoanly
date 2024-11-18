import json
from flask import make_response

def json_response(data, status=200):
    """JSON 응답을 UTF-8로 처리"""
    response = make_response(json.dumps(data, ensure_ascii=False))
    response.status_code = status
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
