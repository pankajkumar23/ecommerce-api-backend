from database.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


user_product = db.Table(
    "user_product",
    db.Column("user_id", ForeignKey("users.id")),
    db.Column("user_product_id", ForeignKey("products.id")),
)


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey("category.id"), nullable=False)
    user_relation = relationship("Users", secondary=user_product, backref="product")
    cart_item_relation = relationship("CartItem", backref="cart_product")
    order_relation = relationship("Order_Items", backref="product_order")
