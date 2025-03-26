import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from bson import ObjectId

# Ensure MONGO_URI is set
MONGO_URI = os.getenv("DATABASE")
if not MONGO_URI:
    raise ValueError("DATABASE environment variable is not set!")

# Connect to MongoDB
try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
except Exception as e:
    print(f"An Invalid URI host error was received.\n {e}")
    sys.exit(1)  # Exit if DB connection fails

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://(?:.*\.)?behdadf\.com",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Database and Collection
db = client["cheatsheets_db"]
collection = db["cheatsheets"]

@app.get("/")
async def root():
    return {"message": "You need to specify an endpoint"}

@app.get("/ids")
async def get_ids():
    documents = await collection.find({}, {"_id": 1}).to_list(length=None)
    ids = [str(doc["_id"]) for doc in documents]
    return {"ids": ids}

@app.get("/{name}")
async def get_cheatsheet(name: str):
    try:
        object_id = ObjectId(name)  # Convert name to ObjectId if necessary
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    cheatsheet = await collection.find_one({"_id": object_id})

    if cheatsheet is None:
        raise HTTPException(status_code=404, detail="Cheatsheet not found")

    cheatsheet["_id"] = str(cheatsheet["_id"])  # Convert ObjectId to string
    return cheatsheet
@app.get("/cheatsheets/{name}")
async def get_cheatsheet_wth_id(name: str):
     cheatsheet = await collection.find_one({"_id": name})  # Assuming "_id" is the cheatsheet name
 
     if cheatsheet:
         cheatsheet["_id"] = str(cheatsheet["_id"])  # Convert ObjectId to string
         return cheatsheet
     else:
         raise HTTPException(status_code=404, detail="Cheatsheet not found")
