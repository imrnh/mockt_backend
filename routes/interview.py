from fastapi import APIRouter, HTTPException, Query, Request
from api.database import generated_interview_collection, tags_collection, resume_collection, answers_collection
from api.service.generate_interview_questions import generate_interview_questions
from api.service.tts import generate_speech_from_text
from api.models.interview import InterviewAnswerCreate, PresetInterviewIn, InterviewSessionRequest
from api.models.interview import TagIn, TagOut, InterviewAnswer
from api.service.answer_feedback import get_interview_feedback

import json
from bson import ObjectId
from typing import List


router = APIRouter()

"""
    TODO:
        Ask AI to make new interview questions. 
        Then write the push to DB logic here.
        Send the interview data to the frontend.

        Frontend will call AI to convert question text into audio if user wants audio format.
        If user response is in audio, frontend captures that, send the bytes to backend.
        Backend then generates text from that audio.
        This is actually done every 1sec of speaking instead of for whole time the user is speaking.
        This helps keeping the delay minimum.
        In the backend, when speech is converted to text, it is accumulted by frontend. 
        And when finally completes answering, the ans is sent to backend with API call for evaluation along with q id and interview id.
        Question is evaluated and evaluation result is sent to the frontend.
        For each question in DB, we save all user tried answers and their evaluation.

"""


@router.post("/create_interview_session")
async def make_new_interview_session(payload: InterviewSessionRequest, request: Request):
    job_role = payload.job_role
    job_description = payload.job_description
    interview_difficulty = payload.interview_difficulty
    question_count = payload.question_count
    user_id = request.state.user_id


    # Fetch user resume
    user_resume_doc = await resume_collection.find_one({"user_id": user_id})
    if not user_resume_doc or "resume_data" not in user_resume_doc:
        raise HTTPException(status_code=404, detail="User resume not found.")
    
    user_resume = user_resume_doc["resume_data"]

    if isinstance(user_resume, dict):
        user_resume = user_resume['raw_text']

    # Call provided generation function
    questions_output = generate_interview_questions(
        job_role,
        user_resume,
        job_description,
        interview_difficulty,
        question_count
    )

    # Save to DB
    preset_data = payload.dict()
    preset_data["questions"] = questions_output
    preset_data["user_id"] = user_id

    result = await generated_interview_collection.insert_one(preset_data)

    return {
        "status": "success",
        "inserted_id": str(result.inserted_id),
        "questions": questions_output
    }


@router.post("/generate_question_audio")
async def generate_question_audio(request: Request):
    # Get user ID from request
    user_id = request.state.user_id
    
    # Find the most recent interview session for this user
    interview_session = await generated_interview_collection.find_one(
        {"user_id": user_id},
        sort=[("_id", -1)]  # Get the most recent one
    )
    
    if not interview_session:
        raise HTTPException(status_code=404, detail="No interview session found for this user")
    
    try:
        # Parse the questions JSON string
        questions_data = json.loads(interview_session["questions"].strip("```json\n").strip("```"))
        questions_list = questions_data["questions"]
        
        # Extract just the question texts
        question_texts = [q["question"] for q in questions_list]
        
        # Generate audio for each question
        audio_paths = []
        for question in question_texts:
            audio_path = await generate_speech_from_text(question)
            audio_paths.append({
                "question": question,
                "audio_path": audio_path
            })
            
        return {
            "status": "success",
            "message": "Audio generated for all questions",
            "audio_files": audio_paths,
            "interview_id": str(interview_session["_id"])
        }
        
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing interview questions: {str(e)}"
        )

# Create new tag -- only admin access
@router.post("/add_preset")
async def add_preset(preset: PresetInterviewIn):
    try:
        result = await generated_interview_collection.insert_one(preset.dict())
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""

    Create, Search Interview Questions.

"""

# Search by title
@router.get("/search/title")
async def search_by_title(q: str = Query(..., min_length=1)):
    # MongoDB text search, sort by text score
    cursor = generated_interview_collection.find(
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

    cursor = generated_interview_collection.aggregate(pipeline)
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

# Create a new tag
@router.post("/tags", response_model=TagOut)
async def create_tag(tag: TagIn):
    # Check if tag already exists
    existing = await tags_collection.find_one({"name": tag.name})
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    result = await tags_collection.insert_one(tag.dict())
    new_tag = await tags_collection.find_one({"_id": result.inserted_id})
    return TagOut(id=str(new_tag["_id"]), name=new_tag["name"])

# Get all available tags
@router.get("/tags", response_model=list[TagOut])
async def list_tags():
    tags_cursor = tags_collection.find()
    tags = []
    async for tag in tags_cursor:
        tags.append(TagOut(id=str(tag["_id"]), name=tag["name"]))
    return tags




"""

 Interview Session

"""

@router.post("/evaluate_interview_answer")
def evaluate_interview(intv: InterviewAnswer):
    feedback = get_interview_feedback(answer_text=intv.answer_text, question_text=intv.question_text, job_role=intv.job_role)
    return feedback



@router.post("/submit_answer/")
async def submit_answer(payload: InterviewAnswerCreate):
    interview_obj_id = ObjectId(payload.interview_id)
    field_key = f"answers.answer_{payload.answer_index}"

    update_result = await answers_collection.update_one(
        {
            "interview_id": interview_obj_id,
        },
        {
            "$push": {field_key: payload.answer_entry.dict()}
        },
        upsert=True
    )

    if update_result.upserted_id:
        return {"message": "Answer created", "id": str(update_result.upserted_id)}
    return {"message": "Answer updated"}