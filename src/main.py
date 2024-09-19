"""
Main running script to subscribe to the RPI.
"""
import os
import argparse
from multiprocessing import Process
from typing import List

from models.cv.obstacle_label import ObstacleLabel
from modules.observer.observer import Observer
from modules.slave.cv.cv import CV
from modules.slave.slave import Slave
from utils.config_logger import init_logger


def entry_slave(url:str, model_name: str) -> None:
    """
    Target for new process to begin image recognition
    :url str: Base URL for sockets to connect to
    :return:
    """
    init_logger()
    slave = Slave(url, model_name)
    slave.run()


def entry_observe(url:str) -> None:
    """
    Target for new process to observe the logs from the rpi
    :url str: Base URL for sockets to connect to
    :return:
    """
    init_logger()
    observer = Observer(url)
    observer.run()


def main():
    """
    Main running function of the application.
    """

    parser = argparse.ArgumentParser(
        prog="MDP Client",
        description="Run this on a client machine to perform the algorithm and image recognition features"
    )

    parser.add_argument(
        "-u", "--url", required=True, type=str, help="Sets the url of RPI host, e.g. ws://localhost:8080"
    )
    parser.add_argument(
        "-a", "--algo", required=True, type=str, help="Algorithm server base URL, e.g. http://localhost:8000"
    )
    parser.add_argument(
        "-m", "--model", required=True, type=str, help="Name of model to be used"
    )
    parser.add_argument("-s", "--slave", action="store_true", help="Runs client as slave")
    parser.add_argument("-o", "--observe", action="store_true", help="Subscribe to logs from the rpi")


    # Parse args and set env vars
    args = parser.parse_args()
    os.environ["SERVER_URL"] = args.url
    os.environ["ALGO_URL"] = args.algo

    if not (args.slave or args.observe):
        parser.error("At least --slave or --observe must be passed in!")

    processes: List[Process] = []

    if args.slave:
        processes.append(Process(target=entry_slave, args=(args.url,args.model,)))

    if args.observe:
        processes.append(Process(target=entry_observe, args=(args.url,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    # main()

    import cv2
    cv = CV("best_v8i_n.onnx")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        res = cv.predict(frame, show=False)

        for result in res:
            # Get confidence scores and class indices
            result.show()
            confidences = result.boxes.conf
            class_indices = result.boxes.cls

            if len(confidences) > 0:
                # Find the index of the highest confidence score
                max_conf_index = confidences.argmax()

                # Get the corresponding class label
                highest_confidence_label = cv.model.names[int(class_indices[max_conf_index])]
                highest_confidence = confidences[max_conf_index]

                print(f'Label: {ObstacleLabel(highest_confidence_label)}, Confidence: {highest_confidence}')
            else:
                print('No detections found.')
