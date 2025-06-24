import os
import uuid
from fastapi import APIRouter, HTTPException, Header, Request
from firebase_admin import auth as firebase_auth
from pdf2image import convert_from_path
from pymongo.collection import Collection
from bson import ObjectId

from api.firebase import *  
from api.database import users_collection, resume_collection
from api.models.user import UserIn
from api.models.interview import PDFConversionRequest
from api.service.ocr import image_ocr

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




# Configuration
OUTPUT_FOLDER = "api/lib"


@router.post("/extract_resume_information")
async def convert_pdf_to_images(request: Request, payload: PDFConversionRequest):
    """
    Convert PDF to images, extract resume info using Gemini, and store in MongoDB.
    """
    # Validate
    if not os.path.exists(payload.pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")

    if not payload.pdf_path.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Unique output folder
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(OUTPUT_FOLDER, unique_id)
    os.makedirs(output_path, exist_ok=True)

    try:
        # Convert PDF to images
        image_paths = convert_from_path(
            payload.pdf_path,
            dpi=300,
            output_folder=output_path,
            output_file=unique_id,
            fmt='png',
            paths_only=True
        )

        # Extract resume info using Gemini
        extracted_info = await image_ocr(image_paths)

        # Get user_id from middleware (attached to request state)
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in request")

        # Store in MongoDB
        resume_collection.insert_one({
            "user_id": user_id,
            "resume_data": extracted_info,
            "pdf_file": payload.pdf_path,
            "unique_id": unique_id
        })

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
    


