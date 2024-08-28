"""
Main running script to subscribe to the RPI.
"""

import argparse
from multiprocessing import Process
from typing import List

from modules.observer.observer import Observer
from modules.slave.slave import Slave


def entry_slave(url:str) -> None:
    """
    Target for new process to begin image recognition
    :url str: Base URL for sockets to connect to
    :return:
    """
    slave = Slave(url)
    slave.run()


def entry_observe(url:str) -> None:
    """
    Target for new process to observe the logs from the rpi
    :url str: Base URL for sockets to connect to
    :return:
    """
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

    parser.add_argument("-u", "--url", required=True, type=str, help="Sets the url, e.g. ws://localhost:8080")
    parser.add_argument("-s", "--slave", action="store_true", help="Runs client as slave")
    parser.add_argument("-o", "--observe", action="store_true", help="Subscribe to logs from the rpi")

    args = parser.parse_args()

    processes: List[Process] = []

    if args.slave:
        processes.append(Process(target=entry_slave, args=(args.url,)))

    if args.observe:
        processes.append(Process(target=entry_observe, args=(args.url,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()








if __name__ == "__main__":
    main()
