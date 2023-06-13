import os
import json
import logging.config
from pathlib import Path


def get_project_root() -> Path:
    """"""
    return Path(__file__).parent.parent


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = get_project_root()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

with open(os.path.join(root, "data", "config.json")) as json_config_file:
    config = json.load(json_config_file)

service_host = config["service_host"]
service_port = config["service_port"]
urls_for_searching = config["urls_for_searching"]