import os

from dotenv import load_dotenv, find_dotenv
from fake_headers import Headers

load_dotenv(find_dotenv())

GLOBAL_URL = 'https://www.euro-millions.com/results'

# headers for requests
header = Headers(browser="chrome", os="win", headers=True)

HEADERS = {
    "undefinedaccept": 'application/json',
    "accept-encoding": 'gzip, deflate, br',
    "cache-control": 'no-cache',
    "pragma": 'no-cache',
    "referer": '{0}'.format(GLOBAL_URL),
    "accept-language": 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    "user-agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    "user-agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

# table names
TABLE_NAME_ALL = 'euro_all'
TABLE_NAME_GAME_DAY = 'euro_game_day'
TABLE_NAME_WIN_RESULTS = 'win_results'
TABLE_NAME_EURO_STAR_NUMBERS = 'euro_star_numbers'
TABLE_UNION_NUMBER = 'union_number'
TABLE_UNION_STAR = 'union_star'

SQL_SELECT_DAYS = "select * from euro_all where play_day = \'{0}\' ORDER BY ROWID ASC LIMIT 1"
INSERT_EURO_NUMBERS = "insert into euro_all (ball_1, ball_2, ball_3, ball_4, ball_5, star_1, star_2, play_day) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, '{7}')"
LAST_INSERT_DAY = "select play_day FROM euro_all WHERE id = (SELECT MAX(id) FROM euro_all)"

# end date
END_DATE = os.getenv('END_DATE')

# Database you intend to use
DB_CORE_HOST = os.getenv('DB_CORE_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE_NAME = os.getenv('DB_DATABASE_NAME')
