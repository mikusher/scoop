import logging
import random
import re
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup as bs

from etl.utils.constants import GLOBAL_URL, header
from etl.utils.converter_number import convert_to_words
from etl.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"


class InternalSoup:

    def __init__(self, day):
        self.url = '{0}/results/{1}#PrizePT'.format(GLOBAL_URL, day)
        self.day = day

    @staticmethod
    def delay() -> None:
        time.sleep(random.uniform(1, 1))
        return None

    def isvalid_request(self) -> bool:
        """Check if the day is valid"""
        base_url = self.url
        InternalSoup.delay()
        page = requests.get(base_url, headers=header.generate())
        if page.status_code != 404 and page.ok:
            return True
        return False

    def get_soap(self) -> bs:
        """Constructs and returns a soup using the HTML content of `url` passed"""
        # initialize a session
        session = requests.Session()
        # set the User-Agent as a regular browser
        session.headers['User-Agent'] = USER_AGENT
        # request for english content (optional)
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        # make the request
        html = session.get(self.url)
        # return the soup
        r_bs = bs(html.content, "html.parser")
        return r_bs

    def get_numbers(self) -> Dict:
        """ get soap and return the numbers """
        soup = self.get_soap()

        results = {
            "balls": [],
            "stars": [],
            "m1lhao": 0,
            "winners": {}
        }

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
                    # from re-import search
                    # search('Rolldown! 0', rs_person_win)
                    if rs_person_win.find('Rolldown') != -1 or rs_person_win.find('Rollover') != -1:
                        rs_person_win = 0
                    else:
                        rs_person_win = int(rs_person_win.replace(",", "").replace(".", ""))
                    results['winners'][name] = [rs_money_win, rs_person_win]
        logger.info('Winners: {}'.format(results['winners']))

        return results
