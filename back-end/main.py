import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = os.getenv("DATABASE")  

app = FastAPI()

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["cheatsheets_db"]
collection = db["cheatsheets"]

@app.get("/")
async def root():
    return {"message": "Welcome to the Cheatsheet API"}

@app.get("/{name}")
async def get_cheatsheet(name: str):
    cheatsheet = await collection.find_one({"_id": name})

    if cheatsheet:
        cheatsheet["_id"] = str(cheatsheet["_id"])  # Convert ObjectId to string
        return cheatsheet
    else:
        raise HTTPException(status_code=404, detail="Cheatsheet not found")
