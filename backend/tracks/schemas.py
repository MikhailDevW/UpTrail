# import json
from pydantic import BaseModel


class UploadTrack(BaseModel):
    title: str
    description: str
    is_public: bool = True
