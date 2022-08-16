import os
import logging
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_FOLDER = os.path.join(BASE_DIR, '../logs')
if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)


# create a public function for manage logging
def init_logger(log_file, app_name):
    log_file = os.path.join(LOGS_FOLDER, log_file)
    # create a file handler if not exists
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
    # create a logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    # print to console if in debug mode
    if os.environ.get('DEBUG'):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
    logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
