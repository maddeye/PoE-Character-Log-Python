import json
import os
import pathlib
import sys

from typing import Dict, Union, List

SETTING_PATH = os.getenv("SETTINGS_PATH") or "./settings.json"

DEFAULT_SETTINGS: Dict = {
    "accounts": [],
    "characters": [],
    "shortsleep": 1,
    "longsleep": 120,
    "maxlevel": 100,
    "minlevel": 5,
    "levelstep": 1,
}


def ensure_config_path():
    """
    Esures that the config file is created and readable
    """

    path = pathlib.Path(SETTING_PATH)

    if not path.exists():
        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(json.dumps(DEFAULT_SETTINGS, indent=2))
        except Exception:
            print(
                f"Fatal Error: Unable to create default configuration "
                f"at {SETTING_PATH}"
            )
            sys.exit(1)


def read_config() -> Dict:
    """
    Open and read the config file
    """
    with open(SETTING_PATH, "r") as f:
        return json.loads(f.read())


def get(key: str) -> Union[str, List[str], int]:
    """
    Read the config file or environment variables and return value at given key
    """
    config: Dict = read_config()

    return os.getenv(key.upper()) or config[key]
