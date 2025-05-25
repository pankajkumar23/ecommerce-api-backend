from flask import Flask, request,jsonify
from models.cart_model import CartItem
from database.db import db
import json
from services.buyer_product_services import increase_product_quantity
from models.product_model import Products



def guest_user_add_to_cart(id):
    try:
        print("guest_user_add_to_cart")
        data = increase_product_quantity(id)
        if isinstance(data, str):
            return data
        return data
    except Exception as e:
        print(f"Error at guest_user_add_to_cart{str(e)}")
        return f"message: {str(e)}", 400


def add_to_cart_services(id,user_data):
    try:
        if not id:
          return {"message":"id not found"},404
        print("add_to_cart_implementation")
        user_id = user_data["id"]
        product_data = request.cookies.get("product")
        if not product_data:
            return increase_product_quantity(id)
        products = json.loads(product_data)
        for product in products:
            product_id = product["product_id"]
            quantity = product["quantity"]
            if user_id ==id :
                product_quantity=quantity
                update_cart_quantity = CartItem.query.filter_by(product_id=product_id).first()
                if update_cart_quantity:
                    update_cart_quantity.quantity = product_quantity
                    db.session.commit()
            product_db = Products.query.get(product_id)
            if not product_db:
                return jsonify({"message": "product not found"}), 400
            existing_cart = CartItem.query.filter_by(product_id=product_id,user_id=user_id).first()
            if not existing_cart :
                cart = CartItem(product_id=product_id, user_id=user_id,quantity=quantity,)
                db.session.add(cart)
                db.session.commit()
                return {"message":"product succefully added to cart"}
            result = increase_product_quantity(id)
            if isinstance(result, str):
                return {"message":result},400
            response = result
        
        if not response:
            return {"message": "No products found to add"}, 400
        return response

    except Exception as e:
        print(f"Error at add_to_cart_implementation{str(e)}")
        return f"message: {str(e)}", 400
    

def get_guest_user_cart_items():
    try:
        grand_total = 0
        product_list = []
        product_data = request.cookies.get("product")
        if not product_data:
            return {"message": "product not found"}
        products = json.loads(product_data)
        for product in products:
            product_id = product["product_id"]
            quantity = product["quantity"]
            carts = CartItem.query.all()
            for cart in carts:
                product = cart.cart_product
                if product and product.id == product_id:
                    if not product.discount:
                        item_discount = 0
                    else:
                        item_discount = product.discount
                    
                    before_discount_price = (product.price) * (quantity)
                    discount = item_discount/ 100
                    discount_amount = discount * before_discount_price
                    after_discount_price = before_discount_price - discount_amount
                    grand_total = grand_total + after_discount_price
                    product_list.append(
                        {
                            "product_name": product.product_name,
                            "product_id": product.id,
                            "price": product.price,
                            "description": product.description,
                            "quantity": quantity,
                            "discount": product.discount,
                            "category": product.category.category_name,
                            "discount_amount":discount_amount,
                            "before_discount_price": before_discount_price,
                            "after_discount_price": after_discount_price,
                        }
                    )
                    

        return {"message": product_list, "grand_total": grand_total}, 200
    except Exception as e:
        print(f"Error at get_cart_items_implementation{str(e)}")
        return f"message: {str(e)}", 400


def get_cart_items_services(user_data):
    try:
        grand_total = 0
        product_list = []
        carts = CartItem.query.all()
        for cart in carts:
            quantity = cart.quantity
            
            
            product = cart.cart_product
            if product :
                if not product.discount:
                    item_discount = 0
                else:
                    item_discount = product.discount
                
                before_discount_price = (product.price) * (quantity)
                discount = item_discount/ 100
                discount_amount = discount * before_discount_price
                after_discount_price = before_discount_price - discount_amount
                grand_total = grand_total + after_discount_price
                product_list.append(
                    {
                        "product_name": product.product_name,
                        "product_id": product.id,
                        "price": product.price,
                        "description": product.description,
                        "quantity": quantity,
                        "discount": product.discount,
                        "category": product.category.category_name,
                        "discount_amount":discount_amount,
                        "before_discount_price": before_discount_price,
                        "after_discount_price": after_discount_price,
                    }
                )
                
        return {"message": product_list, "grand_total": grand_total}, 200
    except Exception as e:
        print(f"Error at get_cart_items_implementation{str(e)}")
        return f"message: {str(e)}", 400


def remove_cart_items_services(user_data,id):
    try:
        if not id :
            return {"message":"id not found"},401
        product = Products.query.get(id)
        if not product:
            return{"message":"product not found"}
        for cart in product.cart_item_relation:
            db.session.delete(cart)
            db.session.commit()
            response = f"cart item {cart.id} removed sucessfully"
            return {"message":response}
        return{"message":"item not found"}
    except Exception as e:
        print(f"Error at remove_cart_items_implementation{str(e)}")
        return f"message: {str(e)}", 400

