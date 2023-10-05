"""Contains the business logic to Anomaly detection."""
import logging
import warnings

import urllib3

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=Warning)

# Log only error/critical message from imported modules.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("fsspec").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)
logging.getLogger("numba").setLevel(logging.ERROR)
logging.getLogger("numexpr").setLevel(logging.ERROR)
