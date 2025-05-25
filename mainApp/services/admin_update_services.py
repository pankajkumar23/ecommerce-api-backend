from flask import jsonify
from models.user_model import Users
from database.db import db
from models.product_model import Products
def update_user_services(id,data,user_data):
    try:
        if not id:
            return {"message":"id not found"},404
        user = Users.query.get(id)
        existing_user = Users.query.filter_by(email = data.email).first()
        if existing_user:
            return{"message":"email already existing!!"}
        if user and user.role!="admin":
            if data.email:
                user.email = data.email
            elif data.username =="":
                user.username = user.username
            elif data.username:
                user.username = data.username
            elif data.username:
                 data.username = user.username
            elif data.role:
                     user.role = user_data.role
            db.session.commit()
            return {"products":"user updated sucessfully!!" }, 200
        return {"message": "user not found"}, 200
    except Exception as e:
        print(f"Error at edit_user_implementation {str(e)}")
        return jsonify({"message": str(e)}), 400


def update_product_services(id,data):
    try: 
        if not id:
          return {"message":"id not found"},404
        products = Products.query.get(id)
        if products and products.id == id:
            if products.product_name:
                products.product_name  = data.product_name
                products.description  = data.description
                products.price  = data.price
                products.category_id  = products.category_id 
                products.discount = data.discount
                products.quantity = data.quantity
            if data.description:
                products.description  = data.description
            elif data.price :
                products.price  = data.price
            elif data.category :
                products.category_id  = products.category_id 
            elif data.quantity:
                products.quantity = data.quantity
            elif data.discount:
                products.discount = data.discount
            db.session.commit()
            return {"message":"product updated successfully"},200
        return {"message":"product not found!!!"},401
    except Exception as e:
        print(f"Error at update_product_by_admin {str(e)}")
        return f"message: {str(e)}", 400

