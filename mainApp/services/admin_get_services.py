from flask import jsonify
from models.user_model import Users
from models.product_model import Products

def get_user_product_services(id):
    try:
        if not id:
            return {"message":"id not found"},404
        all_product_data = []
        user = Users.query.get(id)
        if user and user.role!="admin":
            for product in user.product:
                category_name = product.category.category_name
                all_product_data.append(
                    {
                        "product_id": product.id,
                        "product_name": product.product_name,
                        "description": product.description,
                        "price": product.price,
                        "quantity": product.quantity,
                        "category": category_name,
                        "discount":product.discount,
                        })
            return {"products": all_product_data}, 200
        return {"message": "user not found"}, 200
    except Exception as e:
        print(f"Error at get_user_product_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400


def get_all_users_services():
    try:
        user_data_list =[]
        users = Users.query.all()
        for user in users:
            if user.role != "admin":
                user_data = {
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id,}
                user_data_list.append(user_data)
        return {"users":user_data_list},200
    except Exception as e:
        print(f"Error at get_all_users_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400


def get_all_products_services():
    try:
        all_product_data = {}
        product_user_data = {}
        user_data = {}
        user_data_list = []
        users = Users.query.all()
        products = Products.query.all()
        for user in users:
            if user.role != "admin":
                user_data = {
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id,}
                user_data_list.append(user_data)
        for product in products:
            for user_product in product.user_relation:
                category_name = product.category.category_name
                all_product_data = {
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "discount":product.discount,
                    "category": category_name,}
                product_id = user_product.id
                if product_id not in product_user_data:
                    product_user_data[product_id] = []
                product_user_data[product_id].append(all_product_data)
        for user_data in user_data_list:
           
            id = user_data["user_id"]
            user_data["products"] = product_user_data.get(id, [])
        return jsonify({"user_data": user_data_list}), 200
    except Exception as e:
        print(f"Error at get_products_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400
