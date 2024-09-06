from pydantic import BaseModel, Field

from models.algo.direction import Direction


class Obstacle(BaseModel):
    id: int = Field(default=0)
    x: int
    y: int
    d: Direction
