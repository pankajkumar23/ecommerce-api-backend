from database.db import db
from sqlalchemy import ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import datetime
from datetime import date

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    address_id = db.Column(db.Integer, ForeignKey("address.id"), nullable=False)
    final_bill_amount = db.Column(db.Float, nullable=False)
    order_status =  db.Column(db.String(), nullable=False)
    order_payment_relation = relationship("Payments", backref="order_payment")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    order_items = relationship("Order_Items", backref="order_items")
    delivery_status = db.Column(db.String(), nullable=False) 
    delivery_date = db.Column(db.Date, default=date.today())
 
    
    

