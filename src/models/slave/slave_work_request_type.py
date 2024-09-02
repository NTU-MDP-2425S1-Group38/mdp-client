from enum import Enum


class SlaveWorkRequestType(str, Enum):
    Algorithm = "ALGORITHM"
    ImageRecognition = "IMAGE_RECOGNITION"
