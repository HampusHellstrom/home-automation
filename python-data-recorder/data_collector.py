import json
import requests


def read_config():
    with open("config.json") as f:
        config = json.load(f)
