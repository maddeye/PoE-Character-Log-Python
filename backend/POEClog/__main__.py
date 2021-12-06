import logging
import time

import POEClog.config as config

from POEClogDatabase.database import Database
from POEClog.scheduler import SafeScheduler
from POEClog.screener import Screener


def main():
    """Start POECLog"""

    # Setup logger
    logger = logging.getLogger("poeclog_logger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh = logging.FileHandler("logs/poeclog.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    # logging to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Setup config
    logger.info("Esure settings file exists and is readable")
    config.ensure_config_path()

    # Database setup
    db = Database(logger)
    logger.info("Creating database schema if it doesn't already exist")
    db.create_database()

    # Screener
    screener = Screener(logger, db)

    # Scheduler
    schedule = SafeScheduler(logger)
    schedule.every(config.get("shortsleep")).seconds.do(screener.scan).tag("scanning")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
