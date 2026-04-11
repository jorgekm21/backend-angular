from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import Product as ProductSchema, User as UserSchema
from model import ProductDB
from deps import get_db, get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    products = db.query(ProductDB).all()
    return [ProductSchema.model_validate(p) for p in products]

@router.get("/{product_id}", response_model=ProductSchema)
def get_product_by_id(product_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="El id del producto no existe")
    return ProductSchema.model_validate(product)

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_product = ProductDB(
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio,
        stock=product.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductSchema.model_validate(new_product)

@router.delete("/{product_id}")
def delete_product_by_id(product_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="El id del producto no existe")
        
    db.delete(product)
    db.commit()
    return {"message": "Producto eliminado exitosamente", "product": {"id": product.id, "nombre": product.nombre, "descripcion": product.descripcion, "precio": product.precio}}
