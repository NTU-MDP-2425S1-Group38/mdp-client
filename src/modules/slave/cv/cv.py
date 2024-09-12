import io
import logging
from typing import List
from PIL import Image
import numpy as np
import cv2
import base64
import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results
from utils.cv.determine_model_abs_path import determine_model_abs_path


class CV:

    logger = logging.getLogger("CV")

    def __determine_best_device(self) -> str:
        if torch.cuda.is_available():
            self.logger.info("Using Cuda for inference!")
            return "cuda:0"
        self.logger.info("Using CPU for inference!")
        return "cpu"

    def __init__(self, name:str):
        self.device = self.__determine_best_device()
        self.model = YOLO(determine_model_abs_path(name), task="segment")

    def predict(self, image: Image, show:bool = False) -> List[Results]:
        return self.model.predict(image, device=self.device, show=show, verbose=False)

    def decode_predict(self, image_str: str, show:bool = False) -> List[Results]:
        """
        Method to decode base64 image to be predicted on.
        1. Decodes images from base64 to numpy array
        2. Performs inference on image
        :param show:
        :param image_str:
        :return:
        """

        # Decode the Base64 string into bytes
        image_bytes = base64.b64decode(image_str)

        # Load the bytes into a BytesIO buffer
        buffer = io.BytesIO(image_bytes)

        # Open the buffer as a Pillow Image
        decoded_image = Image.open(buffer)

        # Predict Image
        return self.predict(decoded_image, show=show)



