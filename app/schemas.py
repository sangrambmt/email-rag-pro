from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    question: str
    top_k: int = 5
    file_filter: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
