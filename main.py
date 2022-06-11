'''Main.py'''
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    '''Root'''
    return {"message":"Hello World"}