from typing import List

import numpy as np
import cv2
import base64
import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results
from utils.cv.determine_model_abs_path import determine_model_abs_path


class CV:

    @staticmethod
    def __determine_best_device() -> str:
        if torch.cuda.is_available():
            print("CUDA Detected!")
            return "cuda:0"
        if torch.backends.mps.is_available():
            print("MPS Detected!")
            return "mps"
        print("Using CPU for inference!")
        return "cpu"

    def __init__(self, name:str):
        self.device = self.__determine_best_device()
        self.model = YOLO(determine_model_abs_path(name), task="segment")

    def predict(self, image: np.array, show:bool = False) -> List[Results]:
        return self.model.predict(image, device=self.device, show=show)

    def decode_predict(self, image_str: str, show:bool = False) -> List[Results]:
        """
        Method to decode base64 image to be predicted on.
        1. Decodes images from base64 to numpy array
        2. Performs inference on image
        :param show:
        :param image_str:
        :return:
        """

        # Decode Image to numpy array
        image = np.frombuffer(base64.b64decode(image_str))

        # Predict Image
        return self.predict(image, show=show)



