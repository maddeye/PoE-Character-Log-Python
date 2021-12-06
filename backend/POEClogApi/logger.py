import logging


class Logger:

    def __init__(self):
        # Setup logger
        self.logger = logging.getLogger("poeclogapi_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        fh = logging.FileHandler("logs/poeclogapi.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        # logging to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    
    def log(self, msg: str, level: int = logging.INFO):
        self.logger.log(level, msg)