from database.db import db
from sqlalchemy.orm import relationship


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    hash_password = db.Column(db.String(), nullable=False, unique=True)
    role = db.Column(db.String(), nullable=False)
    address_relation = relationship("Address", backref="user_address")
    order_relation = relationship("Orders", backref="user_order")
    user_cart_relation = relationship("CartItem", backref="user_cart")

