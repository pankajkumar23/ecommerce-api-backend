from flask import Flask, Blueprint, jsonify, request
from services.buyer_product_services import decrease_product_quantity_services,get_buying_products_services
from services.buyer_cart_services import (
    add_to_cart_services,guest_user_add_to_cart,get_cart_items_services,get_guest_user_cart_items,remove_cart_items_services)
from services.auth_services import roles_required
from services.buyer_address_servies import add_address_services,update_address_services,user_address_services
from schemas.address_schema import AddressValidations
from services.buyer_order_services import order_product_services, get_order_details_services,remove_order_services
from services.webhook_services import verify_webhook_signature, create_checkout_session

buyer_router = Blueprint("buyer", __name__)

@buyer_router.route("/get-all-buying-products", methods=["GET"])
@roles_required("buyer")
def get_all_buying_products():
    try:
        data = request.args.to_dict()
        price = data.get("price")
        product_name = data.get("product_name")
        if price:
            price = int(price)
        return get_buying_products_services(product_name, price)
    except Exception as e:
        print(f"Error at get_all_buying_products {str(e)}")
        return jsonify({"message": str(e)}), 400


@buyer_router.route("/add-to-cart", methods=["GET"])
@roles_required("buyer")
def add_to_cart():
    try:
        user_data = request.user_data
        id = request.args.get("id",type=int)
        token = request.headers.get('Authorization')
        if not token:
            return guest_user_add_to_cart(id)
        
        return add_to_cart_services(id,user_data)
    except Exception as e:
        print(f"Error at add_to_cart {str(e)}")
        return jsonify({"message": str(e)}), 400

@buyer_router.route("/decrease-product-quantity", methods=["GET"])
def decrease_product_quantity():
    try:
        id = request.args.get("id",type=int)
        return decrease_product_quantity_services(id)
    except Exception as e:
        print(f"Error at decrease_product_quantity {str(e)}")
        return jsonify({"message": str(e)}), 400


@buyer_router.route("/get-cart-items", methods=["GET"])
@roles_required("buyer")
def get_cart_items():
    try:
        user_data = request.user_data
        token = request.headers.get('Authorization')
        if not token:
            return get_guest_user_cart_items()

        return get_cart_items_services(user_data)
    except Exception as e:
        print(f"Error at get_cart_items {str(e)}")
        return jsonify({"message": str(e)}), 400

@buyer_router.route("/remove-cart-item", methods=["DELETE"])
@roles_required("buyer")
def remove_cart_items():
    try:
        user_data = request.user_data
        id = request.args.get("id",type=int)
        return remove_cart_items_services(user_data,id)
    except Exception as e:
        print(f"Error at get_cart_items {str(e)}")
        return jsonify({"message": str(e)}), 400


@buyer_router.route("/add-address", methods=["POST"])
@roles_required("buyer")
def add_address():
    try:
        user_data = request.user_data
        data = AddressValidations(**request.json)
        return add_address_services(data,user_data)
    except Exception as e:
        print(f"Error at add_address {str(e)}")
        return jsonify({"message": str(e)}), 400

@buyer_router.route("/user-address", methods=["GET"])
@roles_required("buyer")
def user_address():
    try:
        user_data = request.user_data
        return user_address_services(user_data)
    except Exception as e:
        print(f"Error at user_address {str(e)}")
        return jsonify({"message": str(e)}), 400


@buyer_router.route("/update-address", methods=["POST"])
@roles_required("buyer")
def update_address():
    try:
        user_data = request.user_data
        id = request.args.get("id",type=int)
        data = AddressValidations(**request.json)
        return update_address_services(data,user_data,id)
    except Exception as e:
        print(f"Error at update_address {str(e)}")
        return jsonify({"message": str(e)}), 400


@buyer_router.route("/add-to-order", methods=["POST"])
@roles_required("buyer")
def order_product():
    try:
        user_data = request.user_data
        return order_product_services(user_data)
    except Exception as e:
        print(f"Error at order_product {str(e)}")
        return jsonify({"message": str(e)}), 400    

@buyer_router.route("/get-order-details", methods=["GET"])
@roles_required("buyer")
def get_order_details():
    try:
        user_data = request.user_data
        return get_order_details_services(user_data)
    except Exception as e:
        print(f"Error at get_order_details {str(e)}")
        return jsonify({"message": str(e)}), 400
    

@buyer_router.route("/remove-order", methods=["GET"])
@roles_required("buyer")
def remove_order():
    try:
        user_data = request.user_data
        id = request.args.get("id",type=int)
        return remove_order_services(user_data,id)
    except Exception as e:
        print(f"Error at remove_order {str(e)}")
        return jsonify({"message": str(e)}), 400
    
@buyer_router.route("/create-checkout-session", methods=["POST"])
@roles_required("buyer")
def create_checkout():
    try:
        user_data = request.user_data
        data = get_order_details_services(user_data)
        if isinstance(data,str):
            return jsonify({"message": data}), 400
        final_bill_amount = int(data[0]["final_bill_amount"])
        return create_checkout_session(final_bill_amount,user_data)
    except Exception as e:
        print(f"Error at create_checkout_session {str(e)}")
        return jsonify({"message": str(e)}), 400
    

@buyer_router.route("/webhook", methods=["GET","POST"])
def webhook():
    try:
        webhook_endpoint_secret = "whsec_C0Md749AIlt5ZM3ktvpSH36P7TgYQVgB"
        payload = request.data
        sig_headers = request.headers.get("stripe-signature")
        event = verify_webhook_signature(payload, sig_headers, webhook_endpoint_secret)
        if isinstance(event,str):
            return event
        return "ok"
    except Exception as e:
        print(f"Error at webhook {str(e)}")
        return jsonify({"message": str(e)}), 400
