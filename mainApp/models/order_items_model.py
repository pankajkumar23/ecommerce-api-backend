from database.db import db
from sqlalchemy import ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship

class Order_Items(db.Model):
    __tablename__ = "order_items"
    order_id = db.Column(db.Integer, ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey("products.id"), nullable=False)
    quantity =db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    sub_total = db.Column(db.Float, nullable=False)
    discount_amount= db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(), nullable=True) 
    payment_method = db.Column(db.String(), nullable=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'product_id'),
    )
                