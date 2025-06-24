from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
db = client["public"]

# Initializing collections
users_collection = db["users"]
generated_interview_collection = db["generated_interviews"]
tags_collection = db["interview_tags"]
resume_collection = db["user_resume"]
answers_collection = db["interview_answers"]


# Create index on uid for faster access
async def init_indexes():
    await users_collection.create_index([("uid", ASCENDING)], unique=True)
    await generated_interview_collection.create_index([("title", "text")])
    await tags_collection.create_index([("name", ASCENDING)], unique=True)
    await resume_collection.create_index("user_id")