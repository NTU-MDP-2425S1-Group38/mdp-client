import base64
import io
import json
import logging
import multiprocessing
import os
import threading
from typing import List
from ultralytics.engine.results import Results
import websocket
import requests
import numpy as np
from models.algo.algo_req import AlgoRequest
from models.algo.algo_res import AlgoResponse
from models.algo.command import Command
from models.cv.cv_res import CvResponse
from models.cv.obstacle_label import ObstacleLabel, ModelClsToId
from models.slave.from_server.slave_work_request import SlaveWorkRequest
from models.slave.from_server.slave_work_request_payload_algo import SlaveWorkRequestPayloadAlgo
from models.slave.from_server.slave_work_request_payload_img_rec import SlaveWorkRequestPayloadImageRecognition
from models.slave.slave_work_request_type import SlaveWorkRequestType
from modules.slave.algo.algo import Algo
from modules.slave.cv.cv import CV
from PIL import Image


class Slave:
    """
    Class to register the device as a "client" to the RPI.
    """

    logger = logging.getLogger("Slave")

    def __init__(self, url:str, model_name:str):
        self.logger.info("Starting slave!")
        self.url = url
        self.ws = websocket.WebSocket()
        self.cv = CV(model_name)
        self.algo = Algo()

        # Images to stitch
        self.results: List[Results] = []

    def _decode_image(self, image_str:str) -> Image:
        # Decode the Base64 string into bytes
        image_bytes = base64.b64decode(image_str)

        # Load the bytes into a BytesIO buffer
        buffer = io.BytesIO(image_bytes)

        # Open the buffer as a Pillow Image
        return Image.open(buffer)

    @staticmethod
    def _fire_and_forget_stitch_images_and_show(arg_images: List[Results]):
        max_height: int = 0
        total_width: int = 0
        images: List[Image] = []

        # Iterate over results
        for r in arg_images:

            class_indices = r.boxes.cls

            for i in range(len(class_indices)):
                r.boxes.names[i] = f"ID: {ModelClsToId(r.boxes.cls[i])} | {r.boxes.names[i]}"


            cur_image = Image.fromarray(r.plot()[:, :, [2, 1, 0]])
            images.append(cur_image)

            max_height = max(max_height, cur_image.height)
            total_width += cur_image.width

        # Construct new image
        stitched = Image.new('RGB', (total_width, max_height))
        cur_width = 0
        for i in images:
            stitched.paste(i, (cur_width, 0))
            cur_width += i.width

        stitched.show("Stitched Images")

    def _stitch_images_and_show(self) -> None:
        # Copy results to avoid thread safety issues
        results_copy = self.results.copy()
        # Start the image stitching in a new thread
        p = multiprocessing.Process(target=self._fire_and_forget_stitch_images_and_show, args=(results_copy,))
        p.start()




    def _handle_algo(self, payload: SlaveWorkRequestPayloadAlgo, req_id: str) -> AlgoResponse:
        self.logger.info(f"Algo: Received payload! {payload}")
        req_data = AlgoRequest(obstacles=payload.obstacles)
        res = requests.post(f"{os.environ.get('ALGO_URL')}/algo/live", json=req_data.model_dump())
        res_data = AlgoResponse.model_validate(res.json())
        res_data.id = req_id
        self.logger.info(f"Algo: Response prepared! {res_data.model_dump()}")
        return res_data

    def _handle_cv(self, payload: SlaveWorkRequestPayloadImageRecognition, req_id: str) -> CvResponse:
        print("Received image request!")
        img = self._decode_image(payload.image)

        res = self.cv.predict(img)

        for result in [res[0]]:
            # Get confidence scores and class indices
            # result.show()

            # Append to images to stitch
            self.results.append(result)

            confidences = result.boxes.conf
            class_indices = result.boxes.cls

            highest_confidence_label = ObstacleLabel.Unknown
            highest_confidence = 0

            for c in range(len(confidences)):

                current_label = ObstacleLabel(self.cv.model.names[int(class_indices[c])])

                self.logger.info(f'Label: {current_label},\t Confidence: {confidences[c]},\t Skip: {current_label == ObstacleLabel.Shape_Bullseye and payload.ignore_bullseye}')

                # Get the corresponding class label
                if confidences[c] > highest_confidence:
                    if current_label == ObstacleLabel.Shape_Bullseye and payload.ignore_bullseye:
                        continue

                    highest_confidence = confidences[c]
                    highest_confidence_label = current_label

        self._stitch_images_and_show()

        return CvResponse(label=ObstacleLabel(highest_confidence_label), id=req_id)



    def run(self) -> None:
        """
        Main running loop of the slave.
        :return:
        """

        self.ws.connect(f"{self.url}/ws/connect")

        while True:
            raw_request = self.ws.recv()
            print("Received request!")
            request = SlaveWorkRequest.model_validate(json.loads(raw_request))
            # self.ws.send_text("this will fail")

            if isinstance(request.payload, SlaveWorkRequestPayloadAlgo):
                # Do Algo Stuff
                res = self._handle_algo(request.payload, request.id)
                self.ws.send_text(res.model_dump_json())

            if isinstance(request.payload, SlaveWorkRequestPayloadImageRecognition):
                # Do CV stuff
                res = self._handle_cv(request.payload, request.id)
                self.ws.send_text(res.model_dump_json())



