import os

from models.algo.direction import Direction
from models.algo.obstacle import Obstacle
from models.slave.from_server.slave_work_request_payload_algo import SlaveWorkRequestPayloadAlgo
from modules.slave.slave import Slave


def test_handle_algo():
    os.environ["ALGO_URL"]="http://localhost:8000"
    slave = Slave("")
    payload = SlaveWorkRequestPayloadAlgo(
        obstacles=[
            Obstacle(x=3, y=3, d=Direction.South),
            Obstacle(x=8, y=8, d=Direction.East),
        ]
    )

    slave._handle_algo(payload)
