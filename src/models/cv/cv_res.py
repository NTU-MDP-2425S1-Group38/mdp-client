from typing import Optional
from pydantic import BaseModel
from models.cv.obstacle_label import ObstacleLabel


class CvResponse(BaseModel):
    label: Optional[ObstacleLabel]
