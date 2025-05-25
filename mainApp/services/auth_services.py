from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import request

def check_jwt():
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception as e:
        return {"message": str(e)}, 401
    
def roles_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_data = check_jwt()
            if isinstance(user_data,tuple):
                return user_data
            user_data
            if not user_data:
                return {"message": "unauthorised, token required"}, 401
            if user_data["role"] != role:
                response = f"access denied, only {role} can perform this actions"
                return {"message": response}, 400
            request.user_data = user_data
            return f(*args, **kwargs)
        return wrapper
    return decorator

