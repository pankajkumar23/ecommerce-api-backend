from models.product_model import Products
from flask import Flask, Blueprint, jsonify, request
from models.user_model import Users
from models.category_model import Category

def get_products_services(page, per_page,user_data):
    try:
        
        product_list=[]
        user_id = user_data["id"]
        user = Users.query.get(user_id)
        if user:
            for user_product in user.product:
                category_name=user_product.category.category_name
                product_list.append( {
                "product_id": user_product.id,
                "product_name": user_product.product_name,
                "description": user_product.description,
                "price": user_product.price,
                "quantity": user_product.quantity,
                "discount":user_product.discount,
                "category": category_name,})
        return jsonify({"user_id":user_id,"products":product_list}),200
    except Exception as e:
        print(f"Error at get_products_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400




def get_category_services():
    try:
        categories_list = []
        categories = Category.query.all()
        for category in categories:
            categories_list.append({"category_name": category.category_name, "category_id": category.id})
        return {"categories":categories_list},200
    except Exception as e:
        print(f"Error at get_category_implementation {str(e)}")
        return f"message: {str(e)}", 400
