"""
Get million data and save to database.
Training data is saved to database.
Prediction data is saved to database.

Example: .env file:
------------------------------------------------------
PRODUCTION=True
DATABASE_DIALECT=postgresql
DATABASE_USER=miky.mikusher
DATABASE_PASSWORD=mikusher.19
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_DB_EX=satellite
------------------------------------------------------
"""


import logging
from datetime import datetime

from controller.database import prepare_database
from meta.populate import get_euro_number
from neural.network import brain_machine, neural
from utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)
debug_log = logging.getLogger(__name__)

# Using the special variable
# __name__
if __name__ == "__main__":
    # import time and datetime and log when the script starts and ends
    start_time = datetime.now()
    logger.info('Started at: ' + str(start_time))
    prepare_database()
    get_euro_number()
    # neural_result = neural()
    # use weka to predict
    # weka.predict(train_data, valid_data)

    end_time = datetime.now()
    logger.info('Ended at: ' + str(end_time))
    logger.info('Duration: ' + str(end_time - start_time))
    logger.info('Finished')
