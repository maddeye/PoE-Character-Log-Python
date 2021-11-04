#!/usr/bin/python3

# Core
import logging
import json
import time
import traceback

from os.path import exists

from utils.db import DB
from utils.api import API
from utils.config import CONFIG
from utils.pob import POB


def loop():
    config = CONFIG()
    api = API()
    pob = POB()
    db = None

    while True:

        for account in config.get("accounts"):

            db = DB(f"./db/{account}.db")

            try:
                character_to_scan = config.get("characters")

                characters = api.get_chars(account)

                for char in characters:

                    if character_to_scan != [] and char not in character_to_scan:
                        continue

                    # Get Passives tree
                    char["passives"] = json.dumps(
                        api.get_passive_tree(account, char["name"])
                    )

                    # Get Items
                    char["items"] = json.dumps(api.get_items(account, char["name"]))

                    char["pob"] = pob.pob_code_from_char(char)

                    db.store_character(char)

                    logging.info(
                        f"Logger character {char['name']} from account {account}"
                    )

                    time.sleep(config.get("longsleep"))

            except Exception as err:
                trace = traceback.format_exc()
                logging.error(err)
                logging.error(trace)

                time.sleep(config.get("longsleep"))

            db.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s::%(levelname)s: %(message)s",
        handlers=[logging.FileHandler("poeclog.log"), logging.StreamHandler()],
    )

    loop()
