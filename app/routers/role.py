from fastapi import APIRouter,status, Depends
from app import schemas,models
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import APIResponse
from typing import List
from fastapi.responses import JSONResponse
from app.repository import role
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/role",
    tags=["role"]
    )

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=APIResponse[schemas.RoleResponse])
def create_role(request:schemas.RoleBase,db:Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return role.create(request,db)

@router.get("/{role_id}",status_code=status.HTTP_200_OK,response_model=APIResponse[schemas.RoleResponse])
def get_role(role_id:int, db:Session = Depends(get_db)):
    return role.get(role_id,db)

@router.get("/",status_code=status.HTTP_200_OK, response_model=APIResponse[List[schemas.RoleResponse]])
def get_role_all(db:Session = Depends(get_db)):
    return role.get_all(db)

@router.delete("/{role_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
def delete_role(role_id, db: Session = Depends(get_db), get_current_user: schemas.UserResponse = Depends(get_current_user)):
    return role.delete(role_id,db)