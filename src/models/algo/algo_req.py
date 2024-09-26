from typing import List

from pydantic import BaseModel, Field, model_serializer

from models.algo.obstacle import Obstacle


class AlgoRequest(BaseModel):
    cat: str = Field(default="obstacles")
    obstacles: List[Obstacle]
    mode: int = Field(default=0)
    server_mode: str = "live"
    algo_type: str = "Exhaustive Astar"

    @model_serializer()
    def _serialise(self):
        return {
            "cat": self.cat,
            "value": {"obstacles": self.obstacles, "mode": self.mode},
        }
