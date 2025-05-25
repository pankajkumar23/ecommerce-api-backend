from database.db import db
from sqlalchemy import ForeignKey,PrimaryKeyConstraint

class CartItem(db.Model):
    __tablename__= "cart_item"
    product_id = db.Column(db.Integer,ForeignKey("products.id"),nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(user_id,product_id),
        )


