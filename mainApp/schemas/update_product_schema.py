from pydantic import BaseModel,validator

class UpdateProductValidations(BaseModel):
    product_name: str
    description: str
    price: int
    category: str
    quantity :int 
    discount:int

    @validator("product_name","description","category")
    def validate_string(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value
    
    @validator("price","quantity")
    def validate_integer(value):
        if value <=0:
            raise Exception("value must be greater than 0")
        return value

    @validator("discount")
    def validate(value):
        if value=="":
            raise Exception(" field must be filled!!")
        return value
