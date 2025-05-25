from database.db import db
from sqlalchemy import ForeignKey
import datetime

class Payments(db.Model):
    __tablename__= "payments"
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,nullable=False)
    order_id = db.Column(db.Integer,ForeignKey("orders.id"),nullable=False)
    payment_method = db.Column(db.String(),nullable=False)
    payment_amount = db.Column(db.Float,nullable=False)
    payment_status = db.Column(db.String(),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    
