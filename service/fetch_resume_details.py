from pymongo.collection import Collection
from bson import ObjectId

def get_user_resume_details(user_id: str, collection: Collection):
    """
    Retrieve resume details for a specific user.

    Parameters:
    - user_id: ID of the user
    - collection: MongoDB collection instance (e.g., resume_collection)

    Returns:
    - Dictionary with resume details or None if not found
    """
    result = collection.find_one({"user_id": user_id}, {"_id": 0, "resume_data": 1})
    return result.get("resume_data") if result else None