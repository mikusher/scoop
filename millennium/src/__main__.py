#!/usr/bin/env python

"""
Get euro a million data and save to database.
Training data is saved to database.
Prediction data is saved to database.
"""
import argparse
import logging
import os
from datetime import datetime

from src.controller.database import prepare_database, create_superset_database
from src.meta.populate import get_euro_number
from src.utils.log_managment import init_logger
from src.utils.managments import last_numbers

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

VERSION = "1.0"

banner = """
'##::::'##:'####:'##:::::::'##:::::::'########:'##::: ##:'##::: ##:'####:'##::::'##:'##::::'##:
 ###::'###:. ##:: ##::::::: ##::::::: ##.....:: ###:: ##: ###:: ##:. ##:: ##:::: ##: ###::'###:
 ####'####:: ##:: ##::::::: ##::::::: ##::::::: ####: ##: ####: ##:: ##:: ##:::: ##: ####'####:
 ## ### ##:: ##:: ##::::::: ##::::::: ######::: ## ## ##: ## ## ##:: ##:: ##:::: ##: ## ### ##:
 ##. #: ##:: ##:: ##::::::: ##::::::: ##...:::: ##. ####: ##. ####:: ##:: ##:::: ##: ##. #: ##:
 ##:.:: ##:: ##:: ##::::::: ##::::::: ##::::::: ##:. ###: ##:. ###:: ##:: ##:::: ##: ##:.:: ##:
 ##:::: ##:'####: ########: ########: ########: ##::. ##: ##::. ##:'####:. #######:: ##:::: ##:
..:::::..::....::........::........::........::..::::..::..::::..::....:::.......:::..:::::..::
                                                                            v%s by @mikusher 
""" % VERSION


def parse_args():
    print(banner)
    parser = argparse.ArgumentParser(add_help=True, description="Automatic get euro million values.")
    parser.add_argument("-d", "--stardate", default="13-02-2004", help="Day to start getting data, format: dd-mm-yyyy")
    parser.add_argument("-s", "--superset_db", default=False, action="store_true",
                        help="Create a superset database, default: False")
    parser.add_argument("-l", "--show_last", default=False, action="store_true", help="Show last results in the database")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + VERSION)
    return parser.parse_args()


def main():
    options = parse_args()

    # check superset create database on parse args
    SUPERSET_CREATE_DB = os.getenv('SUPERSET_CREATE_DB', 'False').lower() in ('true', '1', 't')

    start_time = datetime.now()
    logger.info('Started at: ' + str(start_time))

    if SUPERSET_CREATE_DB or options.superset_db:
        create_superset_database()
    # prepare_database()
    # get_euro_number()

    if options.show_last or True:
        email_send, message = last_numbers()
        if email_send:
            print(message)

    end_time = datetime.now()
    logger.info('Ended at: ' + str(end_time))
    logger.info('Duration: ' + str(end_time - start_time))
    logger.info('Finished')


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
