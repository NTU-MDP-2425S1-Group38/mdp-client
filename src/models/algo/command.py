from enum import Enum
from typing import Union

from pydantic import BaseModel, Field, field_validator, ValidationError

from models.algo.end_position import EndPosition


class MoveDirection(str, Enum):
    Forward = "FORWARD"
    ForwardRight = "FORWARD_RIGHT"
    ForwardLeft = "FORWARD_LEFT"
    Backward = "BACKWARD"
    BackwardRight = "BACKWARD_RIGHT"
    BackwardLeft = "BACKWARD_LEFT"


class MoveInstruction(BaseModel):
    move: MoveDirection
    amount: float


class CommandInstruction(str, Enum):
    Finish = "FIN"
    Capture = "CAPTURE_IMAGE"


class Command(BaseModel):
    cat:str = Field(default="control")
    end_position: EndPosition
    value: Union[CommandInstruction, MoveInstruction]

    @classmethod
    @field_validator("value", mode="before")
    def validate_value(cls, value, values):
        if isinstance(value, dict) and "move" in value:
            # If it's a MoveInstruction, validate it accordingly
            return MoveInstruction(**value)
        elif isinstance(value, str):
            # If it's a CommandInstruction, validate it as a string Enum
            if value in CommandInstruction.__members__.values():
                return CommandInstruction(value)
        else:
            raise ValidationError("Invalid value for 'value' field!")
