from pydantic import BaseModel
from typing import List

class QuestionItem(BaseModel):
    question: str
    sample_answer: str

class PresetInterviewIn(BaseModel):
    title: str
    questions: List[QuestionItem]
    tags: List[str] 


# Create interview tag
class TagIn(BaseModel):
    name: str

class TagOut(BaseModel):
    id: str
    name: str


