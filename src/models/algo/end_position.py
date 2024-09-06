from pydantic import BaseModel

from models.algo.direction import Direction


class EndPosition(BaseModel):
    x: int
    y: int
    d: Direction
