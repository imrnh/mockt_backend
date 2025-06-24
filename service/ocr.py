from google import genai
from typing import List
from google.genai import types


import os
from dotenv import load_dotenv
load_dotenv()


async def image_ocr(image_paths: List[str]) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    extracted_text = ""

    for path in image_paths:
        img_bytes = open(path, "rb").read()

        contents = [
            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
            "Extract structured resume details: skills, education, experience, projects, other works, etc. Please do not generate anything additional. Just give me structured output."
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        extracted_text += response.text + "\n"

    return {"raw_text": extracted_text.strip()}
