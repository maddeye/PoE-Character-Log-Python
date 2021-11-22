import json
import os
import time

from typing import Dict

import requests

from logging import Logger
from traceback import format_exc

from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

import POEClog.config as config

from POEClogDatabase.database import Database
from POEClog.pob import pob_code_from_char

POESITE = os.getenv("POESITE") or "https://www.pathofexile.com"
USER_AGENT = os.getenv("USER_AGENT") or "POEClog"


class Screener:
    def __init__(self, logger: Logger, db: Database):
        self.logger = logger
        self.db = db

        self.client = requests.session()
        self.client.headers.update({"User-Agent": USER_AGENT})

    def _make_safe_call(self, url: str, params: dict = {}) -> dict:
        try:
            response = self.client.get(url=url, params=params)

            if response.status_code != 200:
                raise Exception(
                    f"Error: failed to make api call to {url} with status code {response.status_code}"
                )

        except (
            ConnectTimeout,
            HTTPError,
            ReadTimeout,
            Timeout,
            ConnectionError,
        ):
            self.logger.error(f"Error on _make_safe_call...\n{format_exc()}")

        return response.json()

    def get_chars(self, account_name: str) -> Dict[str, str]:
        return self._make_safe_call(
            f"{POESITE}/character-window/get-characters?accountName={account_name}&realm=pc"
        )

    def get_passive_tree(self, account_name: str, character_name: str) -> dict:
        return self._make_safe_call(
            f"{POESITE}/character-window/get-passive-skills?reqData=0&accountName={account_name}&realm=pc&character={character_name}"
        )

    def get_items(self, account_name: str, character_name: str) -> dict:
        items = self._make_safe_call(
            url=f"{POESITE}/character-window/get-items",
            params={"accountName": account_name, "character": character_name},
        )

        return items["items"]

    def scan(self):
        try:
            for account in config.get("accounts"):
                characters_list = config.get("characters")

                for char in self.get_chars(account):
                    if characters_list != [] and char not in characters_list:
                        continue

                    char["passives"] = json.dumps(
                        self.get_passive_tree(account, char["name"])
                    )
                    char["items"] = json.dumps(self.get_items(account, char["name"]))
                    char["pob"] = pob_code_from_char(char)

                    self.db.store_char(account, char)

                    self.logger.info(
                        f"Scanned character {char['name']} from account {account}"
                    )

                    time.sleep(config.get("longsleep"))

        except Exception:
            self.logger.error(f"Error while scanning character...\n{format_exc()}")

            time.sleep(config.get("longsleep"))
