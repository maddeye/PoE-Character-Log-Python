import os
import json

from os.path import exists
from typing import Dict


SETTING_PATH = os.getenv("SETTINGS_PATH") or "./settings.json"


DEFAULT_SETTINGS: Dict = {
    "accounts": os.getenv("ACCOUNTS") or [],
    "characters": os.getenv("CHARACTERS") or [],
    "shortsleep": os.getenv("SHORT_SLEEP") or 1,
    "longsleep": os.getenv("LONG_SLEEP") or 120,
    "maxlevel": os.getenv("MAX_LEVEL") or 100,
    "minlevel": os.getenv("MIN_LEVEL") or 5,
    "levelstep": os.getenv("LEVEL_STEP") or 1,
}


class CONFIG:
    def __init__(self):
        self.config = {}

        if not exists(SETTING_PATH):
            with open(SETTING_PATH, "w") as f:
                f.write(json.dumps(DEFAULT_SETTINGS, indent=2))

    def get(self, key: str) -> str:
        with open(SETTING_PATH, "r") as f:
            self.config = json.loads(f.read())

        return self.config[key]
