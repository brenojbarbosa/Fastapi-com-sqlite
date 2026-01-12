from pydantic import BaseModel
from typing import Optional




class CarSchema(BaseModel):
    brand:str
    model:str
    color:Optional[str] = None
    factory_year:Optional[int] = None
    model_year:Optional[int] = None
    description:Optional[str] = None


class CarPublic(BaseModel):
    brand: str
    model: str
    color: Optional[str] = None
    factory_year: Optional[int] = None
    model_year: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CarPartialUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    factory_year: Optional[int] = None
    model_year: Optional[int] = None
    description: Optional[str] = None

class CarList(BaseModel):
    cars: list[CarPublic]

