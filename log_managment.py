
import os
import logging
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')


# create a public function for manage logging
def create_logger(log_file):
    log_file = os.path.join(LOGS_FOLDER, log_file)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
