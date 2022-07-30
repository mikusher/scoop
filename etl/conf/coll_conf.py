import logging
from datetime import timedelta
from typing import List

import requests

from etl.utils.constants import GLOBAL_URL, header
from etl.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)


def get_data_range(start_date, end_date):
    """
    Get the data range from the start date to the end date.
    :param start_date:
    :param end_date:
    :return:
    """
    logger.info('Getting the data range from {} to {}'.format(start_date, end_date))
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


class CollectionsSatellite:

    @staticmethod
    def is_valid_day(day_check, loop) -> requests:
        """
        Check if the day is valid.
        :param day_check:
        :return:
        """
        logger.info('Checking if the day is valid')
        base_url = '{0}/results/{1}#PrizePT'.format(GLOBAL_URL, day_check)
        logger.info('Base url: {}'.format(base_url))
        # Requests the numbers to URL and returns raw HTML
        delay()
        random_header = header.generate()
        page = requests.get(base_url, headers=random_header)
        logger.info('Requesting the page')
        if page.status_code == 404:
            loop.update(1)
        return page

    @staticmethod
    def draws_days(start_dt, end_dt) -> List[str]:
        """
        Get the days of the draws.
        :param start_dt:
        :param end_dt:
        :return:
        """
        logger.info('Getting the days of the draws')
        week_days = [0, 2, 3, 5, 6]
        lst_realms = []
        for dt in get_data_range(start_dt, end_dt):
            if dt.weekday() not in week_days:
                lst_realms.append(dt.strftime("%d-%m-%Y"))
        logger.info('Days of the draws: {}'.format(lst_realms))
        return lst_realms
