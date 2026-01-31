from fastapi import APIRouter, status, HTTPException, Depends
from app import schemas, models, JWTtoken
from app.schemas import APIResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.hashing import Hash
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=APIResponse)
def login(request:schemas.Login , db:Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == request.email).first()
        if not user:
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"User with this email_id {request.email} is not found"
            } , status_code=status.HTTP_404_NOT_FOUND)             

        if not Hash.verify(user.password,request.password):
            return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Incorrect Password"
            } , status_code=status.HTTP_401_UNAUTHORIZED)             

        access_token = JWTtoken.create_access_token(data={"sub": user.email})        
        return APIResponse(
                status=True,
                detail={
                    "access_token":access_token,
                    "token_type":"bearer"
                },
                message="Login successfully"
            )
    except Exception as e:
        return JSONResponse(
             content={
                "status":False,
                "detail":None,
                "message":f"Error : {e}"
            } , status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        