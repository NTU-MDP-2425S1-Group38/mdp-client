import json
import logging
import os
from typing import List
from ultralytics.engine.results import Results
import websocket
import requests
import numpy as np
from models.algo.algo_req import AlgoRequest
from models.algo.algo_res import AlgoResponse
from models.algo.command import Command
from models.cv.cv_res import CvResponse
from models.cv.obstacle_label import ObstacleLabel
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

    def _stitch_images_and_show(self) -> None:

        max_height:int = 0
        total_width:int = 0
        images:List[Image] = []

        # Iterate over results
        for r in self.results:
            cur_image = Image.fromarray(r.plot())
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
        res = self.cv.decode_predict(payload.image)

        for result in res:
            # Get confidence scores and class indices
            result.show()

            # Append to images to stitch
            self.results.append(result)

            confidences = result.boxes.conf
            class_indices = result.boxes.cls

            if len(confidences) > 0:
                # Find the index of the highest confidence score
                max_conf_index = confidences.argmax()

                # Get the corresponding class label
                highest_confidence_label = self.cv.model.names[int(class_indices[max_conf_index])]
                highest_confidence = confidences[max_conf_index]

                print(f'Label: {ObstacleLabel(highest_confidence_label)}, Confidence: {highest_confidence}')
                return CvResponse(label=ObstacleLabel(highest_confidence_label), id=req_id)

            else:
                print('No detections found.')

        self._stitch_images_and_show()

        return CvResponse(label=ObstacleLabel.Unknown, id=req_id)


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

