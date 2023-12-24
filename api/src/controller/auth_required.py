from datetime import datetime, timezone
from functools import wraps
from flask import request
import jwt

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {"error": "Authentication Token is missing"}, 401
        
        try:
            user_info=jwt.decode(token, "TEAM085_SECRET_KEY", algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"error": "Expired token"}, 401
        except:
            return {"error": "Invalid Authentication token"}, 401
        
        return f(user_info, *args, **kwargs)

    return decorated