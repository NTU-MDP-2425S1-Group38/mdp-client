import os


def determine_model_abs_path(name:str) -> str:
    """
    This function resolves the absolute path of a file in /src/files/
    :param name:
    :return:
    """
    return f"{os.path.dirname(__file__)}/../../files/{name}"

