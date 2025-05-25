from pydantic import BaseModel,validator

class AddressValidations(BaseModel):
    address :str
    country :str
    city : str
    state :str
    postalcode: int

    @validator("address","country","city","state")
    def string_validate(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value
    @validator("postalcode")
    def int_validate(value):
        if value =="":
            raise Exception(" field must be filled!!")
        return value




