from typing import List

from pydantic import BaseModel

from models.algo.obstacle import Obstacle


class SlaveWorkRequestPayloadAlgo(BaseModel):
    obstacles: List[Obstacle]
