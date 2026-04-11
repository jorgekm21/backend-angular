from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import User as UserSchema, UserCreate
from model import UserDB
from deps import get_db, get_current_user
from security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    users = db.query(UserDB).all()
    return [UserSchema.model_validate(u) for u in users]

@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="El id del usuario no existe")
    return UserSchema.model_validate(user)

@router.post("/", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_user = UserDB(
        nombre=user.nombre,
        email=user.email,
        edad=user.edad
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserSchema.model_validate(new_user)

@router.delete("/{user_id}")
def delete_user_by_id(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)):
    
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="El id del usuario no existe")
        
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente", "user": {"id": user.id, "nombre": user.nombre, "email": user.email, "edad": user.edad}}
