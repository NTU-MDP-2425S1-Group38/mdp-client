import json
import time
import websocket

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

    def __init__(self, url:str):
        self.url = url
        self.ws = websocket.WebSocket()
        self.ws.connect(f"{url}/ws/connect")
        self.cv = CV("best_v8i.onnx")
        self.algo = Algo()

    def __handle_algo(self, payload: SlaveWorkRequestPayloadAlgo) -> None:
        print("Algo!")
        print(payload)
        self.ws.send_text("Test algo!")

    def __handle_cv(self, payload: SlaveWorkRequestPayloadImageRecognition) -> None:
        print("CV!")
        print(payload)
        res = self.cv.decode_predict(payload.image)

        res[0].show()
        print(res)

        self.ws.send_text("Test CV!")

    def run(self) -> None:
        """
        Main running loop of the slave.
        :return:
        """

        while True:
            raw_request = self.ws.recv()
            print(raw_request)
            request = SlaveWorkRequest(**json.loads(raw_request))
            print(request)

            if request.type == SlaveWorkRequestType.Algorithm:
                # Do Algo Stuff
                self.__handle_algo(request.payload)

            if request.type == SlaveWorkRequestType.ImageRecognition:
                # Do CV stuff
                self.__handle_cv(request.payload)
