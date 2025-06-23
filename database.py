# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# import os
# from dotenv import load_dotenv
# load_dotenv()


# uri = os.getenv('MONGO_URL')

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

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
preset_interview_collection = db["preset_interview"]
tags_collection = db["interview_tags"]



# Create index on uid for faster access
async def init_indexes():
    await users_collection.create_index([("uid", ASCENDING)], unique=True)
    await preset_interview_collection.create_index([("title", "text")])
    await tags_collection.create_index([("name", ASCENDING)], unique=True)

