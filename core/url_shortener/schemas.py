from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


class URLCreateSchema(BaseModel):
    url : str = Field(...,description="Enter the long URL")

class URLResponseSchema(BaseModel):
    url : str = Field(...,description="Enter the long URL")
    short_code : str = Field(...,description=f"short url")
    created_at :datetime = Field(...,description="creation date and time of the task")

    model_config = {
        "from_attributes": True
    }