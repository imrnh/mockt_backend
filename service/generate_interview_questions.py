
from google import genai

from api.service.interview_qgen_prompt import get_interview_generation_prompt
import os
from dotenv import load_dotenv
load_dotenv()


def generate_interview_questions(job_role, user_resume, job_description, interview_difficulty, question_count):
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=GEMINI_API_KEY)

  prompt = get_interview_generation_prompt(job_role, user_resume, job_description, interview_difficulty, question_count)
  response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

  return response.text
