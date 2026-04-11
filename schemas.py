from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int | None = None
    nombre: str
    email: str
    edad: int
    password_hash: str | None = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    nombre: str
    email: str
    edad: int
    password: str

class Product(BaseModel):
    id: int | None = None
    nombre: str
    descripcion: str
    precio: float
    stock: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
