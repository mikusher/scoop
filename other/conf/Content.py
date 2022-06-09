

import sqlite3
from datetime import timedelta, date, datetime
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from sqlmodel import create_engine


INSERT_EURO_NUMBERS = "insert into sc_euro_numbers (ball_1, ball_2, ball_3, ball_4, ball_5, star_1, star_2, play_day) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, '{7}')"
SQL_SELECT_DAYS = "select * from sc_euro_numbers where play_day = \'{0}\' ORDER BY ROWID ASC LIMIT 1"
LAST_INSERT_DAY = "select play_day FROM sc_euro_numbers WHERE id = (SELECT MAX(id) FROM sc_euro_numbers)"

SQLITE_DT = ""

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (XHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36 '
}

global_url = 'https://www.euro-millions.com/results'


def is_valid_day(day_check) -> requests:
    base_url = '{0}/{1}'.format(global_url, day_check)
    # Requests the numbers to URL and returns raw HTML
    page = requests.get(base_url, headers=headers)
    return page


def get_data_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def draws_days(start_dt, end_dt) -> List[str]:
    week_days = [0, 2, 3, 5, 6]
    lst_realms = []
    for dt in get_data_range(start_dt, end_dt):
        if dt.weekday() not in week_days:
            lst_realms.append(dt.strftime("%d-%m-%Y"))
    return lst_realms


def check_numbers(find_date, page) -> Dict:
    results = {
        "balls": [],
        "stars": [],
        "m1lao": [],
        "matches": {}
    }

    soup = BeautifulSoup(page.content, 'html.parser')
    get_balls = soup.find("div", {"id": "ballsAscending"}).findAll(attrs="ball")
    results['balls'] = list(map(lambda ball: int(ball.text), get_balls))

    get_lucky_star = soup.find("div", {"id": "ballsAscending"}).findAll(attrs="lucky-star")
    results['stars'] = list(map(lambda star: int(star.text), get_lucky_star))

    get_m1lao = soup.findAll("div", {"class": "raffle-content"})[0]
    results['m1lao'] = str(get_m1lao.text)

    table_win = []
    # table = soup.find('table', attrs={'class': 'table breakdown mobFormat'})
    table = soup.find('div', {'id': 'PrizePT'}).findAll(attrs={'class': 'table breakdown mobFormat'})[0]
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table_win.append([ele for ele in cols if ele])
    table_results = table_win[:-1]
    """
    Prize Per Winner - Portuguese Winners - Prize Fund Amount - Total Winners
    """
    results['matches'] = table_results

    return results


def day_exist_in_db(_day) -> bool:
    conn = None
    check = False
    try:
        conn = sqlite3.connect(SQLITE_DT)
        cur = conn.cursor()
        _in_db = SQL_SELECT_DAYS.format(_day)
        cur.execute(_in_db)
        ftc = cur.fetchone()
        if ftc is None:
            check = True
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()
    return check


def add_Number(balles, stars, day):
    try:
        conn = sqlite3.connect(SQLITE_DT)
        cur = conn.cursor()
        insert_query = INSERT_EURO_NUMBERS.format(balles[0], balles[1], balles[2], balles[3], balles[4], stars[0], stars[1], day)
        cur.execute(insert_query)
        cur.close()
        conn.commit()
    except (Exception, sqlite3.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def get_euro_number():
    """Get euro number."""
    # 13-02-2004
    today = date.today()
    start_day = get_last_insert_day()
    end_day = date(today.year, today.month, today.day)
    days_to_check = draws_days(start_day, end_day)
    for _day in days_to_check:
        page = is_valid_day(_day)
        if page.status_code != 404 and page.ok:
            day_in_db = day_exist_in_db(_day)
            if day_in_db:
                balls_and_star = check_numbers(_day, page)
                """
                Prize Per Winner - Portuguese Winners - Prize Fund Amount - Total Winners
                """
                ball = balls_and_star['balls']
                star = balls_and_star['stars']
                m1lao = balls_and_star['m1lao']
                matches = balls_and_star['matches']
                day = _day
                add_Number(ball, star, day)


def get_last_insert_day() -> date:
    conn = None
    last_day = date(2004, 2, 13)
    try:
        conn = sqlite3.connect(SQLITE_DT)
        cur = conn.cursor()
        _in_db = LAST_INSERT_DAY
        cur.execute(_in_db)
        ftc = cur.fetchone()
        if ftc is not None:
            pre_last_day = datetime.strptime(ftc[0], '%d-%m-%Y') + timedelta(days=1)
            last_day = date(pre_last_day.year, pre_last_day.month, pre_last_day.day)
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return last_day


# Using the special variable
# __name__
if __name__ == "__main__":
    engine = create_engine(SQLITE_DT, echo=True)
    get_euro_number()
