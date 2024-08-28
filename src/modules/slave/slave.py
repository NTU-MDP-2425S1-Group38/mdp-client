import time
import websocket


class Slave:
    """
    Class to register the device as a "client" to the RPI.
    """

    def __init__(self, url:str):
        self.url = url
        self.ws = websocket.WebSocket()
        self.ws.connect(f"{url}/ws/connect")


    def run(self) -> None:
        """
        Main running loop of the slave
        :return:
        """

        while True:
            self.ws.send("Hello!")
            print(self.ws.recv())
            time.sleep(1)
