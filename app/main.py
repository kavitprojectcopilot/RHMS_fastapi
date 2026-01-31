from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .exceptions.handlers import (
    validation_exception_handler,
    http_exception_handler
)
from . import models 
from .database import engine
from .routers import authentication, users, role


app = FastAPI()

models.Base.metadata.create_all(engine)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(role.router)

