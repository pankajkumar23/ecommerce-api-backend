from flask import jsonify
import stripe
import stripe.error
from models.payment_model import Payments
from models.user_model import Users
from database.db import db
from models.order_items_model import Order_Items
from models.order_model import Orders
from datetime import date
import datetime
from models.address_model import Address

def verify_webhook_signature(payload,sig_headers, webhook_endpoint_secret):
    try:
        event = stripe.Webhook.construct_event(payload,sig_headers,  webhook_endpoint_secret)
        
    except ValueError as e :
        print("invalid payload: {e}")
        return e
    except stripe.error.SignatureVerificationError as e:
        print("invalid signature: {e}")
        return e
    if event["type"]=="checkout.session.completed":
        amount_total = event.data.object["amount_total"]
        email = event.data.object["customer_email"]
        id =event.data.object['id']
        user_id =event.data.object['metadata']['user_id']
        order_id =event.data.object['metadata']['order_id']
        payment_status=event.data.object["payment_status"]
        payment_method=event.data.object["payment_method_types"][0]
        order_items = Order_Items.query.filter_by(order_id=order_id).all()
        address_id =1
        address= Address.query.get(address_id)
        for order_item in order_items:
            if order_item:
                order_item.payment_status = payment_status
                order_item.payment_method =payment_method
                db.session.commit()
        orders = Orders.query.filter_by(id=order_id).all()
        for order in orders:
            if order:
                order.order_status="confirmed"
                order.delivery_status="payment_confirmed"
                order.address_id = 1
                order.delivery_date = date.today() + datetime.timedelta(days=3)
        user= Users.query.filter_by(email=email).first()
        if user:
            payment = Payments(
                user_id=user.id,
                order_id=order_id ,
                payment_amount=amount_total / 100,
                payment_status=payment_status,
                payment_method=payment_method)
            db.session.add(payment)
            db.session.commit()
        print("payment sucessfull")
    if event["type"]=="checkout.session.expired":
        print("session.expired")
    return "success",200
    
    
    
    
def create_checkout_session(final_bill_amount,user_data):
    try:
        user_email = user_data["email"]
        user_id=user_data["id"]
        order_id = 1
        result =check_payment_status(order_id)
        if isinstance(result,tuple):
            return result
        order_id = result
        total_amount = final_bill_amount * 100
        session = stripe.checkout.Session.create(
            metadata={
        "user_id": user_id,
        "order_id": order_id },
            customer_email=user_email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Total Order',
                    },
                    'unit_amount': total_amount,
                },
                'quantity': 1,
            },],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='https://localhost:8000/cancel',)
        return jsonify({'session_data': session})
    except Exception as e:
        return jsonify(error=str(e)), 404



def check_payment_status(order_id):
    try:
        payments= Order_Items.query.filter_by(order_id=order_id).all()
        for payment in payments:
            if payment.payment_status=="paid":
                return jsonify({"message":"payment already done !!"}),400
            order_item =payment.order_id
            return order_item
    except Exception as e:
        return jsonify(error=str(e)), 404
