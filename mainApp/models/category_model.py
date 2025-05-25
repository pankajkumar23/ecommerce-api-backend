from database.db import db
from sqlalchemy.orm import relationship

class Category(db.Model):
    __tablename__= "category"
    id = db.Column(db.Integer,primary_key= True)
    category_name= db.Column(db.String(),nullable= False)
    product_relation =  relationship("Products" ,backref="category")
    
