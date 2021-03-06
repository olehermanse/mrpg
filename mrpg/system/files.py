import os
import json
import sys

from collections import OrderedDict

from mrpg.utils.utils import jsonify


def json_load(data):
    try:
        return json.loads(data, object_pairs_hook=OrderedDict)
    except json.decoder.JSONDecodeError as err:
        print(f"ERROR: Invalid json syntax: {data}")
        sys.exit(1)


def save_data(data, path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if isinstance(data, dict) or isinstance(data, list):
        data = jsonify(data)
    with open(path, "w", encoding="utf-8") as out_file:
        out_file.write(data)


def load_data(path):
    try:
        with open(path, "r", encoding="utf-8") as in_file:
            return json_load(in_file.read())
    except FileNotFoundError:
        return None
