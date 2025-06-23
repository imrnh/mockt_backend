from fastapi import APIRouter, HTTPException, Query
from api.database import preset_interview_collection, tags_collection
from api.models.interview import PresetInterviewIn
from api.models.interview import TagIn, TagOut
from bson import ObjectId
from typing import List


router = APIRouter()

# Create new tag -- only admin access
@router.post("/add_preset")
async def add_preset(preset: PresetInterviewIn):
    try:
        result = await preset_interview_collection.insert_one(preset.dict())
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Search by title
@router.get("/search/title")
async def search_by_title(q: str = Query(..., min_length=1)):
    # MongoDB text search, sort by text score
    cursor = preset_interview_collection.find(
        {"$text": {"$search": q}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])

    results = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"]) 
        del doc["_id"]  
        results.append(doc)

    if not results:
        raise HTTPException(status_code=404, detail="No interviews found matching title")

    return results



# Search by multiple tags, rank by number of matched tags descending
@router.get("/search/tags")
async def search_by_tags(tags: List[str] = Query(..., min_length=1)):
    # MongoDB aggregation pipeline to count matching tags
    pipeline = [
        {
            "$match": {
                "tags": {"$in": tags}
            }
        },
        {
            # Calculate how many tags matched with input tags
            "$addFields": {
                "matched_tags_count": {
                    "$size": {
                        "$setIntersection": ["$tags", tags]
                    }
                }
            }
        },
        {
            "$sort": {"matched_tags_count": -1}
        }
    ]

    cursor = preset_interview_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]    
        results.append(doc)

    if not results:
        raise HTTPException(status_code=404, detail="No interviews found matching tags")

    return results




"""
    Interview Tags
"""

@router.post("/tags", response_model=TagOut)
async def create_tag(tag: TagIn):
    # Check if tag already exists
    existing = await tags_collection.find_one({"name": tag.name})
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    result = await tags_collection.insert_one(tag.dict())
    new_tag = await tags_collection.find_one({"_id": result.inserted_id})
    return TagOut(id=str(new_tag["_id"]), name=new_tag["name"])

@router.get("/tags", response_model=list[TagOut])
async def list_tags():
    tags_cursor = tags_collection.find()
    tags = []
    async for tag in tags_cursor:
        tags.append(TagOut(id=str(tag["_id"]), name=tag["name"]))
    return tags
