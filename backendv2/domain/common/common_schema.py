from pydantic import BaseModel

class PostResponse(BaseModel):
    status: str
    message: str