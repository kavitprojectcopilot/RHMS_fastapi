from fastapi import status
from .. import schemas,models
from ..hashing import Hash
from ..schemas import APIResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .role import get
from typing import List
from fastapi.responses import JSONResponse

def create(request:schemas.UserCreate ,db:Session):

    try:                
        if request.first_name == None or len(request.first_name.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The First_Name Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                         
        elif request.last_name == None or len(request.last_name.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Last_Name Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                 
        elif request.email == None or len(request.email.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Email Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                             
        elif request.country == None or len(request.country.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Country Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                          
        elif request.state == None or len(request.state.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The State Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                       
        elif request.city == None or len(request.city.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The City Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                    
        elif request.role_id == None or request.role_id <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Role ID Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                                        
        elif get(request.role_id,db).status == False :    
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Role with this role_id {request.role_id} is not found"
            } , status_code=status.HTTP_404_NOT_FOUND)                                                                                
        elif request.password == None or len(request.password.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Password Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                                            
        elif len(request.password) < 8 and len(request.password) > 16 :
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Password must be at least 8 characters no more than 16 characters"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                           


        existing_email = db.query(models.User).filter(models.User.email == request.email).first()
        if existing_email:
            return JSONResponse(
                content={
                    "status":False,
                    "detail":None,
                    "message":f"This EmailID {request.email} is already available"
                } , status_code=status.HTTP_409_CONFLICT)                         
                
        user = models.User(
                            first_name=request.first_name,
                            last_name=request.last_name,
                            email=request.email,
                            country=request.country,
                            state=request.state,
                            city=request.city,
                            role_id=request.role_id,
                            password=Hash.encrypt(request.password)                       
                        )
        db.add(user)
        db.commit()
        db.refresh(user)
                
        return APIResponse(
                status=True,
                detail=user,
                message="User Created Successfully"
            )
    except IntegrityError:
        db.rollback()      
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : Database integrity error"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                           
    except Exception as e:
        db.rollback()
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                 


def get_all(db:Session):
    try:
        users = db.query(models.User).all()
        return APIResponse(
                status=True,
                detail=users,
                message=f"Successfully Get All Users"
            )       
    except Exception as e:        
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                 
         
def get(user_id:int, db:Session):
    try:        
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"User with this id {user_id} is not found"
            } , status_code=status.HTTP_404_NOT_FOUND)               

        return APIResponse(
                status=True,
                detail=user,
                message=f"user get Successfully"
            )      
    except Exception as e:        
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                 

    
def delete(user_id,db:Session):
    try:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
        return JSONResponse(content={
                    "status":True,
                    "detail":None,
                    "message":f"Role id {user_id} is deleted Successfully"
            }, status_code=status.HTTP_200_OK)
    except Exception as e: 
        db.rollback()      
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
             
def update(user_id,request:schemas.UserCreate ,db:Session):

    try:        
        user = db.query(models.User).filter(models.User.id == user_id)
        if not user.first():
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"User with this id {user_id} is not found"
            } , status_code=status.HTTP_404_NOT_FOUND)             
        if request.first_name == None or len(request.first_name.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The First_Name Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                         
        elif request.last_name == None or len(request.last_name.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Last_Name Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                 
        elif request.email == None or len(request.email.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Email Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                             
        elif request.country == None or len(request.country.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Country Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                          
        elif request.state == None or len(request.state.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The State Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                       
        elif request.city == None or len(request.city.strip()) <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The City Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                    
        elif request.role_id == None or request.role_id <= 0:
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Role ID Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                                        
        elif get(request.role_id,db).status == False :    
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Role with this role_id {request.role_id} is not found"
            } , status_code=status.HTTP_404_NOT_FOUND)                                                                                
        elif request.password == None or len(request.password.strip()) <= 0:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"The Password Field is Required"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                                            
        elif len(request.password) < 8 and len(request.password) > 16 :
             return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Password must be at least 8 characters no more than 16 characters"
            } , status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)                                                                                
            
        existing_email = db.query(models.User).filter(models.User.email == request.email).first()
        useremail =  user.first().email                
        if existing_email != None :
             if existing_email.email != useremail:
                return JSONResponse(
                content={
                    "status":False,
                    "detail":None,
                    "message":f"This EmailID {request.email} is already available"
                } , status_code=status.HTTP_409_CONFLICT)                                                                                                
                
        user.update({
                            "first_name":request.first_name,
                            "last_name":request.last_name,
                            "email":request.email,
                            "country":request.country,
                            "state":request.state,
                            "city":request.city,
                            "role_id":request.role_id,
                            "password":Hash.encrypt(request.password)                       
                        })                
        db.commit()                                 
        return APIResponse(
                status=True,
                detail=user.first(),
                message=f"user Updated Successfully"
            )     
    except IntegrityError:
        db.rollback()      
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : Database integrity error"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                           
    except Exception as e:
        db.rollback()
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                 
        
