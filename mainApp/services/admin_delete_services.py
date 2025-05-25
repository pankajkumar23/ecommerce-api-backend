from flask import jsonify
from models.product_model import Products
from database.db import db
from models.user_model import Users

def delete_product_services(id):
    try:
        if not id:
          return {"message":"id not found"},404
        product = Products.query.get(id)
        if product and product.id == id:
            db.session.delete(product)
            db.session.commit()
            response = f"sucessfully deleted product {product.id}"
            return jsonify({"message": response}), 200
        return {"message": "product not found"}, 400
    except Exception as e:
        print(f"Error at delete_products_implementation {str(e)}")
        return f"message: {str(e)}", 400


def delete_user_services(id):
    try:
        if not id:
          return {"message":"id not found"},404
        user = Users.query.get(id)
        if user and user.role !="admin" and user.id == id:
            db.session.delete(user)
            db.session.commit()
            for user_product in user.product:
                if user_product:
                    db.session.delete(user_product)
                    db.session.commit()
            response = f"sucessfully deleted product {user.id}"
            return jsonify({"message": response}), 200
        return {"message": "product not found"}, 400
    except Exception as e:
        print(f"Error at delete_user_implementation{str(e)}")
        return f"message: {str(e)}", 400
    
    