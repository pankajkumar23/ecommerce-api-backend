from flask import jsonify
from models.user_model import Users
from database.db import db
from datetime import timedelta
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


def sighin_user_services(data):
    try:
        existing_user = Users.query.filter_by(email=data.email).first()
        if not existing_user:
            user = Users(
                email=data.email,
                hash_password=generate_password_hash(data.password),
                username=data.username,
                role=data.role
            )
            db.session.add(user)
            db.session.commit()
            identity = {
                "role": data.role,
                "email": data.email,
                "username": data.username,
                "id": user.id,
            }
            try:
                access_token = create_access_token(
                    identity=identity, expires_delta=timedelta(days=150)
                )
            except:
                jsonify({"message": "token expired", "error": str(e)}), 400
            return (
                jsonify(
                    {
                        "email": user.email,
                        "username": user.username,
                        "role": user.role,
                        "access_token": access_token,
                    }
                ),
                200,
            )
        return jsonify({"message": "user already registered!!!"}), 400
    except Exception as e:
        print(f"Error at sighin_user_implementation {str(e)}")
        return f"message: {str(e)}"


def login_user_services(data):
    try:
        existing_user = Users.query.filter_by(email=data.email).first()
        if not existing_user:
            return jsonify({"message": "user not found"}), 401
        identity = {
            "email": existing_user.email,
            "id": existing_user.id,
            "role": existing_user.role,
        }
        try:
            access_token = create_access_token(
                identity=identity, expires_delta=timedelta(days=150)
            )
        except:
            jsonify({"message": "token expired", "error": str(e)}), 400
        if existing_user and check_password_hash(
            existing_user.hash_password, data.password
        ):
            return (
                jsonify(
                    {
                        "message": "sucessfully logged_in...",
                        "email": existing_user.email,
                        "username": existing_user.username,
                        "access_token": access_token,
                    }
                ),
                200,
            )
        elif existing_user and not check_password_hash(
            existing_user.hash_password, data.password
        ):
            return jsonify({"message": "incorrect password"}), 401
    except Exception as e:
        print(f"Error at login_user_implementation {str(e)}")
        return f"message: {str(e)}"
