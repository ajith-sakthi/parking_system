from pydantic import BaseModel
from typing import List


class TokenData(BaseModel):
    username:str | None = None

class Something(BaseModel):
    feedback:str

class Feedback(BaseModel):
    getFeedbackList : List[Something]

