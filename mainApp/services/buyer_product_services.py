from flask import Flask, Response, request, make_response, jsonify
from models.product_model import Products
import json
from models.category_model import Category
from models.cart_model import CartItem
from database.db import db

def increase_product_quantity(id):
    try:
        
        product = Products.query.get(id)
        if not product :
            return jsonify({"message": "Product not found"}), 400

        products = request.cookies.get("product")
        
        if products:
            product_list =json.loads(products)
        else:
            product_list=[]

        for item in product_list:
            if item["product_id"]==id:
              
                if item["quantity"] >=product.quantity:
                    return {"message": "Product out of stock"}, 400 
                item["quantity"] += 1
                break
        else :
            product_list.append({"product_id" : id, "quantity": 1})
        
        payload = {"message": "item added", "item": product_list}
        resp = make_response(jsonify(payload), 200)
        resp.set_cookie("product", json.dumps(product_list))
       
        return resp
    except Exception as e:
        print(f"Error at increase_product_quantity{str(e)}")
        return f"message: {str(e)}", 400


def get_buying_products_services(product_name=None, price=None):

    try:
        product_list = []
        query=Products.query
        if price is not None :
            price_range =500
            min_price = price-price_range
            max_price = price+price_range
            query=query.filter(Products.price.between(min_price,max_price))
        if product_name :
           query = query.filter(Products.product_name == product_name)
        products = query.all()
        for product in products:
            category = Category.query.get(product.category_id)
            product_list.append({
                "product_name": product.product_name,
                "product_id": product.id,
                "price": product.price,
                "description": product.description,
                "quantity": product.quantity,
                "discount":product.discount,
                "category": category.category_name})
        return {"message": product_list}, 200
    except Exception as e:
        print(f"Error at get_all_buying_products_implementation{str(e)}")
        return f"message: {str(e)}", 400


def decrease_product_quantity_services(id):
    try:

        if not id:
           return {"message":"id not found"},404
        product = Products.query.get(id)
        if not product :
            return jsonify({"message": "Product not found"}), 400

        product_id = request.cookies.get("product")
        
        if product_id:
            product_list =json.loads(product_id)
        else:
            product_list=[]
        for item in product_list:
            if item["product_id"]==id:
                if item["quantity"] <= 1:
                    return {"message":"quantity cannot decrease"}
                item["quantity"] -= 1
                break
           
        else :
            product_list.append({"product_id" : id, "quantity": 1})

        quantity = item["quantity"]
        update_cart_quantity = CartItem.query.filter_by(product_id=id).first()
        if update_cart_quantity:
            update_cart_quantity.quantity = quantity
            db.session.commit()
        
        payload = {"message": "item added", "item": product_list}
        resp = make_response(jsonify(payload), 200)
        resp.set_cookie("product", json.dumps(product_list))
        return resp
    except Exception as e:
        print(f"Error at add_to_cart_implementation{str(e)}")
        return f"message: {str(e)}", 40