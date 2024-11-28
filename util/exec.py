import logging
import subprocess
import sys
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run(command: List[str]):
    logger.info(" ".join(command))
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logger.error("Return code: {}".format(e.returncode))
        exit(e.returncode)
    logger.info("OK")
    return str(output)
