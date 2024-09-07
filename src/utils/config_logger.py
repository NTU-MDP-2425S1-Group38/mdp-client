import logging


def init_logger() -> None:

    # Formatting stuff
    log_format = '[%(levelname)s][%(filename)s:%(lineno)s][%(asctime)s] %(message)s'
    date_format = '%Y:%m:%d, %H:%M'

    # Sets config for logging to file
    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        level=logging.DEBUG
    )

    # Add StreamHandler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logging.getLogger().addHandler(console_handler)
