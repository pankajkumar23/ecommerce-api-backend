from flask import Flask, Blueprint, jsonify, request
from services.user_services import sighin_user_services,login_user_services
from schemas.sighin_user_schema import SighinUserValidations
from schemas.login_user_schema import LoginUserValidations

user_router = Blueprint("user", __name__)

@user_router.route("/register-user",methods = ['POST'])
def sighin_user():
    try:
        data = SighinUserValidations(**request.json)
        return sighin_user_services(data)
    except Exception as e:
        print(f"Error at sighin_user {str(e)}")
        return jsonify({"message": str(e)}),400


@user_router.route("/login-user",methods = ['POST'])
def login_user():
    try:
        data = LoginUserValidations(**request.json)
        return login_user_services(data)
    except Exception as e:
        print(f"Error at login_user {str(e)}")
        return jsonify({"message": str(e)}),400



    
