from typing import List

from pydantic import BaseModel

from models.algo.command import Command


class AlgoResponse(BaseModel):
    commands:List[Command]
