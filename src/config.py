import os
import json
import logging.config
from pathlib import Path
from src.data_types import Parameters

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
    config_dict = json.load(json_config_file)

parameters = Parameters.parse_obj(config_dict)