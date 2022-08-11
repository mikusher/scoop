"""
Get euro a million data and save to database.
Training data is saved to database.
Prediction data is saved to database.
"""

import logging
import os
from datetime import datetime

from etl.controller.database import prepare_database, create_superset_database
from etl.meta.populate import get_euro_number
from etl.utils.log_managment import init_logger
from etl.utils.managments import last_numbers

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

SUPERSET_CREATE_DB = os.getenv('SUPERSET_CREATE_DB', 'False').lower() in ('true', '1', 't')

# Using the special variable
# __name__
if __name__ == "__main__":
    # import time and datetime and log when the script starts and ends
    start_time = datetime.now()
    logger.info('Started at: ' + str(start_time))

    if SUPERSET_CREATE_DB:
        create_superset_database()

    prepare_database()
    get_euro_number()

    last_day_email = last_numbers()
    logger.info('Last day email send: ' + str(last_day_email))

    end_time = datetime.now()
    logger.info('Ended at: ' + str(end_time))
    logger.info('Duration: ' + str(end_time - start_time))
    logger.info('Finished')