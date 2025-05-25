from pydantic import BaseModel,validator
import re

class EditUserValidation(BaseModel):
    email: str
    username : str
    role :str
    
   
    @validator("role")
    def validate(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value

    @validator("email")
    def email_validate(value):
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value)
        if not valid:
            raise Exception(" invalid email address!!")
        return value