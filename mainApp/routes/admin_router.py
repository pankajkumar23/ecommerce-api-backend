from flask import Flask, Blueprint, jsonify, request
from services.auth_services import roles_required
from services.admin_get_services import (
    get_all_products_services,get_all_users_services, get_user_product_services,)
from services.admin_update_services import update_user_services,update_product_services
from services.admin_delete_services import (
    delete_product_services, delete_user_services
)
from schemas.edit_user_schema import EditUserValidation
from schemas.update_product_schema import UpdateProductValidations


admin_router = Blueprint("admin", __name__)


@admin_router.route("/get-all-products", methods=["GET"])
@roles_required("admin")
def get_all_products():
    try:
        
        return get_all_products_services()
    except Exception as e:
        print(f"Error at get_all_products {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/get-all-users", methods=["GET"])
@roles_required("admin")
def get_all_users():
    try:
        return get_all_users_services()
    except Exception as e:
        print(f"Error at get_all_users {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/get-user-product", methods=["GET"])
@roles_required("admin")
def get_user_product():
    try:
        id = request.args.get("id", type=int)
        return get_user_product_services(id)
    except Exception as e:
        print(f"Error at get-user-product {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/edit-user", methods=["POST"])
@roles_required("admin")
def edit_user():
    try:
        user_data = request.user_data
        id = request.args.get("id", int)
        data = EditUserValidation(**request.json)
        return update_user_services(id, data,user_data)
    except Exception as e:
        print(f"Error at edit_user {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/delete-product", methods=["POST"])
@roles_required("admin")
def delete_product():
    try:
        id = request.args.get("id", type=int)
        return delete_product_services(id)
    except Exception as e:
        print(f"Error at delete_product {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/update-product", methods=["POST"])
@roles_required("admin")
def update_product():
    try:
        id = request.args.get("id", type=int)
        data = UpdateProductValidations(**request.json)
        return update_product_services(id, data)
    except Exception as e:
        print(f"Error at update_product {str(e)}")
        return jsonify({"message": str(e)}), 400


@admin_router.route("/delete-user", methods=["POST"])
@roles_required("admin")
def delete_user():
    try:
        
        id = request.args.get("id", type=int)
        return delete_user_services(id)
    except Exception as e:
        print(f"Error at delete_user {str(e)}")
        return jsonify({"message": str(e)}), 400
