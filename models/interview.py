from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
class AnswerItem(BaseModel):
    answer_text: str
    score: int
    feedback: str

class QuestionItem(BaseModel):
    question: str
    sample_answer: str
    answers: List[AnswerItem] = []  # default to empty list

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


class InterviewAnswer(BaseModel):
    answer_text: str
    question_text: str
    job_role: str


class AnswerEntry(BaseModel):
    content: str
    feedback: Optional[str] = ""
    score: int
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

class InterviewAnswerCreate(BaseModel):
    interview_id: str
    answer_index: int
    answer_entry: AnswerEntry