from typing import List, Optional
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., min_length=5)
    isbnID: str = Field(..., min_length=5, max_length=20)
    notes: Optional[str]
    tags: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "title": "Jonathon Livingston Seagull",
                "isbnID": "9780684846842",
                "notes": "To Read",
                "tags": [
                    "motivational"
                ]
            }
        }