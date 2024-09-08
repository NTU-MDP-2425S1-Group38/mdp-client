from models.algo.algo_res import AlgoResponse
import json


def test_create_algo_response():

    payload = """
    {
      "commands": [
        {
          "cat": "control",
          "value": {
            "move": "FORWARD",
            "amount": 24
          },
          "end_position": {
            "x": 0,
            "y": 2,
            "d": 1
          }
        },
        {
          "cat": "control",
          "value": "FORWARD_RIGHT",
          "end_position": {
            "x": 4,
            "y": 7,
            "d": 3
          }
        },
        {
          "cat": "control",
          "value": {
            "move": "FORWARD",
            "amount": 9
          },
          "end_position": {
            "x": 5,
            "y": 7,
            "d": 3
          }
        },
        {
          "cat": "control",
          "value": "FORWARD_RIGHT",
          "end_position": {
            "x": 10,
            "y": 3,
            "d": 1
          }
        },
        {
          "cat": "control",
          "value": {
            "move": "BACKWARD",
            "amount": 15
          },
          "end_position": {
            "x": 10,
            "y": 4,
            "d": 1
          }
        },
        {
          "cat": "control",
          "value": "BACKWARD_LEFT",
          "end_position": {
            "x": 13,
            "y": 7,
            "d": 4
          }
        },
        {
          "cat": "control",
          "value": "CAPTURE_IMAGE",
          "end_position": {
            "x": 13,
            "y": 7,
            "d": 4
          }
        },
        {
          "cat": "control",
          "value": "FIN",
          "end_position": {
            "x": 13,
            "y": 7,
            "d": 4
          }
        }
      ]
    }
    """

    AlgoResponse.model_validate_json(payload)


