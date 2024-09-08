from typing import List

from pydantic import BaseModel, validator, ValidationError

from models.algo.command import Command, CommandInstruction, MoveInstruction


class AlgoResponse(BaseModel):
    commands:List[Command]
