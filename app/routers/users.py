from fastapi import APIRouter, Depends, status
from .. import schemas
from ..database import get_db
from ..schemas import APIResponse
from sqlalchemy.orm import Session
from typing import List
from ..repository import users
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=APIResponse[schemas.UserResponse])
def create_user(request:schemas.UserCreate ,db:Session = Depends(get_db)):
    return users.create(request,db)

@router.get("/",status_code=status.HTTP_200_OK, response_model=APIResponse[List[schemas.UserResponse]])
def get_user_all(db:Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return users.get_all(db)
         
@router.get("/{user_id}",status_code=status.HTTP_200_OK, response_model=APIResponse[schemas.UserResponse])
def get_user(user_id:int, db:Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return users.get(user_id,db)
    
@router.delete("/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(user_id,db:Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return users.delete(user_id,db)     
    
#response_model=schemas.UserResponse
@router.put("/{user_id}",status_code=status.HTTP_200_OK, response_model=APIResponse[schemas.UserResponse])
def update_user(user_id,request:schemas.UserCreate ,db:Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return users.update(user_id,request,db)