"""Helper for the File interaction."""
import os

import daiquiri
import yaml

from src.common.config import DAIQUIRI_LOG_LEVEL

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
_logger = daiquiri.getLogger(__name__)


def get_json_from_yaml_file(yaml_file_path):
    """Get json object from the yaml file."""
    if os.path.exists(yaml_file_path):
        with open(yaml_file_path, "r", encoding="utf8") as file:
            data = yaml.safe_load(file)
    else:
        _logger.error(f"File not found : {yaml_file_path}")
        data = None
    return data
