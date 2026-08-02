from pydantic import BaseModel, EmailStr




class MobileCreate(BaseModel):
    brand: str
    model: str
    price: float
    color: str


class MobileResponse(MobileCreate):
    id: int

    model_config = {
        "from_attributes": True
    }




class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None



class OrderCreate(BaseModel):
    mobile_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    user_id: int
    mobile_id: int
    quantity: int
    total_price: float

    model_config = {
        "from_attributes": True
    }