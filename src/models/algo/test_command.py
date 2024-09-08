from models.algo.command import Command


def test_create_command_from_json_string_command_only():
    payload = """
    {"cat": "control", "value": "CAPTURE_IMAGE", "end_position": {"x": 0, "y": 2, "d": 1}}
    """
    Command.model_validate_json(payload)


def test_create_command_from_json_string_direction_command_only():
    payload = """
    {"cat": "control", "value": "FORWARD", "end_position": {"x": 0, "y": 2, "d": 1}}
    """
    Command.model_validate_json(payload)


def test_create_command_from_json_string_direction_with_amount():
    payload = """
    {"cat": "control", "value": {"move":"FORWARD_RIGHT", "amount": 10}, "end_position": {"x": 0, "y": 2, "d": 1}}
    """
    Command.model_validate_json(payload)
