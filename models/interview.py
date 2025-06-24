from pydantic import BaseModel
from typing import List

class QuestionItem(BaseModel):
    question: str
    sample_answer: str

class PresetInterviewIn(BaseModel):
    title: str
    questions: List[QuestionItem]
    tags: List[str] 

class InterviewSessionRequest(BaseModel):
    job_role: str
    job_description: str
    interview_difficulty: str
    question_count: int

# Create interview tag
class TagIn(BaseModel):
    name: str

class TagOut(BaseModel):
    id: str
    name: str


class PDFConversionRequest(BaseModel):
    pdf_path: str
