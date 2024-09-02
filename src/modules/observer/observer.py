import websocket


class Observer:

    def __init__(self, url:str):
        self.url = url
        self.ws = websocket.WebSocket()
        self.ws.connect(f"{self.url}/ws/observe")

    def run(self):
        while True:
            print(self.ws.recv())
