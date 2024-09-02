from typing import Union

from pydantic import BaseModel, field_validator, ValidationError

from models.slave.from_server.slave_work_request_payload_algo import SlaveWorkRequestPayloadAlgo
from models.slave.from_server.slave_work_request_payload_img_rec import SlaveWorkRequestPayloadImageRecognition
from models.slave.slave_work_request_type import SlaveWorkRequestType


class SlaveWorkRequest(BaseModel):
    type: SlaveWorkRequestType
    payload: Union[SlaveWorkRequestPayloadAlgo, SlaveWorkRequestPayloadImageRecognition]

    @classmethod
    @field_validator("payload", mode="before")
    def __validate_payload(cls, value, values):
        if values["type"] == SlaveWorkRequestType.Algorithm:
            return SlaveWorkRequestPayloadAlgo(**value)
        if values["type"] == SlaveWorkRequestType.ImageRecognition:
            return SlaveWorkRequestPayloadImageRecognition(**value)

        raise ValidationError("'Type' not defined in request!")


