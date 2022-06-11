import logging
from datetime import date, timedelta, datetime

from dotenv import load_dotenv, find_dotenv

from coll_conf import CollectionsSatellite
from database import create_session
from models import EuroAll, GameDate, WinResults
from log_managment import _init_logger

_init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())


def get_last_insert_day() -> date:
    conn = None
    last_day = date(2004, 2, 13)  # default value
    try:
        session = create_session()
        day_in_db = session.query(GameDate).order_by(GameDate.game_date.desc()).first()
        if day_in_db is not None:
            pre_last_day = day_in_db.game_date + timedelta(days=1)
            last_day = date(pre_last_day.year, pre_last_day.month, pre_last_day.day)
        session.close()
    except (Exception,) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
            logger.info('Database connection closed, for get last day in DB.')
    return last_day


def day_exist_in_db(_day) -> bool:
    session = None
    check = False
    try:
        session = create_session()
        check = session.query(GameDate).filter(GameDate.game_date == _day).first()
        if check is None:
            check = True
        session.close()
    except (Exception,) as error:
        logger.error(error)
    finally:
        if session is not None:
            session.close()
            logger.info('Database connection closed, for check day {}'.format(_day))
    return check


def add_number(balls, stars, day, million, winners):
    try:
        session = create_session()
        # game_date
        # convert datatime
        day = datetime.strptime(day, '%d-%m-%Y')

        game_date = GameDate(game_date=day)
        session.add(game_date)
        session.commit()

        # game_date_id
        game_to_get = session.query(GameDate).filter(GameDate.game_date == day).first()

        # EuroAll
        euro_all = EuroAll()
        euro_all.game_date_id = game_to_get.id
        euro_all.million = million if million is not None else 0
        euro_all.ball_week_1 = int(balls[0])
        euro_all.ball_week_2 = int(balls[1])
        euro_all.ball_week_3 = int(balls[2])
        euro_all.ball_week_4 = int(balls[3])
        euro_all.ball_week_5 = int(balls[4])
        euro_all.star_week_1 = int(stars[0])
        euro_all.star_week_2 = int(stars[1])
        session.add(euro_all)
        session.commit()

        win_results = WinResults()
        win_results.game_date_id = game_to_get.id
        # check if winner is None or empty
        if len(winners) == 0:
            logger.info('No winner')
        else:
            win_results.five_two_winners = winners.get('five_two', 0)[1]
            win_results.five_two_money = winners.get('five_two', 0)[0]
            win_results.five_one_winners = winners.get('five_one', 0)[1]
            win_results.five_one_money = winners.get('five_one', 0)[0]
            win_results.five_winners = winners.get('five', 0)[1]
            win_results.five_money = winners.get('five', 0)[0]
            win_results.four_two_winners = winners.get('four_two', 0)[1]
            win_results.four_two_money = winners.get('four_two', 0)[0]
            win_results.four_one_winners = winners.get('four_one', 0)[1]
            win_results.four_one_money = winners.get('four_one', 0)[0]
            win_results.four_winners = winners.get('four', 0)[1]
            win_results.four_money = winners.get('four', 0)[0]
            win_results.three_two_winners = winners.get('three_two', 0)[1]
            win_results.three_two_money = winners.get('three_two', 0)[0]
            win_results.three_one_winners = winners.get('three_one', 0)[1]
            win_results.three_one_money = winners.get('three_one', 0)[0]
            win_results.three_winners = winners.get('three', 0)[1]
            win_results.three_money = winners.get('three', 0)[0]
            win_results.two_two_winners = winners.get('two_two', 0)[1]
            win_results.two_two_money = winners.get('two_two', 0)[0]
            win_results.two_one_winners = winners.get('two_one', 0)[1]
            win_results.two_one_money = winners.get('two_one', 0)[0]
            win_results.one_two_winners = winners.get('one_two', 0)[1]
            win_results.one_two_money = winners.get('one_two', 0)[0]
        session.add(win_results)
        session.commit()

        session.close()

    except Exception as e:
        logger.error("Error inserting data for day {0}\nError: {1}".format(day, e))
        session.rollback()
        session.close()
    finally:
        if session is not None:
            session.close()
            logger.info('Database connection closed, for day {}'.format(day))


def get_euro_number():
    """Get euro number."""

    # begin euro millions is: 13-02-2004 / get (last_day + next_day) in database
    start_day = get_last_insert_day()  # '13-02-2004'
    today = date.today()
    end_day = date(today.year, today.month, today.day)
    days_to_check = CollectionsSatellite.draws_days(start_day, end_day)
    for _day in days_to_check:
        page = CollectionsSatellite.is_valid_day(_day)
        if page.status_code != 404 and page.ok:
            day_in_db = day_exist_in_db(_day)
            if day_in_db:
                balls_and_star = CollectionsSatellite.check_numbers(_day, page)
                balls = balls_and_star['balls']
                star = balls_and_star['stars']
                million = balls_and_star['m1lhao']
                winners = balls_and_star['winners']
                day = _day
                logger.info('Day:{0} Balls:{1} Star:{2} Million:{3} Winners:{4}'.format(day, balls, star, million, winners))
                # add number to database
                add_number(balls, star, day, million, winners)
                print('Day:{0} Balls:{1} Star:{2} Million:{3} Winners:{4}'.format(day, balls, star, million, winners))
