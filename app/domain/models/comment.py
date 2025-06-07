from pydantic import BaseModel

class Comment(BaseModel):
    id: str
    media_id: str
    text: str

    class Config:
        orm_mode = True
