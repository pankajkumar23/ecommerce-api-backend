from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(db.Model):
    __tablename__="address"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("users.id"),nullable=False)
    address =db.Column(db.String(),nullable=False)
    postalcode =db.Column(db.Integer,nullable=False)
    country = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(),nullable=False)
    state = db.Column(db.String(),nullable=False)
    address_order_relation = relationship("Orders", backref="order_address")


    





    
