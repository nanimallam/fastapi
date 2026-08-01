from pydantic import BaseModel

class MobileCreate(BaseModel):
    brand:str
    model:str
    price:float
    color:str


class MobileResponse(MobileCreate):
    id:int

    model_config={
        "from_attributes":True
    }