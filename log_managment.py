
import os
import logging
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')


# create a public function for manage logging
def _init_logger(log_file, app_name):
    log_file = os.path.join(LOGS_FOLDER, log_file)
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # set the console handler
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setLevel(logging.DEBUG)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
