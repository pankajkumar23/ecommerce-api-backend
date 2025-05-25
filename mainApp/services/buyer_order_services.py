from flask import request
from models.cart_model import CartItem
from database.db import db
from models.order_model import Orders
from models.order_items_model import Order_Items
from models.product_model import Products

def order_product_services(user_data):
    try:
        final_bill_amount = 0
        order_item = []
        user_id = user_data["id"]
        carts = CartItem.query.all()
        address_id = 1
        orders = Orders(user_id=user_id, final_bill_amount=0, order_status="pending",delivery_status="pending",)
        db.session.add(orders)
        db.session.flush()
        for cart in carts:
            quantity = cart.quantity
            product = cart.cart_product
            unit_price = product.price
            product_discount = product.discount
            if not product_discount:
                item_discount = 0
            else:
                item_discount = product_discount
            sub_total = unit_price * quantity
            discount = item_discount / 100
            discount_amount = discount * sub_total
            total = sub_total - discount_amount
            final_bill_amount = final_bill_amount + total

            order_item.append(
                {
                    "user_id": user_id,
                    "product_id": product.id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "sub_total": sub_total,
                    "discount_amount": discount_amount,
                    "total": total,
                }
            )

        for item in order_item:

            user_id = item["user_id"]
            product_id = item["product_id"]
            quantity = item["quantity"]
            unit_price = item["unit_price"]
            sub_total = item["sub_total"]
            discount_amount = item["discount_amount"]
            total = item["total"]

            order_items = Order_Items(
                order_id=orders.id,
                product_id=product_id,
                unit_price=unit_price,
                sub_total=sub_total,
                discount_amount=discount_amount,
                total_amount=total,
                quantity=quantity,
            )
            db.session.add(order_items)
            final_bill_amount 
            orders.final_bill_amount = final_bill_amount
            db.session.commit()
        return {
            "message": "product sucessfully added to order",
            "orders_id":orders.id,
            "order_items": order_item,
            "final_bill_amount": final_bill_amount,
        }
    except Exception as e:
        print(f"Error at order_product_implementation{str(e)}")
        return f"message: {str(e)}", 400



def get_order_details_services(user_data):
    try:
        final_bill_amount = 0
        product_list = []
        order_list = []
        total_saving_amount= 0
        user_id = user_data["id"]
        orders = Orders.query.filter_by(user_id=user_id).all()
        for order in orders:
            order_address = order.order_address
            address_data = {
                "address": order_address.address,
                "postalcode": order_address.postalcode,
                "country": order_address.country,
                "city": order_address.city,
                "state": order_address.state,
            }

            order_items = Order_Items.query.all()
            for order_item in order_items:
                order_product = order_item.product_order
                final_bill_amount = final_bill_amount + order_item.total_amount
                total_saving_amount += order_item.discount_amount
                product_list.append(
                    {
                        "product_name": order_product.product_name,
                        "product_id": order_item.product_id,
                        "unit_price": order_item.unit_price,
                        "description": order_product.description,
                        "quantity": order_item.quantity,
                        "discount": order_product.discount,
                        "category": order_product.category.category_name,
                        "sub_total": order_item.sub_total,
                        "discount_amount":order_item.discount_amount,
                        "total_amount": order_item.total_amount,
                        "payment_status": order_item.payment_status,
                    }
                )
            order_list.append(
                {
                    "user_id": user_id,
                    "order": product_list,
                    "delivery_status": order.delivery_status,
                    "delivery_date": order.delivery_date,
                    "delivery_address":address_data
                }
            )
        return {
            "order_details": order_list,
            "total_saving_amount":total_saving_amount,
            "final_bill_amount": final_bill_amount,
            "payment_status":order_item.payment_status
        }, 200
    except Exception as e:
        print(f"Error at get_order_details_implementation{str(e)}")
        return f"message: {str(e)}", 400


def remove_order_services(user_data,id):
    try:
        if not id :
            return {"message":"product parameter not found"},401
        product = Products.query.get(id)
        if not product:
            return{"message":"product not found"}
        for order in product.order_relation:
            db.session.delete(order)
            db.session.commit()
            response = f"order item {order.id} removed sucessfully"
            return {"message":response}
        return{"message":"item not found"}
    except Exception as e:
        print(f"Error at remove_order_implementation{str(e)}")
        return f"message: {str(e)}", 400
