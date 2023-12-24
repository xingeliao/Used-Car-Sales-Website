from flask import jsonify, Blueprint, request, Response, make_response
import team85.controller.login as lc


login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['POST'])
def login():
    content = request.json    
    username = content.get('username')
    password = content.get('password')

    login_response = lc.basic_auth(username, password)
    if login_response is None:
        error = {
           'error': 'unable to verify user' 
        }
        return jsonify(error), 401

    username = login_response['data']['username']
    user_role = login_response['data']['user_role']
    response = make_response({"username": username, "user_role": user_role})
    response.set_cookie("username", value=username)
    response.set_cookie("user_role", value=user_role)
    
    return response
