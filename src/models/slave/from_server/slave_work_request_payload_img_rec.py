from pydantic import BaseModel


class SlaveWorkRequestPayloadImageRecognition(BaseModel):
    image: str  # Base64 encoded image (UTF-8)
