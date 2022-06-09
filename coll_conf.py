import logging
import re
import requests
from bs4 import BeautifulSoup
from constants import HEADERS, GLOBAL_URL
from datetime import timedelta
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
from converter_number import convert_to_words
from log_managment import _init_logger

_init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())


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
    def is_valid_day(day_check) -> requests:
        """
        Check if the day is valid.
        :param day_check:
        :return:
        """
        logger.info('Checking if the day is valid')
        base_url = '{0}/{1}#PrizePT'.format(GLOBAL_URL, day_check)
        logger.info('Base url: {}'.format(base_url))
        # Requests the numbers to URL and returns raw HTML
        page = requests.get(base_url, headers=HEADERS)
        logger.info('Requesting the page')
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

    @staticmethod
    def check_numbers(find_date, page) -> Dict:
        """
        Check the numbers of the day.
        :param find_date:
        :param page:
        :return:
        """
        logger.info('Checking the numbers of the day')
        results = {
            "balls": [],
            "stars": [],
            "m1lhao": 0,
            "winners": {}
        }
        # ballsAscending or ballsDrawn
        soup = BeautifulSoup(page.content, 'html.parser')

        # find balls
        get_balls = soup.find("div", {"id": "ballsAscending"}).findAll(attrs="ball")
        logger.info('Balls: {}'.format(get_balls))
        results['balls'] = list(map(lambda ball: int(ball.text), get_balls))
        # find stars
        get_lucky_star = soup.find("div", {"id": "ballsAscending"}).findAll(attrs="lucky-star")
        logger.info('Lucky stars: {}'.format(get_lucky_star))
        results['stars'] = list(map(lambda star: int(star.text), get_lucky_star))

        m1lhao = soup.find("div", {"class": "raffle-content"})
        logger.info('M1LHao: {}'.format(m1lhao))
        if m1lhao is not None:
            results['m1lhao'] = m1lhao.text.strip()

        # find numbers on table
        table = soup.find("div", {"id": "PrizePT"})
        if table is not None:
            # get all rows instead the first one
            table_rows = table.findAll("tr")[1:]
            table_rows_numbers = table_rows
            for row in table_rows_numbers:
                rs_numbers_name = re.findall('[0-9]+', row.findAll("td")[0].text.strip())
                for number in rs_numbers_name:
                    rs_money_win = row.findAll("td")[1].text.strip()[1:]
                    rs_person_win = re.sub('Rollover! |Rollover!', '', row.findAll("td")[4].text.strip())
                    if len(rs_numbers_name) > 1:
                        name = '{0}_{1}'.format(convert_to_words(rs_numbers_name[0]),
                                                convert_to_words(rs_numbers_name[1]))
                    else:
                        name = convert_to_words(rs_numbers_name[0])

                    rs_money_win = int(rs_money_win.replace(",", "").replace(".", ""))
                    # from re import search
                    # search('Rolldown! 0', rs_person_win)
                    if rs_person_win.find('Rolldown') != -1 or rs_person_win.find('Rollover') != -1:
                        rs_person_win = 0
                    else:
                        rs_person_win = int(rs_person_win.replace(",", "").replace(".", ""))
                    results['winners'][name] = [rs_money_win, rs_person_win]
        logger.info('Winners: {}'.format(results['winners']))
        return results
