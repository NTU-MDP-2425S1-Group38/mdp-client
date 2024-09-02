
import torch
from ultralytics import YOLO
from utils.cv.determine_model_abs_path import determine_model_abs_path


class CV:

    @staticmethod
    def __determine_best_device() -> str:
        if torch.cuda.is_available():
            return "cuda:0"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def __init__(self, name:str):
        self.model = YOLO(determine_model_abs_path(name))
        self.device = self.__determine_best_device()

    def predict(self, image):
        raise NotImplementedError

