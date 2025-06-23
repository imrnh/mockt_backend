from fastapi import APIRouter, HTTPException
from api.database import tags_collection
from api.models.interview import TagIn, TagOut
from bson import ObjectId

router = APIRouter()

