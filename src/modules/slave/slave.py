import json
import logging
import os
import websocket
import requests

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


class Slave:
    """
    Class to register the device as a "client" to the RPI.
    """

    logger = logging.getLogger("Slave")

    def __init__(self, url:str):
        self.logger.info("Starting slave!")
        self.url = url
        self.ws = websocket.WebSocket()
        self.cv = CV("best_v8i.onnx")
        self.algo = Algo()

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

        res[0].show()
        print(res)

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
