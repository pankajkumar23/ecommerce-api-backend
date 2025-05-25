from pydantic import BaseModel,EmailStr,validator

class SighinUserValidations(BaseModel):
    email: EmailStr
    password :str
    username : str
    role : str
    
    
    @validator("email","password","username","role")
    def validate(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value
    


