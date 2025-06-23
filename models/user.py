from pydantic import BaseModel

class UserIn(BaseModel):
    uid: str
    email: str
    name: str
