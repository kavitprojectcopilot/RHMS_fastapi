from fastapi import status
from app import schemas,models
from sqlalchemy.orm import Session
from app.schemas import APIResponse
from fastapi.responses import JSONResponse

def create(request:schemas.RoleBase,db:Session):
    
    try:

        if len(request.role_name.strip()) <=0 or request.role_name == None:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Role_Name Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                             
        existing_role = db.query(models.Role).filter(models.Role.role_name == request.role_name).first()
        if existing_role:
             return JSONResponse(
                content={
                    "status":False,
                    "detail":None,
                    "message":f"This Role Name {request.role_name} is already available"
                } , status_code=status.HTTP_409_CONFLICT)                         
                
        
        role = models.Role(
             role_name=request.role_name
         )
        db.add(role)
        db.commit()
        db.refresh(role)

        return APIResponse(
                status=True,
                detail=role,
                message=f"Role Successfully Created"
            )
    except Exception as e:
            db.rollback()
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  

def get(role_id:int, db:Session):
    
     try:
          role = db.query(models.Role).filter(models.Role.id == role_id).first()
          if not role:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Role IS Not Found"
            } , status_code=status.HTTP_404_NOT_FOUND)             
         
          return APIResponse(
                    status=True,
                    detail=role,
                    message="Role is found it"
               )
     except Exception as e:          
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  

def get_all(db:Session):
    try:
        roles = db.query(models.Role).all()
        return APIResponse(
                    status=True,
                    detail=roles,
                    message=f"successfully get all roles"
               )
    except Exception as e:
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  

def delete(role_id, db: Session):
    try:
        db.query(models.Role).filter(models.Role.id == role_id).delete()
        db.commit()
        return APIResponse(
                    status=True,
                    detail=None,
                    message=f"Role id {role_id} is deleted Successfully"
            )
    except Exception as e:
        db.rollback()
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  
