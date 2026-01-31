from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return "Hello World"

@app.get("/user")
def show():
    return {"status":True,"detail":{"name":"kavit","email":"kavit@gmail.com"},"message":"Successfully show"}
