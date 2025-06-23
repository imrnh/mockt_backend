from fastapi import APIRouter, HTTPException, Header
from firebase_admin import auth as firebase_auth

from api.firebase import *  
from api.database import users_collection 
from api.models.user import UserIn


router = APIRouter()

@router.post("/register")
async def store_user(user: UserIn, authorization: str = Header(...)):
    try:
        # Verify Firebase token
        token = authorization.replace("Bearer ", "")
        decoded_token = firebase_auth.verify_id_token(token)
        firebase_uid = decoded_token.get("uid")

        if user.uid != firebase_uid:
            raise HTTPException(status_code=403, detail="Invalid user token")

        # Upsert user in MongoDB
        await users_collection.update_one(
            {"uid": user.uid},
            {"$set": {"email": user.email, "name": user.name}},
            upsert=True
        )

        return {"status": "success", "message": "User stored"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
