from flask import Flask, Blueprint, jsonify, request
from services.seller_product_services import add_product_details,delete_products_services, update_product_details
from services.auth_services import roles_required
from schemas.add_prduct_schema import AddProductValidations
from schemas.update_product_schema import UpdateProductValidations
from services.seller_get_services import get_category_services,get_products_services

seller_router = Blueprint("seller", __name__)

@seller_router.route("/add-product", methods=["POST"])
@roles_required("seller")
def add_product():
    try:
        user_data = request.user_data
        data = AddProductValidations(**request.json)
        return add_product_details(data,user_data)
    except Exception as e:
        print(f"Error at add_product {str(e)}")
        return jsonify({"message": str(e)}), 400


@seller_router.route("/get-products", methods=["GET"])
@roles_required("seller")
def get_products():
    try:
        user_data = request.user_data
        page = request.args.get("page", type=int)
        per_page = request.args.get("per_page", type=int)
        return get_products_services(page, per_page,user_data)
    except Exception as e:
        print(f"Error at get_products {str(e)}")
        return jsonify({"message": str(e)}), 400

@seller_router.route("/update-products", methods=["POST"])
@roles_required("seller")
def update_product():
    try:
        user_data = request.user_data
        id = request.args.get("id", type=int)
        if id == None:
            return jsonify({"message": "query parameter required!!!"}), 401
        data= UpdateProductValidations(**request.json)
        return update_product_details(id ,data,user_data)
    except Exception as e:
        print(f"Error at update_product {str(e)}")
        return jsonify({"message": str(e)}), 400


@seller_router.route("/delete-products", methods=["POST"])
@roles_required("seller")
def delete_products():
    try:
        user_data = request.user_data
        id = request.args.get("id", type=int)
        if id is None:
            return jsonify({"message": "product id is required in query parameter!"}), 401
        return delete_products_services(id,user_data)
    except Exception as e:
        print(f"Error at delete_products {str(e)}")
        return jsonify({"message": str(e)}), 400

@seller_router.route("/get-categories", methods=["GET"])
@roles_required("seller")
def get_categories():
    try:
        return get_category_services()
    except Exception as e:
        print(f"Error at get_category_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400
