import os
import json
from definitions import ROOT_DIR

def _read_secrets() -> dict:
    filename = os.path.join(ROOT_DIR, 'secrets/db_secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}
    
secrets = _read_secrets()

def get_secrets():
    return secrets