import os
from typing import Dict

import requests

from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

POESITE = os.getenv("POESITE") or "https://www.pathofexile.com"
USER_AGENT = os.getenv("USER_AGENT") or "POEStalker"


class API:
    def __init__(self):
        self.client = requests.session()
        self.client.headers.update({"User-Agent": USER_AGENT})

        self.error = None

    def _make_safe_call(self, url: str, params: dict = {}) -> dict:
        self.error = None

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
        ) as err:
            self.error = err
            raise err

        return response.json()

    def get_chars(self, account_name: str) -> Dict[str, str]:
        return self._make_safe_call(
            f"{POESITE}/character-window/get-characters?accountName=MaddEye92&realm=pc"
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
