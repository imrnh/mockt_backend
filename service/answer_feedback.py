from google import genai

import os
from dotenv import load_dotenv
load_dotenv()


def get_interview_feedback(answer_text, question_text, job_role):
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=GEMINI_API_KEY)

  prompt = f"""
        You are an expert hiring manager conducting an interview for the {job_role} role.
        Please evaluate the following answer of a candidate for given question.

        Question asked: {question_text}

        Answer of the user: {answer_text}

        Your generated answer must always follow this json template: 

        {{
        "score": int, # here you would rank it in a scale of 1-10
        "feedback": "string" # here tell the candidate what went wrong or why you liked their answer.
        }}

        Please remember, feedback must be no more than 20 words.

    """
  response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

  return response.text