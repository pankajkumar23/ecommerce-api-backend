from database.db import db
from models.product_model import Products
from flask import Flask, Blueprint, jsonify, request
from enums.product_category import ProductCategory
from models.user_model import Users
from models.category_model import Category



def add_product_details(data,user_data):
    try:

        user_id = user_data["id"]
        for product_category in ProductCategory:
            category_name =product_category.name
            if data.category == category_name:
                category = Category.query.filter_by(category_name=category_name).first()
                update_category = category
                if category is None:
                    update_category = Category(category_name=category_name)
                    db.session.add(update_category)
                    db.session.commit()
                    return update_category
                user = Users.query.get(user_id)
                for user_product in user.product:
                    if data.product_name == user_product.product_name:
                        return {"message": "product already existing"}, 400
                product = Products(
                    product_name=data.product_name,
                    description=data.description,
                    category_id=update_category.id,
                    price=data.price,
                    quantity=data.quantity,
                    discount=data.discount
                )
                db.session.add(product)
                db.session.commit()
                product.user_relation.append(user)
                db.session.commit()
                return (
                    jsonify(
                        {
                            "product_name": product.product_name,
                            "description": product.description,
                            "price": product.price,
                            "quantity": product.quantity,
                            "category": update_category.category_name,
                            "discount":product.discount
                        }
                    ),
                    200,
                )
        return {"message": "category not found"}
    except Exception as e:
        print(f"Error at add_product_details {str(e)}")
        return f"message: {str(e)}", 400




def update_product_details(id,data,user_data):
    try: 
        user_id = user_data['id']
        user = Users.query.get(user_id)
        for user_product in user.product:
            if user_product.id == id:
                if data.product_name:
                    user_product.product_name  = data.product_name
                    user_product.description  = data.description
                    user_product.price  = data.price
                    user_product.category_id  = user_product.category_id 
                    user_product.quantity = data.quantity
                    user_product.discount = data.discount

                if data.description:
                    user_product.description  = data.description
                elif data.price :
                    user_product.price  = data.price
                elif data.category :
                    user_product.category_id  = user_product.category_id 
                elif data.quantity:
                    user_product.quantity = data.quantity
                elif data.discount:
                    user_product.discount = data.discount
                db.session.commit()
            if user_product.id != id:
                return {"message":"product not found!!!"},401
        return {"message":"product updated successfully"},200
    except Exception as e:
        print(f"Error at update_product_details {str(e)}")
        return f"message: {str(e)}", 400


def delete_products_services(id,user_data):
    try:
        user_id = user_data["id"]
        user = Users.query.get(user_id)
        for user_product in user.product:
            if user_product.id == id:
                db.session.delete(user_product)
                db.session.commit()
                response = f"sucessfully deleted product {user_product.id}"
                return jsonify({"message": response}), 200
        return {"message": "product not found"}, 400
    except Exception as e:
        print(f"Error at delete_products_implementation {str(e)}")
        return f"message: {str(e)}", 400
