import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

MONGO_URI = os.getenv("DATABASE")  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://10.0.57.10:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


client = AsyncIOMotorClient(MONGO_URI)
db = client["cheatsheets_db"]
collection = db["cheatsheets"]

@app.get("/")
async def root():
    return {"You need to specify an endpoint"}

@app.get("/ids")
async def get_ids():
    documents = await collection.find({}, {"_id": 1}).to_list(length=None)
    ids = [str(doc["_id"]) for doc in documents]
    return {"ids": ids}

@app.get("/{name}")
async def get_cheatsheet(name: str):
    cheatsheet = await collection.find_one({"_id": name})

    if cheatsheet:
        cheatsheet["_id"] = str(cheatsheet["_id"])
        return cheatsheet
    else:
        raise HTTPException(status_code=404, detail="Cheatsheet not found")
