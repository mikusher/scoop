import logging
import os
from datetime import time, datetime

from database import prepare_database
from populate import get_euro_number
from log_managment import _init_logger

_init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

# Using the special variable
# __name__
if __name__ == "__main__":
    # import time and datetime and log when the script starts and ends
    start_time = datetime.now()
    logger.info('Started at: ' + str(start_time))
    prepare_database()
    get_euro_number()
    end_time = datetime.now()
    logger.info('Ended at: ' + str(end_time))
    logger.info('Duration: ' + str(end_time - start_time))
    logger.info('Finished')
