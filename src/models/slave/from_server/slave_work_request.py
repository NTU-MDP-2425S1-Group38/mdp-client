from typing import Union, Optional

from pydantic import BaseModel, field_validator, ValidationError

from models.slave.from_server.slave_work_request_payload_algo import SlaveWorkRequestPayloadAlgo
from models.slave.from_server.slave_work_request_payload_img_rec import SlaveWorkRequestPayloadImageRecognition
from models.slave.slave_work_request_type import SlaveWorkRequestType
from pydantic import Field


class SlaveWorkRequest(BaseModel):
    id:str
    type: Optional[SlaveWorkRequestType] = Field(default=None)
    payload: Union[SlaveWorkRequestPayloadAlgo, SlaveWorkRequestPayloadImageRecognition]

    @classmethod
    @field_validator("payload", mode="before")
    def __validate_payload(cls, value, values):
        request_type = values.get("type")

        if request_type == SlaveWorkRequestType.Algorithm:
            return SlaveWorkRequestPayloadAlgo(**value)
        elif request_type == SlaveWorkRequestType.ImageRecognition:
            return SlaveWorkRequestPayloadImageRecognition(**value)

        # Check if type is missing or not provided
        raise ValidationError(f"'Type' not defined in request: {request_type}")

