from pydantic import BaseModel, Field


class SlaveWorkRequestPayloadImageRecognition(BaseModel):
    image: str  # Base64 encoded image (UTF-8)
    ignore_bullseye: bool = Field(default=False)
